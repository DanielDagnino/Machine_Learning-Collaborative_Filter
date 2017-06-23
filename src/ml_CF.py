
import numpy as np
import sys
import CF_func

#******************************************************************************#
# Minimization function: Gradient descendent.
def CF( us, sum_us, sum_mv, car_us, car_mv, car_bin_mv, t0_mv, t_bins_mv, n_t_bins_mv ):
	
	#******************************************************************************#
	# 
	maxiter = 10
	n_saved_max = 2
	n_saved = min( n_saved_max, maxiter )
	dim_all = len(sum_us) + len(sum_mv) + len(sum_mv)*n_t_bins_mv
	alp_1 = 1.0
	
	var  = np.zeros((n_saved,dim_all),float)
	grad = np.zeros((n_saved,dim_all),float)
	
	#******************************************************************************#
	# Get shuffle.
	shuffle_weight_u = get_shuffle( us )
	
	#******************************************************************************#
	# Mean and cardinal.
	car = sum(car_us)
	mu = sum(sum_us)/car
	
	# Loop over iteration to find the min.
	bib = np.zeros((len(sum_mv),n_t_bins_mv))
	bi  = np.zeros(len(sum_mv))
	bu  = np.zeros(len(sum_us))
	bib_new = np.zeros_like(bib)
	bi_new  = np.zeros_like(bi)
	bu_new  = np.zeros_like(bu)
	error_new = sys.float_info.max
	i_saved = 0
	for iteration in xrange(1,maxiter+1):
		#--------------------------------------------------------#
		# Grad + error calculation.
		error, sumer_bu, sumer_bi, sumer_bib = CF_func.pre_grad_error_L2( us, mu, bu, bi, bib, t0_mv, t_bins_mv, n_t_bins_mv )
		
		grd_bu, grd_bi, grd_bib, l3 = CF_func.gradient( bu, bi, bib, sumer_bu, sumer_bi, sumer_bib, car_us, car_mv, car_bin_mv )
		
		i_saved = min(i_saved+1,n_saved)
		srch_bu, srch_bi, srch_bib = CF_func.minimize( i_saved, bu, bi, bib, grd_bu, grd_bi, grd_bib, var, grad, n_saved )
		
		#--------------------------------------------------------#
#		col_totals = [ sum(x[i] for i in range(len(x)) ) for x in zip(*sumer_bi) ]
#		print '   ', error, sum(sumer_bu), col_totals
		
		#--------------------------------------------------------#
		print '   iteration i_saved', iteration, i_saved
		
		#--------------------------------------------------------#
		# 
		rep = 0
		while error_new>error:
			# 
			rep += 1
			
			# Shuffle.
			shuffle( us, shuffle_weight_u )
			
			# Perturbation.
			bu_new, bi_new, bib_new = CF_func.perturbation( bu, bi, bib, alp_1, srch_bu, srch_bi, srch_bib, car_us, car_mv, car_bin_mv, l3 )
			# Error of the perturbation.
			error_new = CF_func.error_L2( us, mu, bu_new, bi_new, bib_new )
			
			# QC.
			if error_new<error:   # Update.
				print 'min-OK', error_new, error
				for u in xrange(len(bu)): bu[u] = bu_new[u]
				for i in xrange(len(bi)): bi[i] = bi_new[i]
				for i in xrange(len(bib)): bib[i][:] = bib_new[i][:]
			else:   # Reduce step length.
				print 'min-NO', error_new, error
				alpha *= 0.5
			
			## 
			#if rep==5: break
		
	#******************************************************************************#
	# 
	return bu, bi, bib



#******************************************************************************#
# 
def get_shuffle( us ):
	
	shuffle_weight_u = []*len(us)
	for u in xrange(len(us)):
		
		# 
		shuffle_weight_u[u] = np.zeros(us[u].car)
	
#******************************************************************************#
# 
def shuffle( us, shuffle_weight_u ):
	
	shuffle_weight_u = []*len(us)
	for u in xrange(len(us)):
		
		# Loop over the movies for each user.
		for k in xrange(us[u].car):
			
			# Movie id.
			shuffle_weight_u[u].id[k] = bool(random.getrandbits(1))
			
			







