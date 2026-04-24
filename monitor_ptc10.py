# Author: Marina Reggiani-Guzzo
# Last modified: April 23, 2026
# Description: retrieves information from PTC10 and saves it into a text file
# the output data is: "timestamp date time temperature[C] power[W]"

import serial
import time
import matplotlib.pyplot as plt
from collections import deque
import random
import os
from datetime import datetime
from pathlib import Path

if __name__ == "__main__":

    # ===
    # Initial configuration, make sure everything is correct here
    output_file = f"daq/ptc10_output_{datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    #port = '/dev/tty.usbserial-DK0AQB0V' # Marina's computer
    port = '/dev/ttyUSB0' # lab's computer

    # plotting
    create_plot = True
    N_data = 600 # number of points to display
    set_point = float(50) # temperature goal, plot a horizontal line for visual purposes
    
    # === 
    # Initial plotting configuration

    if create_plot:
        # define arrays for plotting
        y_power = deque(maxlen=N_data)
        y_temp = deque(maxlen=N_data)
        y_setpoint = deque(maxlen=N_data)
        x_timestamp = deque(maxlen=N_data)

        plt.ion() # turn on interactive mode
        fig, axs = plt.subplots(2, 1, figsize=(8,6))
        line_power, = axs[0].plot([], [])
        line_setpoint, = axs[1].plot([], [], linestyle='dashed', color='red')
        line_temp,  = axs[1].plot([], [])

    # ===
    # start script

    # Create the folder and any missing parents; do nothing if it already exists
    Path("daq").mkdir(parents=True, exist_ok=True)

    # Write header on file
    with open(output_file, 'a') as f:
        f.write('timestamp date time temperature power\n')

    if os.path.exists(port):

        t_start = time.time()

        # establish serial connection
        ser = serial.Serial(port, 230400, timeout=1)

        # start collecting data from PTC10
        while True:

            # collect information from PTC10
            time.sleep(0.1)
            ser.write(b'getOutput?\n')
            time.sleep(0.1)
            raw = ser.read_all()

            try:
                decoded = raw.decode('ascii').strip()

                if not decoded:
                    raise ValueError("Empty response")

                values = [v.strip() for v in decoded.split(',')]

                # check if there are enough entries in array "values", otherwise retrieving information will fail
                if len(values) <= 4:
                    raise ValueError(f"Not enough values len(values)={len(values)}")

                # Retrieve information
                var_temp = float(values[4])
                var_power = float(values[0])

            except (UnicodeDecodeError, ValueError) as e:
                print(f"ERROR (skip iteration). {e}")
                time.sleep(1)
                continue

            # Retrieve timestamp
            timestamp = time.time()
            timestamp_date = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
            timestamp_time = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
            
            with open(output_file, 'a') as f:
                f.write(f'{timestamp} {timestamp_date} {timestamp_time} {var_temp} {var_power}\n')

            if create_plot:
                y_power.append(var_power)
                y_temp.append(var_temp)
                y_setpoint.append(set_point)
                time_from_t0 = time.time() - t_start
                x_timestamp.append(time_from_t0)

                line_power.set_data(x_timestamp, y_power)
                line_setpoint.set_data(x_timestamp, y_setpoint)
                line_temp.set_data(x_timestamp, y_temp)

                axs[0].relim()
                axs[0].autoscale_view()
                axs[0].set_ylim(min(y_power)-1, max(y_power)+1)
                axs[0].set_ylabel("Power (W)")

                axs[1].relim()
                axs[1].autoscale_view()
                axs[1].set_ylim(min(y_temp)-1, max(y_temp)+1)
                axs[1].set_ylabel("Temperature (C)")
                axs[1].set_xlabel("Seconds since t0")

                plt.draw()
                plt.pause(0.1) # pause to update the plot

            time.sleep(1)
        
        # Close serial connection after daq is finished
        ser.close()
    
    else:
        print("Device not connected. Closing script.")
