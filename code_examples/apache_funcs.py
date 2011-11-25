#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy


def apache_init():
	cloudSnake.memdb.set( 'apache_users', {} )
	cloudSnake.memdb.set( 'apache_groups', {} )
	return True

def apache_add_user( user, pwhash ):
	cloudSnake.memdb.get( 'apache_users' )[ user ] = pwhash
	return True

def apache_add_group( group, members ):
	cloudSnake.memdb.get( 'apache_groups' )[ group ] = set( members )
	return True

def apache_add_to_group( group, user ):
	cloudSnake.memdb.get( 'apache_groups' )[ group ].add( user )
	return True

def apache_remove_from_group( group, user ):
	cloudSnake.memdb.get( 'apache_groups' )[ group ].discard( user )
	return True

def apache_remove_group( group ):
	if group in cloudSnake.memdb.get( 'apache_groups' ):
		del cloudSnake.memdb.get( 'apache_groups' )[ group ]
		return True
	return False


def apache_get_groups():
	return cloudSnake.memdb.get( 'apache_groups' ).keys()

def apache_get_content( group ):
	if group not in cloudSnake.memdb.get( 'apache_groups' ):
		return None
	
	users = cloudSnake.memdb.get( 'apache_groups' )[ group ]
	out = ""
	for user in users:
		pw = cloudSnake.memdb.get( 'apache_users' )[ user ]
		
		out += "%s:{SHA}%s\n"%( user, pw )
	
	return out
	


