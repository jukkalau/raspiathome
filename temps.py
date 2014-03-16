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
import logging
import logging.handlers
import ConfigParser

my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
my_logger.addHandler(handler)

parser = ConfigParser.SafeConfigParser()
parser.read('config.ini')

baud = 9600
port = '/dev/ttyAMA0'
ser = serial.Serial(port, baud, timeout=10)
con = sqlite3.connect('temperature.db')

def main():
    err = 0 # error counter, hackish way to recover from offsync in xrf communication
    while True:
        with con:
            cur = con.cursor()
            llapMsg = str(ser.read(12))
            my_logger.debug(llapMsg)
            #match voltage message
            #matches also negative value aBBTMPA-9.99
            validatorTemp = re.compile("a([A-Z][A-Z])TMPA(( |-)?\d.{1,3}\d)")
            validatorHum = re.compile("a([A-Z][A-Z])HUMA(( |-)?\d.{1,3}\d)")
            m = validatorTemp.match(llapMsg)
            mHum = validatorHum.match(llapMsg)
            if m:
                sqlstring = "insert into temps(sensor,value) values('" + m.group(1)\
                + "','" + m.group(2) + "')"
                my_logger.debug(sqlstring)
                cur.execute(sqlstring)
                fh = open("www/temp/last_temp" + m.group(1) + ".txt", "w+")
                sname = parser.get(m.group(1),"displayName") 
                # fetch calibration multiplier from ini file and use that to 
                # store fixed temp reading to db
                fixedValue = float(parser.get(m.group(1),"calibrationValue")) \
                * float(m.group(2))
                fh.write(sname + ":" + str(round(fixedValue, 2)))
                fh.close()
                err = 0
            elif mHum:  # handle humidity sendor ( by cheating )
                # todo: add new table to db to hold humidity values
                # now, only 2nd identifier character being H differentiates temp from
                # humidity
                sqlstring = "insert into temps(sensor,value) values('" + mHum.group(1)\
                + "','" + mHum.group(2) + "')"
                my_logger.debug(sqlstring)
                cur.execute(sqlstring)
                fh = open("www/temp/last_hum" + mHum.group(1) + ".txt", "w+")
                sname = parser.get(mHum.group(1),"displayName")
                # fetch calibration multiplier from ini file and use that to
                # store fixed temp reading to db
                fixedValue = float(parser.get(mHum.group(1),"calibrationValue")) \
                * float(mHum.group(2))
                fh.write(sname + ":" + str(round(fixedValue, 2)))
                fh.close()
                err = 0
            # todo: fix voltage reporting to be done in correct sensor file
            elif re.search("BATT", llapMsg):
                value = llapMsg[7:12]
                fh = open("www/temp/last_temp" + llapMsg[1:3] +".txt" , "w+")
                fh.write("Patteri " + llapMsg[1:3] + ": " + value + "V")
                fh.close()
                err = 0
            elif re.search("AWAKE", llapMsg):
                my_logger.debug("AWAKE message catched")
	        err = 0
            elif re.search("STARTED", llapMsg):
                my_logger.debug("STARTED message catched")
                err = 0
            elif re.search("SLEEPING", llapMsg):
                my_logger.debug("STARTED message catched")
                err = 0
            else:
                if err > 13:
                    my_logger.debug("Error count hit, bailing out")
                    return 1
                my_logger.debug(
                    "reg-exp did not catch message, emptying serial buffer")
                crap = ser.read(ser.inWaiting())
                my_logger.debug(crap)
                err = err + 1

main()
