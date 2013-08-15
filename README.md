raspiathome
===========

Collection of scripts to collect and present temperature data from XRF temp sensors


Setup:

Scripts use a SQLite database "temperature.db" to store the sensor data. Database can be created with sql query:

CREATE TABLE temps(id INTEGER PRIMARY KEY AUTOINCREMENT, sensor TEXT, value FLOAT, Timestam date DEFAULT (datetime('now','localtime')));
Yes, there is a typo in TimestamP column name. SQLite does not support changing of column name so it will stay like that until everything else has been done...

Python libraries:
Scripts use following libraries, they need to be installed.

argparse
sqlite3
datetime
matplotlib
serial
re
logging




