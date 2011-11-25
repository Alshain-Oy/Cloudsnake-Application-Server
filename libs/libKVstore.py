#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy



class KVStore( object ):
	def __init__( self ):
		self.db = {}
	
	def get( self, key ):
		if key in self.db:
			return self.db[ key ]
		else:
			return None
	
	def set( self, key, value ):
		self.db[ key ] = value

	def get_keys( self ):
		return self.db.keys()
