#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

#import hashlib, bisect, copy


class HashRing( object ):
	def __init__( self, replicas = 1, track_changes = False ):
		self.replicas = replicas
		self.ring = {}
		self.keys = []
		self.invert_ring = {}
	
		self.accessed_keys = set()
		self.key_mapping = {}
		self.saved_mapping = {}
		
		self.invalid_nodes = set()
		
		self.track_changes = track_changes
	
	def invalidate_node( self, node ):
		self.invalid_nodes.add( node )
	
	def validate_node( self, node ):
		self.invalid_nodes.discard( node )
	
	def get_invalid_keys( self ):
		out = []
		for node in self.invalid_nodes:
			out.extend( self.invert_ring[ node ] )
		return out
	
	def save_state( self ):
		for (key, item) in self.key_mapping.items():
			self.saved_mapping[ key ] = item
		
	
	def generate_key( self, key ):
		return cloudSnake.modules.hashlib.md5( key ).hexdigest()
	
	def compute_changes( self ):
		self.compute_mapping()
		changes = []
		for key in self.accessed_keys:
			if self.saved_mapping[ key ] != self.key_mapping[ key ]:
				changes.append( ( key, self.saved_mapping[ key ], self.key_mapping[ key ] ) )
		return changes
		
	
	def add_node( self, node ):
		self.invert_ring[ node ] = []
		
		if self.track_changes:
			self.save_state()
		
		for i in range( self.replicas ):
			key = self.generate_key( str( i ) + "+" + str( node ) )
			self.ring[ key ] = node
			cloudSnake.modules.bisect.insort( self.keys, key )
			self.invert_ring[ node ].append( key )
		
		if self.track_changes:
			return self.compute_changes()
		return True
		
	def remove_node( self, node ):
		
		if self.track_changes:
			self.save_state()
		
		keys = self.invert_ring[ node ]
		for key in keys:
			self.keys.remove( key )
		
		del self.invert_ring[ node ]
	
		if self.track_changes:
			return self.compute_changes()
		else:
			return True
		
	

	def _raw_get_node( self, key ):
		pos = cloudSnake.modules.bisect.bisect_right( self.keys, key )
		
		node_key = self.keys[ pos - 1 ]
		
		return self.ring[ node_key ]

		
	def get_node( self, skey ):
		
		key = self.generate_key( skey )
	
		self.accessed_keys.add( key )
		
		valid_keys = self.keys
		invalid_keys = self.get_invalid_keys()
		for ikey in invalid_keys:
			valid_keys.remove( ikey )
		
		pos = cloudSnake.modules.bisect.bisect_right( valid_keys, key )
		
		node_key = valid_keys[ pos - 1 ]
		
		if self.track_changes:
			self.key_mapping[ key ] = self.ring[ node_key ]
		
		return self.ring[ node_key ]
	

	def get_keys_for_node( self, node ):
		return self.invert_ring[ node ]
	
	def compute_mapping( self ):
		for key in self.accessed_keys:
			self.key_mapping[ key ] = self._raw_get_node( key )

	
