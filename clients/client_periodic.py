
#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, sys, time

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', sys.argv[ 1 ] )


mapped_object = SnakeClient.CloudSnakeMapper( client )

mapped_object.init()

job_id = mapped_object.periodic_add_job( 10, 'increase', [] )

print "Job id:", job_id

for i in range( 10 ):
	time.sleep( 5 )
	print mapped_object.get_counter()

print "Removing job..."
mapped_object.periodic_remove_job( job_id )


for i in range( 5 ):
	time.sleep( 5 )
	print mapped_object.get_counter()
