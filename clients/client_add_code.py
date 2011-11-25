#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import sys


client = SnakeClient.CloudSnakeClient( sys.argv[ 1 ], sys.argv[ 2 ] )


add_artifact = client.get_method( 'add_artifact' )




code = ""
with open( sys.argv[ 3 ], 'r' ) as handle:
	code = handle.read()


print add_artifact( code  )
