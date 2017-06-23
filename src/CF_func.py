
import numpy as np
from ml_data_time import search_bin

#******************************************************************************#
# Define error function.
def error_L2( us, mu, bu, bi, bib ):
	
	# Loop over users.
	error = 0.
	for u in xrange(len(us)):
		
		# Loop over the movies for each user.
		for k in xrange(us[u].car):
			
			# Movie id.
			i = us[u].id[k]-1
			
			# Estimated rate.
			estim = mu + bu[u] + bi[i] + sum(bib[i])
			
			# Error.
			if shuffle_weight_u[u].id[k]: error += ( us[u].rate[k] - estim )**2
		
	return error
    
#******************************************************************************#
# Define gradient + error function.
def pre_grad_error_L2( us, mu, bu, bi, bib, t0_mv, t_bins_mv, n_t_bins_mv ):
	
	# Loop over users.
	sumer_bi = np.zeros_like(bi)
	sumer_bib = np.zeros_like(bib)
	sumer_bu = np.zeros_like(bu)
	error = 0.
	for u in xrange(len(us)):
		
		# Loop over the movies for each user.
		for k in xrange(us[u].car):
			
			# Movie id.
			i = us[u].id[k]-1
			
			# Bin of the item.
			i_bin = search_bin( i, us[u].time[k], t0_mv[i], t_bins_mv )
			
			# Estimated rate.
			estim = mu + bu[u] + bi[i] + sum(bib[i])
			
			# Summation that appears in the gradient.
			if shuffle_weight_u[u].id[k]: 
				sumer_bu[u]         += ( us[u].rate[k] - estim )
				sumer_bi[i]         += ( us[u].rate[k] - estim )
				sumer_bib[i][i_bin] += ( us[u].rate[k] - estim )
			
			# Error.
			if shuffle_weight_u[u].id[k]:  error += ( us[u].rate[k] - estim )**2 
				
	col_totals = [ sum(x[i] for i in range(len(x)) ) for x in zip(*sumer_bib) ]
#	print '   ', error, sum(sumer_bu[0:(len(sumer_bu)-1)]), sum(sumer_bi[0:(len(sumer_bi)-1)])
	#print '   ', error, sum(float(sumer_bu[i]) for i in range(len(sumer_bu))), col_totals
	
	return error, sumer_bu, sumer_bi, sumer_bib

#******************************************************************************#
# Gradient
def gradient( bu, bi, bib, sumer_bu, sumer_bi, sumer_bib, car_us, car_mv, car_bin_mv ):
	
	# Regularization term.
	l3 = 0.001
	
	# Gradient.
	grd_bu  = ( -sumer_bu  + l3*bu  )
	grd_bi  = ( -sumer_bi  + l3*bi  )
	grd_bib = ( -sumer_bib + l3*bib )
	
	return grd_bu, grd_bi, grd_bib, l3

#******************************************************************************#
# Define perturbation function.
def minimize( i_saved, bu, bi, bib, grd_bu, grd_bi, grd_bib, var, grad, n_saved ):
	
	# Join var and grad.
	var[i_saved-1][:]  = np.concatenate( (    bu,    bi,np.ravel(    bib)), axis=0 )
	grad[i_saved-1][:] = np.concatenate( (grd_bu,grd_bi,np.ravel(grd_bib)), axis=0 )
	
	# Search Min.
	srch = search_min( i_saved-1, var, grad )
	
	# De-join srch.
	ia = 0
	ib = len(bu)
	srch_bu = srch[ia:ib]
	
	ia = ib
	ib = ia+len(bi)
	srch_bi = srch[ia:ib]
	
	ia = ib
	ib = len(srch)
	srch_bib = srch[ia:ib].reshape(bib.shape)
	
	# Update gradient.
	if i_saved==n_saved:
		for k in xrange(1,n_saved):
			var[k-1]  = var[k]
			grad[k-1] = grad[k]
	
	return srch_bu, srch_bi, srch_bib


#******************************************************************************#
# Define perturbation function.
def search_min( i_saved-1, var, grad ):
	if i_saved>1:
		srch = grad[k] + grad[k-1]

#******************************************************************************#
# Define perturbation function.
def perturbation( bu, bi, bib, alpha, srch_bu, srch_bi, srch_bib, car_us, car_mv, car_bin_mv, l3 ):
	
	# Perturbation.
	bu_new  = bu  + alpha*srch_bu
	bi_new  = bi  + alpha*srch_bi
	bib_new = bib + alpha*srch_bib
	
	return bu_new, bi_new, bib_new

#******************************************************************************#
# Define error function.
def error_L2_bound( us, mu, bu, bi, bib ):
	
	# Loop over users.
	error = 0.
	for u in xrange(len(us)):
		
		# Loop over the movies for each user.
		for k in xrange(us[u].car):
			
			# Movie id.
			i = us[u].id[k]-1
			
			# Estimated rate.
			estim = mu + bu[u] + bi[i] + sum(bib[i])
			
			# Rate bounds.
			estim = max( 0.5, min( estim, 5.0 ) )
			
			# Error.
			if shuffle_weight_u[u].id[k]: error += ( us[u].rate[k] - estim )**2
		
	return error















