#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, time

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'main' )


test_func = client.get_method( 'test_001' )
test_func2 = client.get_method( 'get_feed' )


t0 = time.clock()
R = test_func2( feed_url =  'http://rss.slashdot.org/Slashdot/slashdot' )
t1 = time.clock()
pprint.pprint( R )
print "It took %.3f secs"%( t1 - t0 )
