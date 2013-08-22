#!/usr/bin/python
# script to generate a graph from data in temperature.db
# takes 3 parameters
# * sensor ID, this is the id xrf sensor uses when communicating
# * period, how far from the past data is collected. Parameter
# is pushed directly to where clause so be careful with it
# * output file, where to generate graph
#
# usage example: python gengraph.py -s AA -p '31 day' -o test.png
# 
# jukkalau@gmail.com
#

import argparse
import sqlite3
import datetime
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from matplotlib import dates

def gen_graph(args):
#parse commandline arguments
    sensor = args.sensor
    period = args.period
    outfile = args.output

    fig = plt.figure()
    fig.set_size_inches(11, 5)
    ax = fig.add_subplot(111)
    ax.xaxis.grid()
    ax.yaxis.grid()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(dates.DateFormatter('%d.%m %H:%M'))
    ax.autoscale_view()
    x_series = []
    x2_series = []
    y_series = []
    y2_series = []
    con = sqlite3.connect('/home/naxu/raspiathome/temperature.db')
    with con:
        cur = con.cursor()
	sql = "select * from temps where sensor = '" + sensor  + "' AND timestam > (datetime('now','-" + period + "'))"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            try:
                value = float(row[2])
            except:
                value = 0
            if (sensor in row[1]) and (value <> 0):
                x2_series.append(dates.date2num(
                        datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")))

                y2_series.append(round(value,1))
        cur.execute("select MIN(value), MAX(value) from temps where sensor = '" + sensor + "' and timestam  > (datetime('now','-" \
                        + period + "'))")
        maxmin = cur.fetchall()
        fig.suptitle("min / max \n" + str(round(maxmin[0][0],1)) + "$^\circ$C / " + str(round(maxmin[0][1],1)) + "$^\circ$C", fontsize=24)
        ax.plot(x2_series, y2_series, label = "Temp " + sensor )
        plt.gcf().autofmt_xdate()
        plt.ylabel("Celsius")
        plt.savefig(outfile,dpi=50)
        print ("graph plotted")
        return True

def roundToHalf(value):
# round sensor value to nearest half degree. Code copied from 	
# http://mail.python.org/pipermail/tutor/2010-October/079317.html
    if value % 1 >= 0.5:
        rounded = round(value) # gives 5.0 if  the the value of the expression x % 1 exceeds 0.5
    else:
       rounded  = round(value) + 0.5 # gives 4.5, as in this case.
    return rounded

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate graph from temperature data')
    parser.add_argument('-s','--sensor', help = 'Sensor ID', required = True)
    parser.add_argument('-p','--period', help = "How long period is used. For example '1 day'", 
                        required = True)
    parser.add_argument('-o','--output', help = 'Graph file name', required = True)
    args = parser.parse_args()	
    gen_graph(args)
