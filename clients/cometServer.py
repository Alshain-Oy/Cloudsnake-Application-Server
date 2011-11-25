#!/usr/bin/env python


import socket, json, urllib, time


import threading

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn


class AsyncJob( threading.Thread ):
	def __init__( self, sock ):
		threading.Thread.__init__( self )
		self.sock = sock
	
	def run( self ):
		global cometEvents
		
		data = ""
		while '\r\n\r\n' not in data:
			data += self.sock.recv( 1024 )
		
		lines = data.splitlines()
		
		#print lines
		
		parts = lines[ 0 ].split()
		path = parts[ 1 ]
		if path.startswith( 'http' ):
			tmp = path.split( '/' )
			path = '/' + tmp[ -1 ]
		
		path = path[1:]
		
		if len( path ) < 1 or path == 'favicon.ico':
			self.sock.close()
			return
		
		
		cometEvents.add_to_event( path, self.sock )
		

class AsyncResponder( threading.Thread ):
	def __init__( self, socks, data, done_event ):
		threading.Thread.__init__( self )
		self.socks = socks
		self.data = data
		self.done = done_event
	
	def run( self ):
		for sock in self.socks:
			try:
				sock.send( self.data )
			except:
				pass
			sock.close()
		
		self.done.set()
		


class EventHandler( object ):
	def __init__( self ):
		self.events = {}
		
	
	def trigger( self, event, content ):
		if event in self.events:
			#payload = urllib.quote_plus( json.dumps( content ) )
			payload = json.dumps( content )
			L = len( payload )
			response = ""
			response += "HTTP/1.1 200 OK\r\n"
			response += "Date: %s\r\n" % time.strftime( "%a, %d %b %Y %H:%M:%S GMT", time.gmtime() )
			response += "Content-Length: %i\r\n"%L
			response += "Content-Type: application/json\r\n"
			response += "Connection: close\r\n"
			response += "\r\n"
			response += payload
			
			
			t0 = time.clock()
			n = 0
			#for sock in self.events[ event ]:
			#	#print "Responding..."
			#	sock.send( response )
			#	sock.close()
			#	n += 1
			dones = []
			for i in range( 0, len( self.events[ event ] ), 200 ):
				socks = self.events[ event ][ i : i + 200 ]
				E = threading.Event()
				dones.append( E )
				J = AsyncResponder( socks, response, E )
				J.setDaemon( True )
				J.start()
			
			are_done = [ x.is_set() for x in dones ]
			while not all( are_done ):
				#time.sleep( 0.1 )
				are_done = [ x.is_set() for x in dones ]
			
			n = len( self.events[ event ] )
			del self.events[ event ]
			t1 = time.clock()
			
			print "It took %.2f secs to respond %i clients..."%( t1-t0, n )
			
	def add_to_event( self, event, sock ):
		print "Registering subscriber to event '%s'"%event
		if event not in self.events:
			self.events[ event ] = [ sock ]
		else:
			self.events[ event ].append( sock )
			



cometEvents = EventHandler()



class ThreadedServer( ThreadingMixIn, HTTPServer ):
	""" Threaded HTTP server """


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
	
	def do_POST( self ):
		global cometEvents
		
		self.send_response( 200 )
		self.end_headers()
		headers = self.get_headers()
		L = headers[ 'content-length' ]
		
		raw_payload = self.rfile.read( int( L ) )
		payload = urllib.unquote_plus( raw_payload )
		rpc = json.loads( payload )
		
		params = rpc[ 'params' ]
		
		#print params
		
		event = None
		content = None
		
		if type( params ) == dict:
			event = params['event']
			content = params[ 'content' ]
		elif type( params ) == list:
			event = params[ 0 ]
			content = params[ 1 ]
		
		
		if event and content:
			cometEvents.trigger( event, content )
		
		rpc_response = {'jsonrpc':"2.0", "id":rpc[ 'id' ], 'result':True }
		
		self.wfile.write( json.dumps( rpc_response ) )



server_done = False

if __name__ == '__main__':
	
	server = ThreadedServer( ('', 8101 ), Handler )
	server_thread = threading.Thread( target = server.serve_forever )
	server_thread.setDaemon( True )
	server_thread.start()
	print "JSON-RPC interface started."
	
	
	serversocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	serversocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
	serversocket.bind( ('', 8100 ) )
	serversocket.listen( 5 )
	print "Waiting for connections..."
	try:
		while not server_done:
			( client, addr ) = serversocket.accept()
			print "Connection from", addr
			AsyncJob( client ).start()
			
			
	except KeyboardInterrupt:
		pass
	
	serversocket.close()
