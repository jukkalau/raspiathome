#!/bin/bash
# script to check that temps.py is still running
ps -ef | grep -v grep | grep temps.py
# if not found - equals to 1, start it
if [ $? -eq 1 ]
then
python ~/raspiathome/temps.py &
#ugly hardcoded path to repo home
else
#echo "eq 0 - temps.py found - all ok"
fi
