#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy


import fuse

import time, sys


import stat, os, errno

import libCloudSnakeClient as SnakeClient

fuse.fuse_python_api = (0, 2)

class ObjectStat(fuse.Stat):
	def __init__( self ):
		self.st_mode = stat.S_IFDIR | 0755
		self.st_ino = 0
		self.st_dev = 0
		self.st_nlink = 2
		self.st_uid = 0
		self.st_gid = 0
		self.st_size = 4096
		self.st_atime = int( time.time() )
		self.st_mtime = int( time.time() )
		self.st_ctime = int( time.time() )
  


class testFS( fuse.Fuse ):
	def __init__(self, *args, **kw):
		fuse.Fuse.__init__(self, *args, **kw)

		print 'Init complete.'
		
		self.files = []
		#self.files.append( 'htpasswd_id' )
		self.client = None
		
	def attach_cloudsnake( self, client ):
		self.client = client
		self.snake = SnakeClient.CloudSnakeMapper( self.client )
		
		self.files = self.snake.apache_get_groups()
		print "self.files:", self.files
		self.content = {}

	def getattr(self, path):
		"""
		- st_mode (protection bits)
		- st_ino (inode number)
		- st_dev (device)
		- st_nlink (number of hard links)
		- st_uid (user ID of owner)
		- st_gid (group ID of owner)
		- st_size (size of file, in bytes)
		- st_atime (time of most recent access)
		- st_mtime (time of most recent content modification)
		- st_ctime (platform dependent; time of most recent metadata change on Unix,
					or the time of creation on Windows).
		"""

		print '*** getattr', path

		#depth = getDepth(path) # depth of path, zero-based from root
		#pathparts = getParts(path) # the actual parts of the path

		#return -errno.ENOSYS
		
		self.files = self.snake.apache_get_groups()
		print "self.files:", self.files
		
		st = ObjectStat()
		
		parts = path.split( '/' )
		if len( parts ) > 1:
			fn = parts[ 1 ]
		else:
			fn = ''
		
		if fn == '':
			print "returing stats"
			st.st_nlink += len( self.files )
			return st
		
		elif fn not in self.files:
			print "No such file! (%s)"%fn
			return -errno.ENOENT
		else:
			print "Returning stats.."
			st.st_mode = stat.S_IFREG | 0755
			
			self.content[ fn ] = self.snake.apache_get_content( fn )
			st.st_size = len( self.content[ fn ] )
			
			return st
		
#	def getdir(self, path):
#		"""
#		return: [[('file1', 0), ('file2', 0), ... ]]
#		"""
#		self.files = self.snake.apache_get_groups()
#		
#		print '*** getdir', path
#		#return -errno.ENOSYS
#		return [[ (x, 0) for x in self.files ]]
	
	def readdir(self, path, offset):
		
		print "*** readdir"
		
		dirents = [ '.', '..' ]
		
		self.files = self.snake.apache_get_groups()
		print "self.files:", self.files
		
		
		if path == '/':
			dirents.extend( self.files )
		
		for r in dirents:
			yield fuse.Direntry( str( r ))


	def chmod( self, path, mode ):
		print '*** chmod', path, oct(mode)
		#return -errno.ENOSYS
		return 0

	def chown( self, path, uid, gid ):
		print '*** chown', path, uid, gid
		#return -errno.ENOSYS
		return 0

	def fsync( self, path, isFsyncFile ):
		print '*** fsync', path, isFsyncFile
		return -errno.ENOSYS

	def link( self, targetPath, linkPath ):
		print '*** link', targetPath, linkPath
		return -errno.ENOSYS

	def mkdir( self, path, mode ):
		print '*** mkdir', path, oct(mode)
		return -errno.ENOSYS

	def mknod( self, path, mode, dev ):
		print '*** mknod', path, oct(mode), dev
		return -errno.ENOSYS

	def open( self, path, flags ):
		print '*** open', path, flags
		#return -errno.ENOSYS
		return 0

	def read( self, path, length, offset ):
		print '*** read', path, length, offset
		#return -errno.ENOSYS
		parts = path.split( '/' )
		fn = parts[ 1 ]
		self.content[ fn ] = self.snake.apache_get_content( fn )
		#return self.content[ fn ][ offset : offset + length ]
		out = self.content[ fn ][ offset : offset + length ]
		print "out:", out
		return str( out )
		
		
		

	def readlink( self, path ):
		print '*** readlink', path
		return -errno.ENOSYS

	def release( self, path, flags ):
		print '*** release', path, flags
		#return -errno.ENOSYS
		return 0

	def rename( self, oldPath, newPath ):
		print '*** rename', oldPath, newPath
		return -errno.ENOSYS

	def rmdir( self, path ):
		print '*** rmdir', path
		return -errno.ENOSYS

	def statfs( self ):
		print '*** statfs'
		return -errno.ENOSYS

	def symlink( self, targetPath, linkPath ):
		print '*** symlink', targetPath, linkPath
		return -errno.ENOSYS

	def truncate( self, path, size ):
		print '*** truncate', path, size
		return -errno.ENOSYS

	def unlink( self, path ):
		print '*** unlink', path
		return -errno.ENOSYS

	def utime( self, path, times ):
		print '*** utime', path, times
		return -errno.ENOSYS

	def write( self, path, buf, offset ):
		print '*** write', path, buf, offset
		return -errno.ENOSYS


if __name__ == '__main__':
	
	client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'main' )
	
	fs = testFS()
	fs.attach_cloudsnake( client )
	
	fs.flags = 0
	fs.multihreaded = 0
	fs.parse()
	fs.main()
	#print fs.main.__doc__
	
	
