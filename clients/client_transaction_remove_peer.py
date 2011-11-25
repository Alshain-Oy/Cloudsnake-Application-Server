
#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, sys, time

client = SnakeClient.CloudSnakeClient( sys.argv[ 1 ], 'main' )


mapped_object = SnakeClient.CloudSnakeMapper( client )

mapped_object.transaction_remove_peer( sys.argv[ 2 ]  )
