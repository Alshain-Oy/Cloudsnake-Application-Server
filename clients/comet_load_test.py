#!/usr/bin/env python


import socket, json, urllib, time


import threading

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn


class AsyncJob( threading.Thread ):
	def __init__( self, url, done ):
		threading.Thread.__init__( self )
		self.url = url
		self.done = done
	
	def run( self ):
		
		handle = urllib.urlopen( self.url )
		out = handle.read()
		handle.close()
		#print out
		#print out
		
		self.done.set()







url = "http://localhost:8100/event1"


t = []

for i in range( 980 ):
	#AsyncJob( url ).run()
	E = threading.Event()
	j = AsyncJob( url, E )
	t.append( E )
	j.start()


are_done = [ x.is_set() for x in t ]

while not all( are_done ):
	time.sleep( 1 )
	are_done = [ x.is_set() for x in t ]

