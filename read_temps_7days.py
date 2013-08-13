import sqlite3
import datetime
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from matplotlib import dates

def gen_graph():
	fig = plt.figure()
	fig.set_size_inches(11,5)
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
	con = sqlite3.connect('~/raspiathome/temperature.db')
	with con:
		cur = con.cursor()
		cur.execute("select * from temps where timestam > (datetime('now','-7 day'))")
		rows = cur.fetchall()
		for row in rows:
			if 'BB' in row[1]:
				x2_series.append(dates.date2num(datetime.datetime.strptime(row[3],"%Y-%m-%d %H:%M:%S")))
				y2_series.append(row[2])
	ax.plot(x2_series, y2_series, label="Temp BB")
	plt.gcf().autofmt_xdate()
	plt.ylabel("Celsius")
#	ax2 = ax.twinx()
#	ax2.plot(x_series, y_series, label="Temp AA")
#	plt.savefig("/srv/http/kuva.png",dpi=100)
	plt.savefig("~/raspiathome/www/temp/7_days.png",dpi=50)
	print ("graph plotted")
	return True

if __name__ == "__main__":
   gen_graph()
