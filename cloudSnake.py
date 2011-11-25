#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy


import threading

import json

import urllib

import time

import sys

import os

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

sys.path.append( os.path.abspath( os.path.dirname( sys.argv[ 0 ] ) ) )

import libs.libArtifact as libArtifact, libs.libCloudSnake as libCloudSnake, libs.libMaintenance as libMaintenance, libs.libLogger as libLogger


cloudsnake = libCloudSnake.CloudSnake()

janitor = libMaintenance.Janitor()

stream_stdout = libLogger.OutputConsole()
stream_stderr = libLogger.OutputConsole()

janitor.attach_stream( 'stdout', stream_stdout )
janitor.attach_stream( 'stderr', stream_stderr )




def parse_http_args( txt ):
	data = ""
	if '?' in txt:
		(tmp,data) = txt.split( '?', 1 )
	else:
		data = txt
	
	pairs = data.split( '&' )
	out = {}
	for pair in pairs:
		if '=' in pair:
			(k,v) = pair.split( '=', 1 )
			out[ k.strip() ] = v.strip()
		else:
			out[ pair ] = True
	return out


class Handler( BaseHTTPRequestHandler ):
	def get_headers( self ):
		out = {}
		for key in self.headers:
			out[ key ] = self.headers[ key ]
		return out
	
	def do_GET( self ):
		self.send_response( 200 )
		self.end_headers()
		
		self.wfile.write( "Ok.\r\n" )
	
	def do_POST( self ):
		global cloudsnake, janitor
		janitor.mark_new_request()

		#sys.stdout = janitor.streams['stdout']
		#sys.stderr = janitor.streams['stderr']


		
		self.send_response( 200 )
		self.send_header( 'Content-Type', 'application/json' )
		self.end_headers()
		GET_vars = parse_http_args( self.path )
		headers = self.get_headers()
		L = headers[ 'content-length' ]
		
		raw_payload = self.rfile.read( int( L ) )
		payload = urllib.unquote_plus( raw_payload )
		rpc = json.loads( payload  )
		
		user = GET_vars[ 'user' ]

		print 'Method:', rpc['method']
		
		jsonrpc_version = 1
		if 'jsonrpc' in rpc:
			jsonrpc_version = 2
		
		A = cloudsnake.get_artifact( user, rpc[ 'method' ] )
		
		if A:
			try:
				result = A( rpc[ 'params' ] )
				if jsonrpc_version > 1:
					rpc_response = {'jsonrpc':"2.0", "id":rpc[ 'id' ], 'result':result }
				else:
					rpc_response = { "id":rpc[ 'id' ], 'result':result, 'error': None }
			except:
				info = sys.exc_info()
				error = "%s: %s"%( str( info[ 0 ] ), str( info[ 1 ] )  )
				if jsonrpc_version > 1:
					rpc_response = {'jsonrpc':"2.0", "id":rpc[ 'id' ], 'error': error }
				else:
					rpc_response = { "id":rpc[ 'id' ], 'result':None, 'error': error }
	
		else:
			if jsonrpc_version > 1:
				rpc_response = {'jsonrpc':"2.0", "id":rpc[ 'id' ], 'error':'No such method.' }
			else:
				rpc_response = { "id":rpc[ 'id' ], 'result':None, 'error': 'No such method.' }
		
		jresponse = json.dumps( rpc_response )
		self.wfile.write( jresponse )
		#print "Threaded ended."



class ThreadedServer( ThreadingMixIn, HTTPServer ):
	""" Threaded HTTP server """

def get_janitor_report( J ):
	def report():
		return J.report()
	return report

def get_janitor_stream( J ):
	def get_stream( name ):
		return J.get_stream_content( name )
	return get_stream

def server_shutdown( snake ):
	#raise KeyboardInterrupt
	def shutdown():
		snake.done = True
	return shutdown

def list_user_artifacts( db, user ):
	def list_artifacts():
		return db.db.db[ user ].keys()
	return list_artifacts

if __name__ == '__main__':
	
	
	cloudsnake.add_user( 'main' )
	cloudsnake.add_user( 'maintenance' )
	
	cloudsnake.attach_method( 'maintenance', 'report', get_janitor_report( janitor ) )
	cloudsnake.attach_method( 'maintenance', 'shutdown', server_shutdown( cloudsnake ) )
	cloudsnake.attach_method( 'maintenance', 'get_stream', get_janitor_stream( janitor ) )
	
	cloudsnake.attach_method( 'main', 'list_artifacts', list_user_artifacts( cloudsnake, 'main' ) )
	cloudsnake.attach_method( 'maintenance', 'list_artifacts', list_user_artifacts( cloudsnake, 'maintenance' ) )
	
	port = 8500
	if len( sys.argv ) > 1:
		port = int( sys.argv[ 1 ] )
	server = ThreadedServer( ('', port ), Handler )
	
	server_thread = threading.Thread( target = server.serve_forever )
	server_thread.setDaemon( True )
	server_thread.start()

	print "Server started."
	
	#sys.stdout = stream_stdout
	#sys.stderr = stream_stderr

	
	while not cloudsnake.done:
		time.sleep( 1.0 )
	
	server.shutdown()
	

