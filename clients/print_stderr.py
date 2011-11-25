#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'maintenance' )


get_stream = client.get_method( 'get_stream' )



lines = get_stream( name = "stderr" )['result']

for line in lines:
	print line
