#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy


import threading, hashlib, time, random

class JobQueue( threading.Thread ):
	def __init__( self ):
		threading.Thread.__init__( self )
		self.results = {}
		self.jobs = {}
		self.queue = []
		self.done = False
	
	def generate_key( self ):
		return hashlib.md5( str( time.time() ) + ":" + str( random.random() ) ).hexdigest()
	
	def shutdown( self ):
		self.done = True
	
	def add_job( self, method, params ):
		key = self.generate_key()
		self.jobs[ key ] = ( method, params )
		self.queue.append( key )
		return key
	
	def has_results( self, key ):
		return key in self.results.keys()
	
	def get_results( self, key ):
		if self.has_results( key ):
			result = self.results[ key ]
			del self.results[ key ]
			del self.jobs[ key ]
			return result
		else:
			return None
	
	def run( self ):
		while not self.done:
			#print self.queue
			if len( self.queue ) > 0:
				job_key = self.queue.pop()
				job = self.jobs[ job_key ]
				self.results[ job_key ] = job[ 0 ]( job[ 1 ] ) #self.jobs( self.jobs[ job_ke method( params ) )
			else:
				time.sleep( 1.0 )
	
	
		

		


 
