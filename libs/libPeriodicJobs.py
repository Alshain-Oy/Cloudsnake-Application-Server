#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import threading, time

import hashlib, random

class AsyncJob( threading.Thread ):
	def __init__( self, method, params ):
		threading.Thread.__init__( self )
		self.method = method
		self.params = params
	
	def run( self ):
		self.method( self.params )
		


class PeriodicJobs( threading.Thread ):
	def __init__( self ):
		threading.Thread.__init__( self )
		self.jobs = {}
		self.clock = 0

	def generate_key( self ):
		return hashlib.md5( str( time.time() ) + ":" + str( random.random() ) ).hexdigest()
	

	def add_job( self, interval, method, params ):
		#self.jobs.append( (interval, method, params ) )
		key = self.generate_key()
		self.jobs[ key ] = (interval, method, params )
		return key
	
	def remove_job( self, key ):
		if key in self.jobs:
			del self.jobs[ key ]
	
	def run( self ):
		while True:
			for (key,job) in self.jobs.items():
				if self.clock % job[ 0 ] == 0:
					async_job = AsyncJob( job[ 1 ], job[ 2 ] )
					async_job.setDaemon( True )
					async_job.start()
			
			time.sleep( 1.0 )
			self.clock += 1

