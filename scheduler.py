#!/usr/bin/python
import sched
import sys
import time
import datetime as dt
from subprocess import call
import logging
import logging.handlers
import os.path



def powerOn(deviceID):
        my_logger.info('PowerON:' + str(dt.datetime.today()))
        call(["tdtool","-n 1"])
def powerOff(deviceID):
        my_logger.info('PowerOFF:' + str(dt.datetime.today()))
        call(["tdtool","-f 1"])
def getTemp(path):
        global temptime
        with open(path, 'r') as f:
                data = f.read()
                temp = data.split(':')[1]
                my_logger.info("temperature outside: " + str(temp))
                temp = float(temp)
                if (temp < 5) and (temp >=-5):
                        time = 40
                elif (temp <-5) and (temp >=-10):
                        time = 70
                elif (temp <-10):
                        time = 130
                else:
                        time = 0
                temptime = time

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def readEndTime():
        if os.path.isfile("/tmp/endtime"):
            with open("/tmp/endtime") as f:
                line = f.readlines()
            splitted = line[0].split(":")
            my_logger.info("values read from configuration: %s:%s" %  (splitted[0], splitted[1]))
            if is_number(splitted[0]) and is_number(splitted[1]):
		if int(splitted[0])<25 and int(splitted[1])<60:
                    return splitted
        my_logger.error("Invalid values in configuration file, using defaults instead")
        return False

my_logger = logging.getLogger("car pre-heating scheduler")
my_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("/var/www/temp/scheduler.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
my_logger.addHandler(handler)

my_logger.info("scheduler started")
temptime = 0

targetTimes = readEndTime()
if targetTimes:
    targetHeatHour = int(targetTimes[0])
    targetHeatMinutes = int(targetTimes[1])
else:
    targetHeatHour = 7
    targetHeatMinutes = 20

#temp = int(sys.argv[1])
now = dt.datetime.today()
endTime = dt.datetime(now.year, now.month, now.day, targetHeatHour,targetHeatMinutes)
heatCalculationTime = dt.datetime(now.year, now.month, now.day, 5,30)
my_logger.info("heating time will be measured at: " + str(heatCalculationTime))
my_logger.info("target time for heating to be finished: " + str(endTime))

scheduler = sched.scheduler(time.time, time.sleep)
scheduler2 = sched.scheduler(time.time, time.sleep)

# first schedule is to find out how long heating is needed
heatCalculationTime = time.mktime(heatCalculationTime.timetuple())
scheduler.enterabs(heatCalculationTime, 1, getTemp,("/var/www/temp/last_tempBB.txt",))
scheduler.run()

# heating starts n minutes before end time
startDate = endTime - dt.timedelta(minutes=temptime)
startTime = time.mktime(startDate.timetuple())
endTimeT = time.mktime(endTime.timetuple())

# start heating
if temptime !=0:
	my_logger.info("heating will start: " + str(startDate) + " heating time will be: " + str(temptime))
	scheduler2.enterabs(startTime,2,powerOn,(1,))
	# stop heating
	my_logger.info("heating will stop: " + str(endTime))
	scheduler2.enterabs(endTimeT,2,powerOff,(1,))
else:
	my_logger.info("heating not needed, temperature over 5 degrees")

# TODO: enter periodic mode
#scheduler.enterabs(startTime,1,powerOn,(1,))
#scheduler.enterabs(endTime,1,powerOff,(1,))

time.sleep(10)
scheduler2.run()
my_logger.info("Scheduler stopped")
