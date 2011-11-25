#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import sys


client = SnakeClient.CloudSnakeClient( sys.argv[ 1 ], sys.argv[ 2 ] )


add_key = client.get_method( 'partition_add_key' )

print add_key( sys.argv[ 3 ], sys.argv[ 4 ], 'main' )
