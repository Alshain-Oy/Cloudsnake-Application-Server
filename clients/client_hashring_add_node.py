#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, sys

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'main' )


add_node = client.get_method( 'add_node' )



print add_node( node = sys.argv[ 1 ] )

