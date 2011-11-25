
#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, sys, time

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', sys.argv[ 1 ] )


mapped_object = SnakeClient.CloudSnakeMapper( client )


job_id = mapped_object.queue_add_job( 'get_feed', { 'feed_url': 'http://rss.slashdot.org/Slashdot/slashdot' } )

print "Job Id:", job_id

while not mapped_object.queue_has_results( job_id ):
	time.sleep( 0.5 )

result = mapped_object.queue_get_results( job_id )

pprint.pprint( result )
