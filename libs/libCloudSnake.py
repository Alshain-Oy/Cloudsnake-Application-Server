#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libArtifact
import json
import threading

import libLogger as Logger

#import math, urllib, urllib2

import libEval

import libKVstore

import libJobQueue

import libPeriodicJobs

import libTransaction

import libPartitions

import libCloudSnakeClient as SnakeClient


class ArtifactDB( object ):
	def __init__( self ):
		self.db = {}
		self.db_lock = threading.Lock()
		self.output = {}
		self.kvstore = {}
		self.jobQueue = {}
		self.periodicJobs = {}
		self.transaction_db = {}
		self.partition_table = {}
	
	
	def add_user( self, user ):
		self.db_lock.acquire()
		self.db[ user ] = {}
		self.output[ user ] = Logger.OutputConsole()
		self.kvstore[ user ] = libKVstore.KVStore()
		self.jobQueue[ user ] = libJobQueue.JobQueue()
		self.periodicJobs[ user ] = libPeriodicJobs.PeriodicJobs()
		
		self.jobQueue[ user ].setDaemon( True )
		self.jobQueue[ user ].start()
		
		self.periodicJobs[ user ].setDaemon( True )
		self.periodicJobs[ user ].start()
		
		self.transaction_db[ user ] = {}
		self.transaction_db[ user ][ 'L' ] = libTransaction.TransactionLocker()
		self.transaction_db[ user ][ 'H' ] = libTransaction.TransactionHandler( self.kvstore[ user ], self.transaction_db[ user ][ 'L' ] )
		self.transaction_db[ user ][ 'P' ] = set()
		self.transaction_db[ user ][ 'Pc' ] = {}
		
		self.partition_table[ user ] = libPartitions.PartitionTable()
		
		self.db_lock.release()
	
	def add_artifacts( self, user, artifacts ):
		self.db_lock.acquire()
		if user in self.db:
			for key in artifacts:
				self.db[ user ][ key ] = artifacts[ key ]
		self.db_lock.release()
	
	def get_artifact( self, user, name ):
		if user in self.db:
			if name in self.db[ user ]:
				return self.db[ user ][ name ]
		return None
	
	def get_console( self, user ):
		if user in self.output:
			return self.output[ user ]
		else:
			return None
	
	def get_kvstore( self, user ):
		if user in self.kvstore:
			return self.kvstore[ user ]
		else:
			return None


def artifact_adder_func( db, user ):
	def artifact_adder( code ):
		artifacts = code_to_artifacts( db, user, code )
		db.add_artifacts( user, artifacts )
		return True
	return artifact_adder


def internal_call_func( db, user ):
	def internal_call( method, params ):
		func = db.get_artifact( user, method )
		#return func( params )
		if func:
			return func( params )
		else:
			return None
	return internal_call


def internal_get_output_func( db, user ):
	def internal_get_output():
		output = db.get_console( user ).get_output()
		return output
	return internal_get_output
	
def internal_jobqueue_adder( db, user ):
	def jobQueue_adder( method, params ):
		func = db.get_artifact( user, method )
		return db.jobQueue[ user ].add_job( func, params )
	return jobQueue_adder

def internal_jobqueue_hasresults( db, user ):
	def jobQueue_hasresults( key ):
		return db.jobQueue[ user ].has_results( key )
	return jobQueue_hasresults

def internal_jobqueue_getresults( db, user ):
	def jobQueue_getresults( key ):
		return db.jobQueue[ user ].get_results( key )
	return jobQueue_getresults


def internal_periodicjobs_adder( db, user ):
	def periodicJobs_adder( interval, method, params ):
		func = db.get_artifact( user, method )
		return db.periodicJobs[ user ].add_job( interval, func, params )
	return periodicJobs_adder

def internal_periodicjobs_remove( db, user ):
	def periodicJobs_remove( key ):
		db.periodicJobs[ user ].remove_job( key )
	return periodicJobs_remove


def internal_transaction_query_to_commit( db, user ):
	def transaction_qtc( trans_id, payload ):
		return db.transaction_db[ user ][ 'H' ].query_to_commit( trans_id, payload )
	return transaction_qtc

