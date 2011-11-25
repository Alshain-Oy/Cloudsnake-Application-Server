#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import client_countdown_lib as Countdown
import sys, getpass, time, math

user = sys.argv[ 1 ]
fn = sys.argv[ 2 ]



countdown = Countdown.TimerDB( user )

countdown.load_token( fn )

timers = countdown.get_timers()

now = time.time()

for timer in timers:
	print "%-30s"%timer['name'], 
	target = time.mktime( time.strptime( timer['target'], "%Y-%m-%d %H:%M:%S" ) )
	dt = target-now
	days = math.floor( dt / ( 24 * 3600 ) )
	dt = dt - days * 24 * 3600
	
	hours = math.floor( dt / ( 3600 ) )
	
	dt = dt - hours * 3600
	
	minutes = math.floor( dt / 60 )
	
	dt = dt - minutes * 60
	
	print "%02id %02ih %02im %02is left."%( days, hours, minutes, dt )
	
	

	

 
