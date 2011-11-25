#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import sys


client = SnakeClient.CloudSnakeClient( sys.argv[ 1 ], sys.argv[ 2 ] )

snake = SnakeClient.CloudSnakeMapper( client )


#snake.set_value( 'avain1', 'moi' )
#snake.set_value( 'avain_9001', 'sending' )

print snake.get_value( 'avain_9001' )

