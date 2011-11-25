#!/usr/bin/env python

import libJobQueue

import time

queue = libJobQueue.JobQueue()


funkkari = lambda x: x+1


queue.setDaemon( True )
queue.start()

time.sleep( 3 )

key = queue.add_job( funkkari, 3 )

print "key:", key

while not queue.has_results( key ):
	time.sleep( 0.1 )
	
print queue.get_results( key )


