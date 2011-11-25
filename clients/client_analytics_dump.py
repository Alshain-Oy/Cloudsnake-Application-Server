
#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, sys, time

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', sys.argv[ 1 ] )


mapped_object = SnakeClient.CloudSnakeMapper( client )

pprint.pprint( mapped_object.dump_analytics() )