def internal_transaction_rollback( db, user ):
	def transaction_rollback( trans_id ):
		return db.transaction_db[ user ][ 'H' ].rollback( trans_id )
	return transaction_rollback

def internal_transaction_commit( db, user ):
	def transaction_commit( trans_id ):
		return db.transaction_db[ user ][ 'H' ].commit( trans_id )
	return transaction_commit

def internal_transaction_add_peer( db, user ):
	def transaction_add_peer( peer ):
		db.transaction_db[ user ][ 'P' ].add( peer )
		
		client = SnakeClient.CloudSnakeClient( peer, 'main' )
		db.transaction_db[ user ][ 'Pc' ][ peer ] = SnakeClient.CloudSnakeMapper( client )
		
		return True
	return transaction_add_peer

def internal_transaction_remove_peer( db, user ):
	def transaction_remove_peer( peer ):
		db.transaction_db[ user ][ 'P' ].discard( peer )
		del db.transaction_db[ user ][ 'Pc' ][ peer ]
		return True
	return transaction_remove_peer

def internal_transaction_list_peers( db, user ):
	def transaction_list_peers():
		return list( db.transaction_dn[ user ][ 'P' ] )
	return transaction_list_peers

def internal_partition_set( db, user ):
	def partition_set( key, value ):
		db.kvstore[ user ].set( key, value )
	return partition_set

def internal_partition_get( db, user ):
	def partition_get( key ):
		return db.kvstore[ user ].get( key )
	return partition_get

def internal_partition_add_key( db, user ):
	def partition_add_key( key, uri, bucket ):
		db.partition_table[ user ].add_key( key, uri, bucket )
		return True
	return partition_add_key

def internal_partition_remove_key( db, user ):
	def partition_remove_key( key ):
		db.partition_table[ user ].remove_key( key )
		return True
	return partition_remove_key

def eval_code( db, user, code ):
	
	#cloudSnake = object()
	class cloudSnakeInternal( object ):
		pass
	cloudSnake = cloudSnakeInternal()
	cloudSnake.call = internal_call_func( db, user )
	cloudSnake.version = '0.0.1'
	cloudSnake.user = user
	cloudSnake.output = db.get_console( user )
	cloudSnake.modules = libEval.SandboxModules()
	cloudSnake.memdb = db.get_kvstore( user )
	
	cloudSnake.jobQueue = cloudSnakeInternal()
	cloudSnake.jobQueue.add_job = internal_jobqueue_adder( db, user )
	cloudSnake.jobQueue.has_results = internal_jobqueue_hasresults( db, user )
	cloudSnake.jobQueue.get_results = internal_jobqueue_getresults( db, user )
	
	cloudSnake.periodicJobs = cloudSnakeInternal()
	cloudSnake.periodicJobs.add_job = internal_periodicjobs_adder( db, user )
	cloudSnake.periodicJobs.remove_job = internal_periodicjobs_remove( db, user )
	cloudSnake.Transaction = libTransaction.TransactionContext( db.get_kvstore( user ), db.transaction_db[ user ][ 'Pc' ], db.transaction_db[ user ][ 'L' ] )
	
	cloudSnake.partitionManager = cloudSnakeInternal()
	cloudSnake.partitionManager.add_key = internal_partition_add_key( db, user )
	cloudSnake.partitionManager.remove_key = internal_partition_remove_key( db, user )
	cloudSnake.Partitions = libPartitions.PartitionedContext( db.get_kvstore( user ), db.partition_table[ user ] )
	
	
	
	eval_locals = { '__builtins__':{ 'abs':abs, 'all':all, 'int':int, 'float':float, 'filter':filter, 'hex': hex, 'bin':bin, 'isinstance':isinstance, 'map':map, 'max':max, 'min':min, 'str':str, 'sum':sum,'sorted':sorted,'repr':repr,'type':type, 'object':object, 'len':len, 'range':range, 'xrange': xrange, 'set':set, 'False':False, 'True': True, 'None': None, 'setattr':setattr, 'getattr':getattr  }, 'cloudSnake':cloudSnake, '__name__':'__cloudsnake__' }
	eval_globals = {'__builtins__':[]}
	not_included = ['__builtins__']
	
	eval( code, eval_locals, eval_globals )
	out = {}
	for z in eval_globals:
		if z not in not_included:
			out[ z ] = eval_globals[ z ]
	return out



