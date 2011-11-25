#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import threading

import json

import urllib

import time

import sys

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

import libCloudSnakeClient as SnakeClient

snakeClient = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'main' )

class Handler( BaseHTTPRequestHandler ):

	def get_headers( self ):
		out = {}
		for key in self.headers:
			out[ key ] = self.headers[ key ]
		return out
	
	def do_GET( self ):
		global snakeClient 
		
		#self.wfile.write( "Ok.\r\n" )
		headers = self.get_headers()
		path = self.path
		request = {'headers': headers, 'path': path, 'client': self.client_address[ 0 ] }
		
		response = snakeClient.get_method( 'handle_get')( request = request )
		
		if 'error' not in response:
			self.send_response( 200 )
			
			for line in response['result']['headers']:
				print "Sending header: ", line
				self.send_header( line[ 0 ], line[ 1 ] )
			
			self.end_headers()
			
			self.wfile.write( response['result']['body'] )
		else:
			self.send_response( 500 )
			self.end_headers()
			self.wfile.write( response['error'] )
		
		
		
	
	
	def do_POST( self ):
		global snakeClient
		self.send_response( 200 )
		self.end_headers()
		
		headers = self.get_headers()
		L = headers[ 'content-length' ]
		raw_payload = self.rfile.read( int( L ) )
		payload = urllib.unquote_plus( raw_payload )
		
		request = { 'headers': headers, 'body': payload, 'path': self.path, 'client': self.client_address[ 0 ]  }
		
		response = snakeClient.get_method( 'handle_post' )( request = request )
		
		if 'error' not in response:
			self.send_response( 200 )

			for line in response['result']['headers']:
				self.send_header( line[ 0 ], line[ 1 ] )

			self.end_headers()

			self.wfile.write( response['result']['body'] )
		else:
			self.send_response( 500 )
			self.end_headers()
			self.wfile.write( response['error'] )
		
		
		
	def do_HEAD( self ):
		global snakeClient
		self.send_response( 200 )
		self.end_headers()
		
		headers = self.get_headers()
		request = { 'headers': headers, 'path': self.path, 'client': self.client_address[ 0 ]  }
		
		response = snakeClient.get_method( 'handle_head' )( request = request )
		
		if 'error' not in response:
			self.send_response( 200 )
			self.end_headers()
		else:
			self.send_response( 500 )
			self.end_headers()


class ThreadedServer( ThreadingMixIn, HTTPServer ):
	""" Threaded HTTP server """

if __name__ == '__main__':
	done = False

	server = ThreadedServer( ('', 8501 ), Handler )
	
	server_thread = threading.Thread( target = server.serve_forever )
	server_thread.setDaemon( True )
	server_thread.start()

	print "Server started."
	
	while not done:
		time.sleep( 1.0 )
	server.shutdown()
