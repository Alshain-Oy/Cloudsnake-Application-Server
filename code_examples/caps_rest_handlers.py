
# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

def handle_head( request ):
	#return "HEAD."
	return { 'headers':[], 'body': "HEAD." }


def handle_get( request ):
	out = "GET '%s'"% cloudSnake.modules.urllib.unquote_plus( request['path'] )
	out += "\n"*3
	out += str( request['client'] )
	out += "\n"*3
	stream = cloudSnake.modules.StringIO.StringIO()
	cloudSnake.modules.pprint.pprint( cloudSnake.call( 'parse_url', {'url':request['path']} ) , stream )
	out += stream.getvalue()
	out += "\n"*3
	stream = cloudSnake.modules.StringIO.StringIO()
	cloudSnake.modules.pprint.pprint( request['headers'], stream )
	out += stream.getvalue()
	stream.close()
	#return out
	
	
	cookies = cloudSnake.call( 'parse_cookies', {'headers': request['headers'] } )
	headers = []
	
	if cloudSnake.memdb.get( '_cloudsnake-analytics' ):
		#print cookies
		if 'cloudsnake-analytics' not in cookies or str( cookies['cloudsnake-analytics'] ) == 'None':
			tracking_id = cloudSnake.call( 'generate_tracking_cookie', {'cookies': cookies} )
			#print "tracking_id", tracking_id
			headers.append( cloudSnake.call( 'generate_cookie', {'name': 'cloudsnake-analytics', 'value': tracking_id, 'domain': 'localhost', 'path': '/', 'expires': 365*24*3600, 'httponly': True, 'secure': False } ) )
			cookies['cloudsnake-analytics'] = tracking_id
			
		cloudSnake.call( 'apply_analytics', {'path': request['path'], 'headers': request['headers'], 'client': request['client'], 'cookies': cookies } )	
	
	return { 'headers': headers, 'body': out }



def handle_post( request ):
	#return "POST '%s'"% cloudSnake.modules.urllib.unquote_plus( request['path'] )
	return {'headers': [], 'body': "POST '%s'"% cloudSnake.modules.urllib.unquote_plus( request['path'] ) }



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


def parse_url( url ):
	parts = url.split( '/' )
	args = cloudSnake.call( 'parse_http_args', { 'txt': url  } )
	return {'parts': parts, 'args': args }


def parse_cookies( headers ):
	cookies = {}
	if 'cookie' in headers:
		parts = headers[ 'cookie' ].split( ';' )
		for part in parts:
			( key, value ) = part.split( '=' )
			cookies[ key.strip() ] = value.strip()
	return cookies

def generate_cookie( name, value, domain, path, expires, httponly, secure ):
	#ts = cloudSnake.modules.time.gmtime( cloudSnake.modules.time.time() + expires )
	#str_ts = cloudSnake.modules.time.strftime( "%"
	out = ""
	out = "%s=%s; Domain=%s; Path=%s; Max-Age=%i; " %( name, value, domain, path, expires )
	if secure:
		out += "Secure; "
	if httponly:
		out += "HttpOnly; "
	
	return ('Set-Cookie', out)

