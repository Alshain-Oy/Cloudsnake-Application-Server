#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libFunctionMarkup as FM


html = FM.HtmlGenerator()

html( 'html', begin = True )

head = html()

head( 'title', 'otsikko' )

html( 'head', head )

main_list = html()
main_list( 'ul', begin = True )


for i in range( 10 ):
	main_list( 'li', 'Item #%i'%i, _class="kolme" )

main_list( 'ul', end = True )


html( 'body', main_list )

html( 'html', end = True )

print html

