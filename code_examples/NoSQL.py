
# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

def get( key ):
	return cloudSnake.memdb.get( key )

def set( key, value ):
	cloudSnake.memdb.set( key, value )
	

def find( path, value ):
	keys = cloudSnake.memdb.get_keys()
	
	parts = path.split( '.' )
	out = []
	
	for key in keys:
		tmp = cloudSnake.memdb.get( key )
		for part in parts:
			if part in tmp:
				tmp = tmp[ part ]
			else:
				tmp = None
				break
		if tmp:
			if tmp == value:
				out.append( cloudSnake.memdb.get( key ) )
	return out

def get_keys():
	return cloudSnake.memdb.get_keys()


