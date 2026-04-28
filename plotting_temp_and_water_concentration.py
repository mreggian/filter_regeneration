# Author: Marina Reggiani-Guzzo
# Last modified: 2026-04-28

# Description: this script retrieves information from the backup files, and plots
# the temperature and water vapor concentration inside the filter. Trying to reproduce
# Figure 5 from https://arxiv.org/pdf/0903.2066

# Requirements:
# - backup_ezohum_data.csv
# - backup_ptc_data.csv

# How to run:
# > python3 plotting_temp_and_water_concentration.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

def create_dataframe(filename: str):
    df = pd.read_csv(filename, low_memory=False)
    df = df.drop(['#group', 'false', 'false.1', 'true', 'true.1', 'true.3'], axis=1) # remove undesired columns
    df.rename(columns={'false.2': 'timestamp'}, inplace=True) 
    df.rename(columns={'false.3': 'measurement'}, inplace=True)
    df.rename(columns={'true.2': 'tag'}, inplace=True)
    df = df.drop([0,1,2], axis=0) # remove undesired rows
    df.reset_index(drop=True, inplace=True) # reset row index, so it starts at row=0
    df['measurement'] = df['measurement'].astype(float) # transform column 'measurement' from string to float
    return df

def calc_water_vapor_concentration(df: pd.DataFrame, P=101325):

    # For reference:
    # https://www.processsensing.com/en-us/blog/converting-dew-point-other-measuring-units.htm

    # convert celcius to kelvin
    df["measurement_K"] = df["measurement"] + 273.15
    T = df["measurement_K"]

    df["e"] = np.where(
    T > 273.15,  # corresponds to dew_point > 0°C
    (-6096.9385 / T)
    + 21.2409642
    - 2.711193 * T
    + 1.673952e-5 * T
    + 2.433502 * np.log(T),

    (-6024.5282 / T)
    + 29.32707
    + 1.0613868 * T / 100
    - 1.3198825e-5 * T**2
    - 0.49382577 * np.log(T)
)

    df["e"] = np.exp(df["e"])

    df["ppmv"] = (df["e"]/P)*1000000

    return df


if __name__ == "__main__":

    df = create_dataframe('daq/backup_ptc_data.csv')
    df = df[df.tag=="temp"]
    df = df.iloc[::20]
    df.reset_index(drop=True, inplace=True)

    df_ezo = create_dataframe('daq/backup_ezohum_data.csv')
    df_ezo = df_ezo[df_ezo.tag=='dewpoint']
    df_ezo = df_ezo.iloc[::20]
    df_ezo = calc_water_vapor_concentration(df_ezo.copy())
    df_ezo.reset_index(drop=True, inplace=True)


    fig, ax1 = plt.subplots()

    # Left y-axis → Temperature
    ax1.set_ylabel("Water Vapor Concentration [ppm]", color="tab:red")
    ax1.plot(range(0,len(df_ezo)), df_ezo['ppmv'], color="tab:red", linewidth=2)
    ax1.tick_params(axis="y", labelcolor="tab:red")
    ax1.yaxis.set_major_locator(MaxNLocator(nbins=10))
    ax1.xaxis.set_major_locator(MaxNLocator(nbins=6))

    # Right y-axis → Power
    ax2 = ax1.twinx()
    ax2.set_ylabel("Temperature [C]", color="tab:blue")
    ax2.plot(df["timestamp"], df["measurement"], color="tab:blue", linewidth=2)
    ax2.tick_params(axis="y", labelcolor="tab:blue")
    ax2.yaxis.set_major_locator(MaxNLocator(nbins=10))


    tick_positions = ax1.get_xticks() 
    tick_positions = tick_positions.astype(int) 
    tick_positions = tick_positions[(tick_positions >= 0) & (tick_positions < len(df_ezo))]
    arr = df_ezo.iloc[tick_positions]["timestamp"].to_numpy() # retrieve timestamp from dataframe from the selected entries
    timestamp_readable = pd.to_datetime(arr).strftime("%b %-d, %Y\n%H:%M:%S") # re-shape timestamp to more readable format
    plt.xticks(tick_positions, timestamp_readable, rotation='vertical', ha="center") # replace ticks with timestamps
    fig.tight_layout()
    plt.show()


