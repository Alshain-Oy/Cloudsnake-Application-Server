#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, sys

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'main' )


get_node = client.get_method( 'get_node' )



print get_node( key = sys.argv[ 1 ]  )

