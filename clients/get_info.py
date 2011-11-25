#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import libCloudSnakeClient as SnakeClient

import pprint

client = SnakeClient.CloudSnakeClient( 'http://localhost:8500', 'maintenance' )


get_report = client.get_method( 'report' )


#print test_001( {'data':[]})

#print get_output()


#client.print_output()


pprint.pprint( get_report() )
