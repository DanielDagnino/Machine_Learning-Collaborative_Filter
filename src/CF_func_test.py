
from ml_data_time import search_bin

#******************************************************************************#
# Define error function using a user list different from the one used for the bu and bi.
def error_L2_bound( us_test, mu, bu_test, bi, bib ):
	
	# Loop over users.
	error_test = 0.
	car_out = 0
	for u in xrange(len(us_test)):
		
		# Loop over the movies for each user.
		for k in xrange(us_test[u].car):
			
			# Movie id.
			i = us_test[u].id[k]-1
			
			# In case the film is in the feeding list.
			if i<=len(bi):
				
				# Estimated rate.
				estim = mu + bu_test[u] + bi[i] + sum(bib[i])
				
				# Rate bounds.
				estim = max( 0.5, min( estim, 5.0 ) )
				
				# Error.
				error_test += ( us_test[u].rate[k] - estim )**2
			else:
				car_out += 1
		
	return error_test, car_out









