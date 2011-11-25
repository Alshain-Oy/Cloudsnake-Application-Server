
# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

# cloudsnake hash ring

# remember to insert libHashRing_caps.py also


def init():
	cloudSnake.memdb.set( "ring", cloudSnake.call( "HashRing", {'replicas': 3} ) )

def add_node( node ):
	return cloudSnake.memdb.get( "ring" ).add_node( node )

def remove_node( node ):
	return cloudSnake.memdb.get( "ring" ).remove_node( node )

def get_node( key ):
	return cloudSnake.memdb.get( "ring" ).get_node( key )
