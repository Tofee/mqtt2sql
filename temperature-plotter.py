#!/usr/bin/python3

import json
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from dateutil import parser
from matplotlib import style
from matplotlib.dates import date2num

def graph_data():
    # Connect to database
    now = datetime.now()
    sqlite_file = '/var/spool/mqtt2sql/mqtt-sensors.db'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT ts,value FROM mqtt_history')
    data = c.fetchall()
    # data[*][0] = timestamp
    # data[*][1] = json payload

    temperature = []
    humidity = []
    battery = []
    timenow = []

    for row in data:
        json_obj = json.loads(row[1])
        temperature.append(json_obj['temperature'])
        humidity.append(json_obj['humidity'])
        battery.append(json_obj['battery'])
        timenow.append(parser.parse(row[0]))

    # Convert datetime.datetime to float days since 0001-01-01 UTC.
    dates = [date2num(t) for t in timenow]

    style.use('fivethirtyeight')
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title("Température du salon")

    # Configure x-ticks
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y %H:%M'))

    # Plot temperature data on left Y axis
    ax1.set_ylabel("Temperature [°C]")
    ax1.plot_date(dates, temperature, '-', label="Temperature", color='r')

    # Plot humidity data on right Y axis
    ax2 = ax1.twinx()
    ax2.set_ylabel("Humidité [% RH]")
    ax2.plot_date(dates, humidity, '-', label="Humidity", color='b')

    # Format the x-axis for dates (label formatting, rotation)
    fig.autofmt_xdate(rotation=60)
    fig.tight_layout()

    # Show grids and legends
    ax1.grid(True)
    ax1.legend(loc='best', framealpha=0.5)
    ax2.legend(loc='best', framealpha=0.5)

    plt.savefig("/tmp/temperature-salon.png")
    
    c.close()
    conn.close()
    
graph_data()
