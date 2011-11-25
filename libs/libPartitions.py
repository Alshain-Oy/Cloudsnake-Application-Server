#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy


import threading, hashlib, random, time, copy

import libCloudSnakeClient as SnakeClient


class PartitionTable( object ):
	def __init__( self ):
		self.mapping = {}
		self.snakes = {}
		
	
	def add_key( self, key, uri, user ):
		self.mapping[ key ] = uri
		if uri not in self.snakes:
			self.snakes[ uri ] = SnakeClient.CloudSnakeClient( uri, user )
	
	def get_key( self, key ):
		if key not in self.mapping:
			return None
		else:
			return self.mapping[ key ]
	
	def remove_key( self, key ):
		if key in self.mapping:
			del self.mapping[ key ]
			
	def get_snake_client( self, uri ):
		if uri in self.snakes:
			return self.snakes[ uri ]
		return None
	
	def get_keys():
		return self.mapping.keys()
	



class PartitionedMemDBWrapper( object ):
	def __init__( self, db, table ):
		self.db = db
		self.table = table
	
	
	def set( self, key, value ):
		uri = self.table.get_key( key )
		if not uri:
			self.db.set( key, value )
		else:
			client = self.table.get_snake_client( uri )
			if client:
				client.call_method( 'partition_set', {'key': key, 'value': value} )
	
	def get( self, key ):
		uri = self.table.get_key( key )
		value = None
		if not uri:
			self.db.get( key )
		else:
			client = self.table.get_snake_client( uri )
			if client:
				value = client.call_method( 'partition_get', {'key': key} )
		return value
	
	def get_keys():
		keys = self.db.get_keys()
		keys.extend( self.table.get_keys() )
		return list( set( keys ) )

class PartitionedContext( object ):
	def __init__( self, db, table ):
		self.db = db
		self.table = table
	
	def __enter__( self ):
		return PartitionedMemDBWrapper( self.db, self.table )
	
	def __exit__( self, _type, value, traceback ):
		if not _type:
			return True
		else:
			return False


