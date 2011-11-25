#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import json, urllib, urllib2

class CloudSnakeClient( object ):
	def __init__( self, url, user ):
		self.url = url
		self.user = user
		self.n_id = 1
	
	def call_method( self, method, params ):
		data = {'jsonrpc':"2.0", 'method':method, 'params':params, 'id':self.n_id }
		url = self.url + "/api?user=" + self.user
		#print data
		jstr = json.dumps( data )
		#query = urllib.urlencode( { 'q':unicode( jstr ) } )
		query = urllib.quote_plus( jstr )
		handle = urllib2.urlopen( url, query )
		result = handle.read()
		#print "result:",result
		handle.close()
		self.n_id += 1

		return json.loads( result )

	def get_method( self, method ):
		def client_method( *args, **kwargs ):
			if len( args ) > 0:
				return self.call_method( method, args )
			if len( kwargs ) > 0:
				return self.call_method( method, kwargs )
			return self.call_method( method, [] )
		return client_method

	def get_output( self ):
		result = self.call_method( 'get_output', [] )
		out = result[ 'result' ]
		return out
	
	def print_output( self ):
		lines = self.get_output()
		for line in lines:
			print line[ 0 ], line[ 1 ]


class CloudSnakeException( Exception ):
	def __init__( self, value ):
		self.value = value
	def __str__( self ):
		return repr( self.value )

class CloudSnakeMapper( object ):

	def _method_wrapper( self, method ):
		def cloudsnake_method( *args, **kwargs ):
			if len( args ) > 0:
				response = method( *args )
				if 'error' in response:
					raise CloudSnakeException( response['error'] )
				else:
					return response['result']
			elif len( kwargs ) > 0:
				response = method( **kwargs )
				if 'error' in response:
					raise CloudSnakeException( response['error'] )
				else:
					return response['result']
			else:
				response = method()
				if 'error' in response:
					raise CloudSnakeException( response['error'] )
				else:
					return response['result']
		return cloudsnake_method
		
	def __init__( self, client ):
		methods = client.get_method( 'list_artifacts' )()['result']
		
		for method in methods:
			self.__dict__[ method ] = self._method_wrapper( client.get_method( method ) )

	def refresh_methods( self ):
		methods = client.get_method( 'list_artifacts' )()['result']
		
		for method in methods:
			self.__dict__[ method ] = self._method_wrapper( client.get_method( method ) )
		
