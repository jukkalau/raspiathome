#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# script to read xrf sensor data from serial
# validate message to avoid carbage being pushed to the db
# writes also last detected temp value from each sensor to 
# a separate file
#
# This code is put together from various examples in the net
# If you see this usefull in your project, use it. :)
#
# jukkalau@gmail.com
#

import serial
import re
import sqlite3
import sys
import read_temps
import logging
import logging.handlers

my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address='/dev/log')
my_logger.addHandler(handler)


baud = 9600
port = '/dev/ttyAMA0'
ser = serial.Serial(port, baud)

con = sqlite3.connect('~/raspiathome/temperature.db')

while True:
	with con:
		cur = con.cursor()
		llapMsg = str(ser.read(12))
		my_logger.debug(llapMsg)
		#match voltage message
		validator = re.compile("a([A-Z][A-Z])TMPA{1,2}(\d.\.{1,2}\d{1,2}\d)")
		m = validator.match(llapMsg)
		if m:
			sqlstring = "insert into temps(sensor,value) values('" + m.group(1) + "','" + m.group(2) + "')"
			my_logger.debug(sqlstring)
			cur.execute(sqlstring)
			fh = open("~/raspiathome/www/temp/last_temp" + m.group(1) + ".txt", "w")
			if m.group(1) == 'BB':
			    sname = 'Ulkona'
			elif m.group(1) == 'CC':
			    sname = 'Tuloilma'
                        else:
			    sname = 'Alakerrassa'
			fh.write(sname + ":" + m.group(2))
			fh.close()
		# todo: fix voltage reporting to be done in correct sensor file
		elif re.search("BATT", llapMsg):
			value = llapMsg[7:12]
			fh = open("/var/www/temp/last_temp.txt", "w")
	       	        fh.write("Patteri: " + value + "V")
               		fh.close()
		else:
			null = ser.read(24)	
