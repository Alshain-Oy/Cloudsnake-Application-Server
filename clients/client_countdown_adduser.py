#!/usr/bin/env python

# Cloudsnake Application server
# Licensed under Apache License, see license.txt
# Author: Markus Gronholm <markus@alshain.fi> Alshain Oy

import client_countdown_lib as Countdown
import sys, getpass

fn = sys.argv[ 1 ]

user = raw_input( "User: " )
pw = getpass.getpass()

countdown = Countdown.TimerDB()

countdown.create_user( user, pw )


#countdown = Countdown.TimerDB( user )
#if countdown.authenticate():
#	countdown.save_token( fn )

 
