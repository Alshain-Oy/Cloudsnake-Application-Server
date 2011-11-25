#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import json
import threading

class Artifact( object ):
	def __init__( self, name, method, single = False ):
		self.name = name
		self.method = method
		self.single = single
		self.lock = threading.Lock()
		
	
	def __call__( self, params ):
		#print "Calling artifact '%s'"%self.name
		results = None
		if self.single:
			self.lock.acquire()
		#print "params:", params
		try:
			if type( params ) == list:
				results = self.method( *params )
			elif type( params ) == dict:
				results = self.method( **params )
		except Exception, e:
			if self.single:
				self.lock.release()
			raise e
		if self.single:
			self.lock.release()
		
		return results

	def set_single( self, value ):
		self.lock.acquire()
		self.single = value
		self.lock.release()
	






		
