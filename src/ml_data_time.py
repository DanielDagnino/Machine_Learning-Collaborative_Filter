
import ml_class as ml

#******************************************************************************#
def search_bin( i, time, t0, t_bins_mv ):
	
	#--------------------------------------------------------#
	# Search bin.
	
	# Loop over bins.
	for bin in xrange(len(t_bins_mv)):
		if ( time < t0 + t_bins_mv[bin] ): return bin
	
	return len(t_bins_mv)














