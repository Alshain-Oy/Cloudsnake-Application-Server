#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy


def get_value( key ):
	out = None
	with cloudSnake.Partitions as db:
		out = db.get( key )
	return out

def set_value( key, value ):
	with cloudSnake.Partitions as db:
		db.set( key, value )
