#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, sys

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'main' )


remove_node = client.get_method( 'remove_node' )



print remove_node( node = sys.argv[ 1 ] )

