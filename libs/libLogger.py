#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import time, threading

import libBuffer

class OutputConsole( object ):
	def __init__( self ):
		self.lines = libBuffer.DataBuffer( 1024, "" )
	
	def log( self, line ):
		self.lines.push( line )
	
	def get_output( self ):
		return self.lines.get_entries( 32 )


	def write( self, data ):
		data = data.strip()
		
		if len( data ) < 1:
			return None
		
		if '\n' in data:
			lines = data.splitlines()
			for line in lines:
				self.lines.push( ( time.strftime( "[%Y-%m-%d %H:%M:%S]") , line ) )
		else:
			self.lines.push( ( time.strftime( "[%Y-%m-%d %H:%M:%S]") , data ) )

