#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import os, time
import threading


try:
	import resource
except ImportError:
	pass
	


class Janitor( object ):
	def __init__( self ):
		self.started = time.time()
		self.n_requests = 0
		self.streams = {}
	
	
	def mark_new_request( self ):
		self.n_requests += 1

	def report( self ):
		out = {}
		out['requests'] = self.n_requests
		out['time'] = time.time() - self.started
		out['threads'] = threading.active_count()
		
		
		
		try:
			res = resource.getrusage( resource.RUSAGE_SELF )
			out['memory'] = res[ 2 ] * resource.getpagesize() / ( 1024.0 * 1024.0 ) 
		except:
			out['memory'] = 0
		
		return out

	def attach_stream( self, name, stream ):
		self.streams[ name ] = stream
	
	def get_stream_content( self, name ):
		if name in self.streams:
			return self.streams[ name ].get_output()
		return None 
