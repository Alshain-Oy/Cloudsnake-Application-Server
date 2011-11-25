
# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy


def init():
	conn = cloudSnake.modules.postgres.connect( "dbname=timers user=caps host=localhost password=mursu123" )
	cloudSnake.memdb.set( "postgres_connection", conn )


def create_user( user, pw ):
	ts = cloudSnake.modules.time.strftime( "%Y-%m-%d %H:%M:%S" )
	
	pwhash = cloudSnake.modules.hashlib.sha1( pw ).hexdigest()
	
	cursor = cloudSnake.memdb.get( 'postgres_connection' ).cursor()
	cursor.execute( "INSERT INTO users (name, pwhash, created) VALUES( %s, %s, %s )", [ user, pwhash, ts ] )
	
	cloudSnake.memdb.get( 'postgres_connection' ).commit()
	


def get_auth_token( user, pwhash ):
	cursor = cloudSnake.memdb.get( 'postgres_connection' ).cursor()
	cursor.execute( "SELECT * FROM users WHERE name=%s", [user] )
	
	results = cursor.fetchone()
	
	if results:
		
		auth_token = cloudSnake.modules.hashlib.sha1( pwhash + ":" + str( cloudSnake.modules.time.time() ) ).hexdigest()
		
		ts = cloudSnake.modules.time.strftime( "%Y-%m-%d %H:%M:%S" )
		
		cursor.execute( "INSERT INTO auth_tokens (owner, token, created) VALUES (%s,%s,%s)", [ user, auth_token, ts ] )
		
		cloudSnake.memdb.get( 'postgres_connection' ).commit()
		return auth_token
	
	
	
	else:
		return False
	


def check_auth_token( user, token ):
	cursor = cloudSnake.memdb.get( 'postgres_connection' ).cursor()
	cursor.execute( "SELECT * FROM auth_tokens WHERE owner=%s AND token=%s", [user, token] )
	results = cursor.fetchone()
	
	if results:
		return 1
	else:
		return 0


def add_timer( user, token, timer_name, timer_time ):
	
	if not cloudSnake.call( 'check_auth_token', {'user':user, 'token': token } ):
		return False
	
	cursor = cloudSnake.memdb.get( 'postgres_connection' ).cursor()
	ts = cloudSnake.modules.time.strftime( "%Y-%m-%d %H:%M:%S" )
	idhash = cloudSnake.modules.hashlib.sha1( ts + ":" + user ).hexdigest()
	
	cursor.execute( "INSERT INTO timers (owner, name, target, created, hash ) VALUES ( %s, %s, %s, %s, %s )", [ user, timer_name, timer_time, ts, idhash ] )
	
	cloudSnake.memdb.get( 'postgres_connection' ).commit()
	
	return idhash

def get_timers( user, token ):
	out = []
	if not cloudSnake.call( 'check_auth_token', {'user':user, 'token': token } ):
		return False
	
	cursor = cloudSnake.memdb.get( 'postgres_connection' ).cursor()
	ts = cloudSnake.modules.time.strftime( "%Y-%m-%d %H:%M:%S" )
	
	cursor.execute( "SELECT name, target, created, hash FROM timers WHERE owner=%s AND target > %s ", [user, ts ] )
	
	results = cursor.fetchall()

	for row in results:
		out.append( {'name': row[ 0 ], 'target': str(row[ 1 ]), 'created': str(row[ 2 ]), 'hash': row[ 3 ] } )
		
	return out

def remove_timer( user, token, idhash ):
	if not cloudSnake.call( 'check_auth_token', {'user':user, 'token': token } ):
		return False
	
	cursor.execute( "DELETE FROM timers WHERE owner=%s AND hash=%s", [user, idhash] )
	
	cursor.execute()
	
	cloudSnake.memdb.get( 'postgres_connection' ).commit()
	
	return True
	
