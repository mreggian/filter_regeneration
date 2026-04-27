import time
import os
from collections import deque
import matplotlib.pyplot as plt

from influxdb_config import token, ORG, url, BUCKET
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

client = InfluxDBClient(url=url, token=token, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)


data_file_env = f"daq/env_2026-04-27.txt"
data_file_prs = f"daq/prs_2026-04-27.txt"
poll_interval_s = 0.5   #seconds between check
max_points = 400     #points shown
real_time_plotting = False


current_reading_env = ""
current_reading_prs = ""
timestamp_env = ""
timestamp_prs = ""
last_timestamp_env = None
last_timestamp_prs = None

first_timestamp_env = None
first_timestamp_prs = None


def read_n_to_last_line(filename, n=1):
    """Returns the nth before last line of a file (n=1 gives last line)"""
    num_newlines = 0
    with open(filename, 'rb') as f:
        #for line in f:
            #if line.strip():
                #o.write(line)
        try:
            f.seek(-2, os.SEEK_END)    
            while num_newlines < n:
                f.seek(-2, os.SEEK_CUR)
                if f.read(1) == b'\n':
                    num_newlines += 1
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
    return last_line

def give_me_value(last_line, key):
    parts = [p.strip() for p in last_line.strip().split("|")]

    for part in parts:
        if ":" not in part:
            continue
            
        key_from_line,val = part.split(":",1)
        key_from_line = key_from_line.strip().upper()
        val = val.strip()
    
        if key_from_line == key.upper():
            try:
                return float(val)
            except ValueError:
                return None
    return None     
    

if real_time_plotting:

    humidity = []
    temperature = []
    dewpoint = []
    pressure = []
    time_env = []
    time_prs = []

    plt.ion()

    fig, axs = plt.subplots(4, 1, figsize=(8, 10))

    line_hum, = axs[0].plot([], [])
    line_temp, = axs[1].plot([], [])
    line_dew, = axs[2].plot([], [])
    line_prs, = axs[3].plot([], [])

    axs[0].set_title("Relative Humidity")
    axs[1].set_title("Temperature")
    axs[2].set_title("Dew Point")
    axs[3].set_title("Pressure")

    axs[0].set_ylabel("Humidity (%)")
    axs[1].set_ylabel("Temperature (°C)")
    axs[2].set_ylabel("Dew Point (°C)")
    axs[3].set_ylabel("Pressure (psi)")

    axs[3].set_xlabel("Time (milliseconds)")

    plt.tight_layout()

while True:
    
    current_reading_env = read_n_to_last_line(data_file_env)
    current_reading_prs = read_n_to_last_line(data_file_prs)

    timestamp_env_str = current_reading_env.split("|")[0].strip()

    # ======================================================================
    # environment
    if timestamp_env_str != last_timestamp_env:

        hum = give_me_value(current_reading_env, "HUM")
        temp = give_me_value(current_reading_env, "Air TMP")
        dew = give_me_value(current_reading_env, "DEW")

        if hum is not None and temp is not None and dew is not None:

            if real_time_plotting:
                humidity.append(float(hum))
                temperature.append(float(temp))
                dewpoint.append(float(dew))
                time_env.append(float(timestamp_env_str))

            # save new points to InfluxDB
            point_hum = Point("ezohum").field("humidity", hum)
            point_temp = Point("ezohum").field("temperature", temp)
            point_dew = Point("ezohum").field("dewpoint", dew)
            write_api.write(bucket=BUCKET, org=ORG, record=point_hum)
            write_api.write(bucket=BUCKET, org=ORG, record=point_temp)
            write_api.write(bucket=BUCKET, org=ORG, record=point_dew)

            last_timestamp_env = timestamp_env_str

    timestamp_prs_str = current_reading_prs.split("|")[0].strip()

    # ======================================================================
    # pressure
    if timestamp_prs_str != last_timestamp_prs:

        prs_value = give_me_value(current_reading_prs, "PRS")
        
        if prs_value is not None:

            if real_time_plotting:
                pressure.append(float(prs_value))
                time_prs.append(float(timestamp_prs_str))

            # save new point to InfluxDB
            point_prs = Point("ezoprs").field("pressure", float(prs_value))
            write_api.write(bucket=BUCKET, org=ORG, record=point_prs)

            last_timestamp_prs = timestamp_prs_str

    if real_time_plotting:
        x_env = time_env
        x_prs = time_prs

        line_hum.set_data(x_env, humidity)
        line_temp.set_data(x_env, temperature)
        line_dew.set_data(x_env, dewpoint)
        line_prs.set_data(x_prs, pressure)

        for ax in axs:
            ax.relim()
            ax.autoscale_view()

        plt.pause(0.5)

    time.sleep(1)

client.close()
