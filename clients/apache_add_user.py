#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, sys, time, hashlib, getpass, base64

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'main' )



snake = SnakeClient.CloudSnakeMapper( client )

user = sys.argv[ 1 ]

pw = getpass.getpass()

pwhash = base64.b64encode( hashlib.sha1( pw ).digest() )

snake.apache_add_user( user, pwhash )


