#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

from collections import deque
import threading

class DataBuffer( object ):
	def __init__( self, N, default_value = None ):
		self.buf = deque()
		self.N = N
		self.lock = threading.Lock()
		self.default_value = default_value


	def push( self, value ):
		self.lock.acquire()
		
		self.buf.append( value )
		if len( self.buf ) > self.N:
			self.buf.popleft()
		
		self.lock.release()
	
	def pop( self ):
		self.lock.acquire()
		
		out = self.defaul_value
		
		if len( self.buf ) > 1:
			out = self.buf.popleft()
		
		self.lock.release()
		
		return out

	def get_entries( self, N ):
		out = []
		p = min( N, self.N )
		p = min( p, len( self.buf ) )
		
		self.lock.acquire()
		
		for i in range( p ):
			out.append( self.buf[ i ] )
		
		self.lock.release()
		
		return out
