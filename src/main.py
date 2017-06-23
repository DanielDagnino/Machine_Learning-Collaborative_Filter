#!/usr/bin/python

#******************************************************************************#
import os
os.system('clear; clear;')

import re
import math

#import scipy
import numpy as np

#******************************************************************************#
import ml_class as ml
import ml_data
import ml_CF
import CF_func
import CF_func_test

#******************************************************************************#
n_user_learning = 10000

#******************************************************************************#
# Bins of time for all the items (the last is implicit infinite).
s_day = 60*60*24
#t_bins_mv = [ 2*30*s_day, 2*365*s_day, 5*365*s_day, 10*365*s_day ]
#t_bins_mv = [ 7*s_day, 30*s_day, 3*30*s_day, 6*30*s_day, 365*s_day, 365*2*s_day ]
t_bins_mv = [ 2*30*s_day, 2*365*s_day ]
#t_bins_mv = [ 0, 2*365*s_day ]
#t_bins_mv = [ 0 ]
#t_bins_mv = []
n_t_bins_mv = len(t_bins_mv) + 1

#******************************************************************************#
#******************************************************************************#
# Feeding the ml.
#******************************************************************************#
# Read data.
us = ml_data.build_data( '../1b-movie_data_set_formatted_time/ratings_upto_'+str(n_user_learning)+'.csv' )

sum_us, car_us = ml_data.variables_us( us )

sum_mv, car_mv, car_bin_mv, t0_mv = ml_data.variables_mv( us, t_bins_mv, n_t_bins_mv )

#******************************************************************************#
# CF mcahine learning.
bu, bi, bib = ml_CF.CF( us, sum_us, sum_mv, car_us, car_mv, car_bin_mv, t0_mv, t_bins_mv, n_t_bins_mv )

#******************************************************************************#
# Final MSE.
car = sum(car_us)
mu = sum(sum_us)/car
error = CF_func.error_L2( us, mu, bu, bi, bib )
error = math.sqrt( error/car )

print 'mean error learned = ', error

#quit()

#******************************************************************************#
#******************************************************************************#
# Testing the ml.
#******************************************************************************#
# Final MSE.

# Read test file.
us_test = ml_data.build_data( "../1b-movie_data_set_formatted_time/ratings_fmt_test.csv" )

sum_us_test, car_us_test = ml_data.variables_us( us_test )

sum_mv_test, car_mv_test, car_bin_mv_test, t0_mv_aux = ml_data.variables_mv( us_test, t_bins_mv, n_t_bins_mv )

# Calculate bu for the new users.
#bu_test = []
#for u in xrange(len(us_test)):
	#bu_test.append( sum(sum_us_test)/sum(car_us_test) - mu )
bu_test = np.zeros_like(bu)
for u in xrange(len(bu)):
	bu_test[u] = sum(sum_us_test)/sum(car_us_test) - mu
	
# Error.
car_test = sum(car_us_test)
error, car_out = CF_func_test.error_L2_bound( us_test, mu, bu_test, bi, bib )
error = math.sqrt( error/(car_test-car_out) )

print 'mean error test    = ', error
print 'car, car_test, car_out = ', car, car_test, car_out

#******************************************************************************#
# Final MSE with b*=0.

#bu_zero_test = [0.]*len(bu_test)
#bi_zero = [[0.]*n_t_bins_mv]*len(bi)
bu_zero_test = np.zeros_like(bu_test)
bi_zero = np.zeros_like(bi)
bib_zero = np.zeros_like(bib)

# Error.
error, car_out = CF_func_test.error_L2_bound( us_test, mu, bu_zero_test, bi_zero, bib_zero )
error = math.sqrt( error/(car_test-car_out) )

print 'mean error zero    = ', error






















