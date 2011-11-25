#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'main' )

class MemDB( object ):
	def __init__( self, snake ):
		self._get = snake.get_method( 'get' )
		self._set = snake.get_method( 'set' )
		self._find = snake.get_method( 'find' )
		self._keys = snake.get_method( 'get_keys' )
	
	def get( self, key ):
		R = self._get( key = key )
		print R
		return R['result']
	
	def set( self, key, value ):
		R = self._set( key = key, value = value )
		
	def find( self, path, value ):
		R = self._find( path = path, value = value } )
		return R['result']

	def get_keys( self ):
		R = self._keys()
		return R['result']


def create_record( username, street, city, state ):
	out = {}
	out['username'] = username
	out['address'] = {}
	out['address']['street'] = street
	out['address']['city'] = city
	out['address']['state'] = state
	return out


def create_record2( a, b, c ):
	out = { 'a': a, 'b':b, 'c': c }
	return out

memdb = MemDB( client )


entry1 = create_record( "bob", "123 Main Street", "Springfield", "NY" )
entry2 = create_record( "ejnar", "Saefellsvagen 4", "Hafnarfjordur", "RE" )
entry3 = create_record( "sigur", "Laugavegur", "Reykjavik", "RE" )

entry4 = create_record2( 1, 2, 3 )


memdb.set( 'record_0001', entry1 )
memdb.set( 'record_0002', entry2 )
memdb.set( 'record_0003', entry3 )
memdb.set( 'record_0004', entry4 )


pprint.pprint( memdb.find( 'address.state', 'RE' ) )
pprint.pprint( memdb.find( 'a', 1 ) )
