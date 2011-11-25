#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'main' )


init = client.get_method( 'init' )



print init()
