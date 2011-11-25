# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy


def init():
	cloudSnake.memdb.set( 'counter', 0 )


def increase():
	N = cloudSnake.memdb.get( 'counter' )
	cloudSnake.memdb.set( 'counter', N + 1 )


def get_counter():
	return cloudSnake.memdb.get( 'counter' )
