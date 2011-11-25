#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

class Luokka( object ):
	def __init__( self, N ):
		self.luku = N
	
	
	def test( self ):
		return self.luku




def test_001( data ):
	#print >> cloudSnake.output, "Moi kaikki"
	#print >> cloudSnake.output, cloudSnake.call( 'mean', [ [1,2,3,4] ] )
	
	print >> cloudSnake.output, "Luokkakoe nro 1"
	otus = cloudSnake.call( 'Luokka', [7] )
	print >> cloudSnake.output, otus.test()
	
	