def compile_code( db, user, txt ):
	#print "txt", txt
	code = compile( txt, '<string>'	, 'exec' )
	return eval_code( db, user, code )

def code_to_artifacts( db, user, code ):
	artifacts = compile_code( db, user, code )
	out = {}
	for key in artifacts:
		out[ key ] = libArtifact.Artifact( key, artifacts[ key ] )
	return out



class CloudSnake( object ):
	def __init__( self ):
		self.db = ArtifactDB()
		
		self.done = False
	
	def add_user( self, user ):
		self.db.add_user( user )
		
		self.db.add_artifacts( user, { 'add_artifact': libArtifact.Artifact( 'add_artifact', artifact_adder_func( self.db, user ), single = True ) } )
		self.db.add_artifacts( user, {'get_output': libArtifact.Artifact( 'get_output', internal_get_output_func( self.db, user ), single = True ) } )
		
		self.db.add_artifacts( user, {'queue_add_job': libArtifact.Artifact( 'queue_add_job', internal_jobqueue_adder( self.db, user ) ) } )
		self.db.add_artifacts( user, {'queue_has_results': libArtifact.Artifact( 'queue_has_results', internal_jobqueue_hasresults( self.db, user ) ) } )
		self.db.add_artifacts( user, {'queue_get_results': libArtifact.Artifact( 'queue_get_results', internal_jobqueue_getresults( self.db, user ) ) } )
		
		self.db.add_artifacts( user, {'periodic_add_job': libArtifact.Artifact( 'periodic_add_job', internal_periodicjobs_adder( self.db, user ) ) } )
		self.db.add_artifacts( user, {'periodic_remove_job': libArtifact.Artifact( 'periodic_remove_job', internal_periodicjobs_remove( self.db, user ) ) } )
		
		self.db.add_artifacts( user, {'transaction_query_to_commit': libArtifact.Artifact( 'transaction_query_to_commit', internal_transaction_query_to_commit( self.db, user ) ) } )
		self.db.add_artifacts( user, {'transaction_rollback': libArtifact.Artifact( 'transaction_rollback', internal_transaction_rollback( self.db, user ) ) } )
		self.db.add_artifacts( user, {'transaction_commit': libArtifact.Artifact( 'transaction_commit', internal_transaction_commit( self.db, user ) ) } )
		self.db.add_artifacts( user, {'transaction_add_peer': libArtifact.Artifact( 'transaction_add_peer', internal_transaction_add_peer( self.db, user ) ) } )
		self.db.add_artifacts( user, {'transaction_remove_peer': libArtifact.Artifact( 'transaction_remove_peer', internal_transaction_remove_peer( self.db, user ) ) } )
		self.db.add_artifacts( user, {'transaction_list_peers': libArtifact.Artifact( 'transaction_list_peers', internal_transaction_list_peers( self.db, user ) ) } )
		
		self.db.add_artifacts( user, {'partition_set': libArtifact.Artifact( 'partition_set', internal_partition_set( self.db, user ) ) } )
		self.db.add_artifacts( user, {'partition_get': libArtifact.Artifact( 'partition_get', internal_partition_get( self.db, user ) ) } )
		self.db.add_artifacts( user, {'partition_add_key': libArtifact.Artifact( 'partition_add_key', internal_partition_add_key( self.db, user ) ) } )
		self.db.add_artifacts( user, {'partition_remove_key': libArtifact.Artifact( 'partition_remove_key', internal_partition_remove_key( self.db, user ) ) } )
		
	
	def add_code_blob( self, user, code ):
		arts = code_to_artifacts( self.db, user, code )
		#print "Added ", arts.keys()
		self.db.add_artifacts( user, arts )
	
	def get_artifact( self, user, name ):
		return self.db.get_artifact( user, name )

	def attach_method( self, user, name, method ):
		self.db.add_artifacts( user, { name: libArtifact.Artifact( name, method, single = True ) } )




