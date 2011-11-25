#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy


import math, json, urllib, urllib2, base64, hashlib
import collections, os, mimetypes, time, bisect, copy
import xml.dom.minidom, re, pprint, StringIO

# Postgresql
#import psycopg2

class SandboxModules( object ):
	def __init__( self ):
		self.math = math
		self.json = json
		self.urllib = urllib
		self.urllib2 = urllib2
		self.base64 = base64
		self.hashlib = hashlib
		self.collections = collections
		self.os = os
		self.mimetypes = mimetypes
		self.time = time
		self.dom = xml.dom.minidom
		self.bisect = bisect
		self.copy = copy
		self.re = re
		self.pprint = pprint
		self.StringIO = StringIO
		
		#self.postgres = psycopg2
		
