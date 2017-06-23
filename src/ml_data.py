
import numpy as np
import csv
import ml_class as ml
from ml_data_time import search_bin

#******************************************************************************#
def build_data( file_name ):
	
	#--------------------------------------------------------#
	# Read full CSV file.
	with open( file_name, 'rb') as csvfile:
		f_rat = csv.reader( csvfile, delimiter=',', quotechar='"' )
		
		# Header.
		line = f_rat.next()
		
		# Initialization of the list of values: (usid,rate).
		sumrate = 0.
		cont    = 0
		score   = []
		scid    = []
		sct     = []
		us      = [ ml.user() ]
		
		# Loop line per line.
		# Read all the values + introduce in the list mv.
		for line in f_rat:
			# Values to sum to the mean.
			usid = int(line[0])
			mvid = int(line[1])
			rate = float(line[2])
			time = int(line[3])
			
			# Continue a previous one.
			if usid<=len(us):
				# Update user with new info.
				sumrate += rate
				cont    += 1
				score.append(rate)
				scid.append(mvid)
				sct.append(time)
				us[usid-1] = ml.user( sumrate, cont, scid, score, sct )
			# New one.
			else:
				# Zero values of still not introduced users.
				incr = usid-len(us)-1
				for rep in range(incr): us.append( ml.user() )
				# New users.
				sumrate = rate
				cont    = 1
				score   = [rate]
				scid    = [mvid]
				sct     = [time]
				us.append( ml.user( sumrate, cont, scid, score, sct ) )
				
	return us
	
#******************************************************************************#
# Rate for the users.
def variables_us( us ):
	
	#car_us = []
	#sum_us = []
	#for u in xrange(len(us)):
		#sum_us.append( us[u].sum )
		#car_us.append( us[u].car )
		
	car_us = np.empty((0,1), float)
	sum_us = np.empty((0,1), float)
	for u in xrange(len(us)):
		sum_us = np.append( sum_us, us[u].sum )
		car_us = np.append( car_us, us[u].car )
		
	return sum_us, car_us
	
#******************************************************************************#
# Rate of movies (instead of the previous one for users).
# Time of appearence for all the items.
# Cardinal.
def variables_mv( us, t_bins_mv, n_t_bins_mv ):
	
	#--------------------------------------------------------#
	# Loop over users.
	#car_mv = [0]
	#sum_mv = [0.]
	#car_bin_mv = [[[]]*n_t_bins_mv]
	car_mv = np.zeros((1,1),int)
	sum_mv = np.zeros((1,1),float)
	car_bin_mv = np.zeros((1,n_t_bins_mv),int)
	t0_mv = [[]]
	for u in xrange(len(us)):
	
		# Sum the rate of the movies of the user.
		for k in xrange(us[u].car):
		
			# Zero values of still not introduced users.
			incr = us[u].id[k]-len(sum_mv)
			if incr>0: 
				#car_mv.extend([0]*incr)
				#sum_mv.extend([0.]*incr)
				#car_bin_mv.extend([[[]]*n_t_bins_mv]*incr)
				car_mv = np.append( car_mv, np.zeros((incr,1)) )
				sum_mv = np.append( sum_mv, np.zeros((incr,1)) )
				car_bin_mv = np.concatenate( (car_bin_mv,np.zeros((incr,n_t_bins_mv),int)) ,axis=0)
				t0_mv.extend([[]]*incr)
											
			# Movie id.
			i = us[u].id[k]-1
			
			# Suming the rate.
			car_mv[i] += 1
			sum_mv[i] += us[u].rate[k]
			
			# Min time.
			t0_mv[i] = min( t0_mv[i], us[u].time[k] )
			
			# Cardinal per bin.
			#car_bin_mv[i] = [0]*n_t_bins_mv
			
	#--------------------------------------------------------#
	# Time of appearence for all the items.
	
	# Loop over users.
	for u in xrange(len(us)):
		
		# Sum the rate of the movies of the user.
		for k in xrange(us[u].car):
			
			# Movie id.
			i = us[u].id[k]-1
			
			# Bin of the item.
			i_bin = search_bin( i, us[u].time[k], t0_mv[i], t_bins_mv )
			
			# Suming the cardinal of each bin.
			car_bin_mv[i][i_bin] += 1
	
	# Mean number of rates per bin.
	col_totals = [ sum(x[i] for i in range(len(x)) if car_mv[i]!=0 ) for x in zip(*car_bin_mv) ]
	print 'mean #rates per bin', [ round(100*float(x)/sum(car_mv)) for x in col_totals ], '%'
	
	#--------------------------------------------------------#
	return sum_mv, car_mv, car_bin_mv, t0_mv















