# Todo
# [x] Get all measurements
# [x] Get temperature from RSP (if possible)
# [x] Save all measurements to file with timestamp
# [x] Might be interesting to look at the csv module 
# [] Give file a timestamp
# [x] Add Header to file
# [x] Add sensible cronjob time interval -> Running every 2 mins via crontab
# [] Try out using a Class
# [] Calibrate the temperature readings
# [x] Add to git / github
# [] Add appropriate start and end of this file 

# Import Libraries
from sense_hat import SenseHat
import csv
import os.path
import subprocess
import datetime as dt
from time import sleep
import re

# Initialization of SenseHat
sense = SenseHat()

# File path to write to
FILE_PATH = "/home/pi/data/sense_data.csv"

# Check if file exist or is empty
try:
    fileEmpty = os.stat(FILE_PATH).st_size == 0
except:
    fileEmpty = True

# Retrieve Sensor results (if any is zero, retry)
pressure = sense.get_pressure()
humidity = sense.get_humidity()
temp_hum = sense.get_temperature_from_humidity()
temp_pres = sense.get_temperature_from_pressure()

# Get RSP temperature
# cli command: vcgencmd measure_temp
rsp_temp_output = subprocess.run(["vcgencmd","measure_temp"],
                                 capture_output=True)
rsp_temp = re.findall("temp=(.*)'C", str(rsp_temp_output))[0]

# Write sensor results to file
with open(FILE_PATH, "a") as csvfile:
    header = ['timestamp',
               'rsp_temp',
               'pressure',
               'humidity',
               'temp_hum',
               'temp_pres']
    writer = csv.DictWriter(csvfile,
                            delimiter=',',
                            lineterminator='\n',
                            fieldnames=header)
    if fileEmpty:
        writer.writeheader()  # file doesn't exist yet, write a header

    writer.writerow({'timestamp': dt.datetime.now(),
                     'rsp_temp': rsp_temp,
                     'pressure': pressure,
                     'humidity': humidity,
                     'temp_hum': temp_hum,
                     'temp_pres': temp_pres})
