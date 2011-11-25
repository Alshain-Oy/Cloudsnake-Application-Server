#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, time

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'main' )


test_func = client.get_method( 'test_001' )
test_func2 = client.get_method( 'get_feed' )


N = 1000
t0 = time.clock()

for i in range( N ):
	z = test_func()[ 'result' ]
	#print sum( z )

t1 = time.clock()

print "It took %.3f secs to perform %i requests..."%( t1-t0, N )
print "Per request time = %.3f ms"%( (t1-t0)/N * 1000 )

