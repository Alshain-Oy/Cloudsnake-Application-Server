#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import sys


client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', sys.argv[ 1 ] )


add_artifact = client.get_method( 'add_artifact' )




code = ""
with open( sys.argv[ 2 ], 'r' ) as handle:
	code = handle.read()


print add_artifact( code  )
