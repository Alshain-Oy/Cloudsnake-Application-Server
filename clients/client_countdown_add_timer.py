#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import client_countdown_lib as Countdown
import sys, getpass

user = sys.argv[ 1 ]
fn = sys.argv[ 2 ]

name = sys.argv[ 3 ]
target = sys.argv[ 4 ]


countdown = Countdown.TimerDB( user )

countdown.load_token( fn )

countdown.add_timer( name, target )



	

 
