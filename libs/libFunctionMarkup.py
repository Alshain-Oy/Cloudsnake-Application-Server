#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

class HtmlStream( object ):
	def __init__( self ):
		self.content = ""
	
	def write( self, text ):
		self.content += text
	
	def getvalue( self ):
		return self.content

	def __str__( self ):
		return self.content

class HtmlGenerator( object ):
	def __init__( self ):
		self.stream = HtmlStream()
	
	
	def set_stream( self, stream ):
		self.stream = stream
	
	def emit( self ):
		return self.stream.getvalue()
	
	def __str__( self ):
		return self.emit()
	
	def __call__( self, tag = "", content = "", **kwargs ):
		if len( tag ) == 0:
			return HtmlGenerator()
		
		if not content:
			content = ""
		else:
			content = str( content )
		
		
		tag_attributes = {}
		
		begin = False
		end = False
		
		for ( key, value ) in kwargs.items():
			if key == 'begin':
				begin = value
			elif key == 'end':
				end = value
			else:
				if key.startswith( '_' ):
					key = key[1:]
				tag_attributes[ key ] = value
		
		
		str_attr = ""
		for (key,val) in tag_attributes.items():
			str_attr += '%s="%s" ' %( key, val )
		
		str_attr = str_attr.strip()
		
		out = ""
		if len( content ) > 0:
			out = "<%s %s >%s</%s>"%( tag, str_attr, str( content ), tag )
		else:
			if not begin and not end:
				out = '<%s %s />'%( tag, str_attr )
			elif begin:
				out += '<%s %s >'%( tag, str_attr )
			elif end:
				out += '</%s>'%( tag )
		
		print >>self.stream, out
			
		
	
	
