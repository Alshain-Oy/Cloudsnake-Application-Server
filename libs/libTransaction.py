#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy


import threading, hashlib, random, time, copy

class TransactionLog( object ):
	def __init__( self ):
		self.keys = set()
		self.values = {}
	
	def add( self, key ):
		self.keys.add( key )
	
	def attach_value( self, key, value ):
		self.values[ key ] = copy.deepcopy( value )
	
	def dump( self ):
		return list( self.keys )




class TransactionLocker( object ):
	def __init__( self ):
		self.affected_keys = set()
		self.lock = threading.Lock()
	
	def reserve_keys( self, keys ):
		out = True
		with self.lock:
			test = [ x not in self.affected_keys for x in keys ]
			if not all( test ):
				out = False
			else:
				for k in keys:
					self.affected_keys.add( k )
		return out
	
	def release_keys( self, keys ):
		with self.lock:
			for k in keys:
				self.affected_keys.discard( k )
	
	def check_keys( self, keys ):
		with self.lock:
			out =  all( [ x in self.affected_keys for x in keys ] )
		return out

class memdb_wrapper( object ):
	def __init__( self, db ):
		self.db = db
		
		self.klog = TransactionLog()
	
	def get( self, key ):
		if key not in self.klog.keys:
			self.klog.add( key )
			self.klog.attach_value( key, self.db.get( key ) )
		else:
			self.klog.add( key )
		return self.db.get( key )
	
	def set( self, key, value ):
		self.klog.add( key )
		self.klog.attach_value( key, value )
		self.db.set( key, value )
	
	def get_keys( self ):
		return self.db.get_keys()
	


class TransactionContext( object ):
	def __init__( self, db, peers, locker ):
		self.db = memdb_wrapper( db )
		self.peers = peers#set( peers )
		self.locker = locker
	
	def add_peer( self, peer ):
		self.peers.add( peer )
		
	def remove_peer( self, peer ):
		self.peers.discard( peer )
	
	def __enter__( self ):
		return self.db
	
	def __exit__( self, _type, value, traceback ):
		
		keys = self.db.klog.dump()
		
		if not self.locker.reserve_keys( keys ):
			return False
		
		payload = self.db.klog.values
		
		
		trans_id = hashlib.sha1( str( time.time() ) + ':' + str( random.random() ) ).hexdigest()
		
		votes = []
		for (key,peer) in self.peers.items():
			votes.append( peer.transaction_query_to_commit( trans_id, payload ) )
		
		if not all( votes ):
			for (key,peer) in self.peers.items():
				peer.transaction_rollback( trans_id )
			self.locker.release_keys( keys )
			return False
		
		for (key,peer) in self.peers.items():
			peer.transaction_commit( trans_id )
		
		for (key, value) in payload.items():
			self.db.db.set( key, value )
		
		
		self.locker.release_keys( keys )
		return True


class TransactionHandler( object ):
	def __init__( self, db, locker ):
		self.db = db
		self.commit_log = {}
		self.trans_locker = locker
		
	
	def query_to_commit( self, trans_id, payload ):
		keys = payload.keys()
		if not self.trans_locker.reserve_keys( keys ):
			return False
		
		self.commit_log[ trans_id ] = payload
		
		return True
	
	def rollback( self, trans_id ):
		keys = self.commit_log[ trans_id ].keys()
		self.trans_locker.release_keys( keys )
		del self.commit_log[ trans_id ]
		return True
	
	def commit( self, trans_id ):
		keys = self.commit_log[ trans_id ]
		for (key, value) in self.commit_log[ trans_id ].items():
			self.db.set( key, value )
		
		self.trans_locker.release_keys( keys )
		return True

