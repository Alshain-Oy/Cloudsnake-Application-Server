#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint, sys

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', sys.argv[ 1 ] )


pprint.pprint( client.get_method( 'list_artifacts' )() )
