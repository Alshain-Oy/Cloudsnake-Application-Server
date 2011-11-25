
#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, sys, time

client = SnakeClient.CloudSnakeClient( sys.argv[ 1 ], 'main' )


mapped_object = SnakeClient.CloudSnakeMapper( client )

#mapped_object.t_test( "avain", "arvo:" + sys.argv[ 1 ]  )

print mapped_object.t_test2( "avain" )
