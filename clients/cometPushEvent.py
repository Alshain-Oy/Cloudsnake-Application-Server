#!/usr/bin/env python

import libCloudSnakeClient as SnakeClient

import pprint, sys

client = SnakeClient.CloudSnakeClient( 'http://localhost:8101', 'main' )


push = client.get_method( 'push' )



print push( event =  sys.argv[ 1 ], content = sys.argv[ 2 ] )


