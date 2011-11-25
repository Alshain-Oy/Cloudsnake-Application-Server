#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, hashlib, getpass


class TimerDB( object ):
	def __init__( self, user = "" ):
		self.user = user
		self.token = ""
		client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'main' )

		self._create_user = client.get_method( 'create_user' )
		self._init = client.get_method( 'init' )
		self._get_auth_token = client.get_method( 'get_auth_token' )
		self._add_timer = client.get_method( 'add_timer' )
		self._remove_timer = client.get_method( 'remove_timer' )
		self._get_timers = client.get_method( 'get_timers' )
	
	def init( self ):
		R = self._init( [] )
	
	def create_user( self, user, pw ):
		R = self._create_user( user = user, pw = pw  )
	
	def authenticate( self ):
		if len( self.token ) < 1:
			pw = getpass.getpass()
			pwhash = hashlib.sha1( pw ).hexdigest()
			R = self._get_auth_token( user = self.user, pwhash = pwhash )
			if R['result']:
				self.token = R['result']
				return True
			return False
	
	def load_token( self, fn ):
		txt = ""
		with open( fn, 'r' ) as handle:
			txt = handle.read()
		self.token = txt
	
	def save_token( self, fn ):
		with open( fn, 'w' ) as handle:
			handle.write( self.token )
	
	def add_timer( self, name, target ):
		R = self._add_timer( user = self.user, token = self.token, timer_name = name, timer_time = target )
		return R['result']
	
	def get_timers( self ):
		R = self._get_timers( user = self.user, token = self.token )
		return R['result']
	
	def remove_timer( self, timer_hash ):
		R = Self._remove_timer( user = self.user, token = self.token, idhash = timer_hash )
		return R['result']


