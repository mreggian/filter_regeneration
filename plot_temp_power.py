# Author: Marina Reggiani-Guzzo
# Last modified: April 20, 2026
# Description: This script takes the data saved as ptc10_output_<timestamp>.txt
# and creates a plot with temperature and power information

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def open_txt_file_as_pandas_df(inFile: str):

    df = pd.read_csv(inFile, sep=r"\s+", header=None, names=["timestamp", "date", "time", "temp", "power"])
    df = df.drop([0], axis=0) # remove undesired rows
    df.reset_index(drop=True, inplace=True)
    print(df.head())
    return df

if __name__ == "__main__":

    # what file do you want to plot?
    inFile = 'daq/ptc10_output_2026-04-23_10-57-36.txt'
    
    # what is the set temperature? displayed as a red-dotted line on the plot
    setpoint = 40 # unit = Celsius
    
    df = open_txt_file_as_pandas_df(inFile)

    # make plot
    fig, ax1 = plt.subplots()

    # Left y-axis → Temperature
    ax1.set_xlabel("Seconds since t0")
    ax1.set_ylabel("Temperature [°C]", color="tab:red")
    ax1.plot(df["timestamp"], df["temp"], color="tab:red", linewidth=2)
    ax1.tick_params(axis="y", labelcolor="tab:red")
    ax1.tick_params(axis='x', rotation=45)
    #ax1.axhline(y=50, color="red", linestyle="--", linewidth=1)
    #ax1.axhline(y=90, color="red", linestyle="--", linewidth=1)
    ax1.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax1.xaxis.set_major_locator(MaxNLocator(nbins=6))


    # Right y-axis → Power
    ax2 = ax1.twinx()
    ax2.set_ylabel("Power [W]", color="tab:blue")
    ax2.plot(df["timestamp"], df["power"], color="tab:blue", linewidth=2)
    ax2.tick_params(axis="y", labelcolor="tab:blue")
    ax2.yaxis.set_major_locator(MaxNLocator(nbins=5))

    plt.title("Temperature and Power vs Time")

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    #ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="best")

    #ax1.grid(True)
    fig.tight_layout()

    plt.show()


