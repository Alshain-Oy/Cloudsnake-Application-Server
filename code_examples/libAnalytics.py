#!/usr/bin/env python


# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy


def init_analytics():
	cloudSnake.memdb.set( '_cloudsnake-analytics', True )
	cloudSnake.memdb.set( '_cloudsnake-analytics_log', [] )
	cloudSnake.memdb.set( '_cloudsnake-analytics_visitors', {} )


def generate_tracking_cookie( cookies ):
	if 'cloudsnake-analytics' in cookies:
		if str( cookies[ 'cloudsnake-analytics' ] ) != 'None':
			print "returgin..."
			return cookies[ 'cloudsnake-analytics' ]
	
	return cloudSnake.modules.hashlib.sha1( str( cloudSnake.modules.time.time() ) + ":" + str( cloudSnake.modules.random.random() ) ).hexdigest()

def apply_analytics( path, headers, client, cookies ):
	ts = cloudSnake.modules.time.strftime( "%Y-%m-%d %H:%M:%S" )
	
	
	entry = {}
	entry[ 'tracking_id' ] = cookies['cloudsnake-analytics']
	entry['timestamp'] = ts
	entry['path'] = path
	entry['referer'] = ""
	if 'referer' in headers:
		entry[ 'referer' ] = headers['referer']
	cloudSnake.memdb.get( '_cloudsnake-analytics_log' ).append( entry )

	entry = {}
	entry[ 'user_agent' ] = headers['user-agent']
	entry[ 'lang' ] = headers['accept-language']
	entry[ 'address' ] = client
	entry['timestamp'] = ts
	cloudSnake.memdb.get( '_cloudsnake-analytics_visitors' )[ cookies['cloudsnake-analytics'] ] = entry

	
	


def dump_analytics():
	visitors = cloudSnake.memdb.get( '_cloudsnake-analytics_visitors' )
	log = cloudSnake.memdb.get( '_cloudsnake-analytics_log' )
	return {'visitors': visitors, 'log': log }

def clear_analytics():
	cloudSnake.memdb.set( '_cloudsnake-analytics_log', [] )
	cloudSnake.memdb.set( '_cloudsnake-analytics_visitors', {} )
