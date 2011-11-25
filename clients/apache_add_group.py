#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, sys, time, hashlib, getpass

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'main' )



snake = SnakeClient.CloudSnakeMapper( client )

group = sys.argv[ 1 ]


snake.apache_add_group( group, [] )




