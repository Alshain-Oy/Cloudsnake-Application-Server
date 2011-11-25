
# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy


def test_001():
	out = []
	#for x in range( 2000 ):
	#	out.append( x**2 )
	return out


def get_feed( feed_url ):
	feed = cloudSnake.memdb.get( 'feed:' + feed_url )
	if not feed or feed[ 1 ] > cloudSnake.modules.time.time() + 60:
		handle = cloudSnake.modules.urllib.urlopen( feed_url )
		data = handle.read()
		handle.close()
		doc = cloudSnake.modules.dom.parseString( data )
		items = []
		for elem in doc.getElementsByTagName( "item" ):
			title = elem.getElementsByTagName( "title" )[ 0 ]
			txt = ""
			for node in title.childNodes:
				if node.nodeType == node.TEXT_NODE:
					txt += node.data
			items.append( txt )
		cloudSnake.memdb.set( 'feed:' + feed_url, ( items, cloudSnake.modules.time.time() ) )
	else:
		items = feed[ 0 ]
		
	return items
	
