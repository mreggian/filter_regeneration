Author: Marina Reggiani-Guzzo (Syracuse University)

Last modified: 2026-06-29

# Filter Regeneration

Hello, this repository contains all the scripts you need to monitor the variables of interest during the filter regeneration process.

Variables of interest, the the name of the device used for collecting this information:
1. Temperature in the body of the filter (device: PTC10)
2. Power provided to the heating tapes (device: PTC10)
3. Humidity, dew point and temperature on the top of the filter (device: EZO-HUM sensor)
4. Pressure at the top of the filter (device: EZO-PRS sensor)

## List of files in Repository

- `back_up_files.sh`: backs up data from InfluxDB into CSV files. Information is retrieved from the PTC10, EZO-HUM and EZO-PRS devices. Back-up files are saved under `/daq/`
- `monitor_ezo_sensors.py`: reads information from Arduinos (already saved into a text file) and saves the good-quality data into InfluxDB.
- `monitor_ptc10.py`: reads information from PTC10 and saves it to InfluxDB.
- `plotting_temp_and_water_concentration.py`: plots temperature at filter (collected by the temperature probe installed on the body of the filter) and the water concentration in ppm, calculated from the dew point measured by the EZO-HUM sensor.
- `setup.py`: activates the virtual environment, activates the USB ports (used by the PTC10 and EZO sensors), opens two CoolTerm windows and prints instructions on how to set it up in order to save data from Arduino into a text file.
- `venv_regeneration.txt`: list of packages to be installed on virtual environment

## Hardware Preparation

Please grab the "Filter Regeneration Kit", it should contain the following items:
* 1x [PTC10 Temperature Controller](https://www.thinksrs.com/products/ptc10.html) with PTC330K and PTC420 cards
* 2x [heating tapes](https://www.mcmaster.com/3641K17/);
* Extension cord (to be used with heating tapes);
* [EZO-PRS](https://atlas-scientific.com/product/pressure-sensor/?srsltid=AfmBOopZfapj54Jq4X8SrQzSNvsDnx7D30NAhOcFSfpvjAbZaWylhGV-) and [EZO-HUM](https://atlas-scientific.com/probes/humidity-probe/?srsltid=AfmBOooUSNPaoxlnDZgBcq05bG310ZNOctu_RlRq1W5-tr1qAW-cpYpQ) sensors;
* Acrylic board with two arduinos;
* 3x USB cables (2 long, 1 short);
* Connectors to install EZO sensors and exhaust hose;
* Orange hose (for exhaust system);
* Exhaust fan and black hose;
* Regulator, flowmeter and hose system (to be connected to dewar);
* [VCR to NPT adapter](https://www.mcmaster.com/9066N406/);
* Purchase:
  * Gas mix (95% argon and 5% hydrogen)
  * [Fiberglass blanket](https://www.mcmaster.com/4579N12/)
 
### Installation

Follow the instructions below:
- Prepare the filter:
  - Wrap the heating tape around the filter evenly (leave both plugs close together to make it easier to connect them to the power strip). Connect both plugs to a power strip and plug it on the output plug of the PTC10 device.
  - Cover everything with a fiberglass blanket and tape. Make sure to leave open an access to the plug for the temperature probe;
  - Install temperature probe on the body of the filter, and connect it to port 3A of the PTC10 device (pay attention to the orientation).
- Connect the regulator and the flowmeter on the argon&hydrogen cylinder, then connect the hose to the 1/2" VCR connector at the bottom of the filter. Make sure there is no gas flow at first.
<img width="430" height="766" alt="Screenshot 2026-04-29 at 15 00 31" src="https://github.com/user-attachments/assets/43d24695-6e88-407a-a284-a3aecc3be8fc" />

- Connect the cross-shaped adapter to the pipe on top of the filter, after the yellow valve. Install the exhaust hose, and the EZO-HUM and EZO-PRS sensors as image below.
  - The orange hose goes connected to the exhaust pipe of the lab.
  - Connect EZO-HUM and EZO-PRS sensors to the arduino boards, follow labels, and then connect them to your computer using a USB cable.
<img width="1343" height="529" alt="Screenshot 2026-04-29 at 14 58 54" src="https://github.com/user-attachments/assets/a34fed16-c4bb-4718-94c1-9f585a397918" />

- Connect the PTC10 device to a computer using a USB cable.
- Place the fan on the top of the structure and connect it to the ventilation system of the lab.
- Cover the structure holding the filter with plastic, to avoid the smell of burn and any other evaporated chemical to spread in the lab.

### Calibrating sensors

The EZO-HUM and EZO-PRS sensors should already be calibrated from the previous time we regenerated the filter. But, follow steps below in case you need to re-calibrate them.
* **EZO-PRS sensor**. Use the 1/4" NPTM-1/2" VCRF adaptor to connect the EZO-PRS sensor directly to the hose coming from the argon-gas-mix dewar. Set pressure on regulator to 5 PSI, and use command `Cal,5` on ArduinoUNO software.
* **EZO-HUM sensor**. We used the temperature probe connected to the body of the filter as our thermometer. We want both temperature sensors (EZO-HUM and Temperature Probe type K) to have the same initial reading. Once you know the room temperature use command `Cal,20` (if temperature is 20C) on ArduinoUNO software.

### Calibrating the PTC10 device
- Settings for the output channel:
<img width="554" height="410" alt="Screenshot 2026-04-29 at 16 06 45" src="https://github.com/user-attachments/assets/4786cdf0-c49c-48c2-bafd-5f47090f445f" />

- Settings for the temperature probe channel, 3A:
<img width="554" height="410" alt="Screenshot 2026-04-29 at 16 07 49" src="https://github.com/user-attachments/assets/26166f30-8337-458f-a9fd-7141efd3e4ac" />



## Software Preparation

The steps below will consider that you already have all the devices properly installed and ready for data acquisition.

You should also have a file `influxdb_config.py` with the following information


1. [Only required on first time] Download files and prepare environment
    1. Download repository on the computer you're going to use for the procedure
    2. Open the repository on a terminal
    3. Create a virtual environment: `python3 -m venv venv_regeneration`
    4. Activate your virtual environment: `source venv_regeneration/bin/activate`
    5. Install packages: `pip install -r venv_regeneration.txt`
    6. Create a file `influxdb_config.py` with the following information about your InfluxDB database
```
token = ""
root_token = ""
ORG = ""
BUCKET = ""
url = ""
```
2. [From second time] Setup environment by running `source setup.sh`, and follow instructions on terminal on how to set up CoolTerm and save data from Arduino to a text file.
3. [Install InfluxDB](https://docs.influxdata.com/influxdb/v2/install/) and activate (`sudo service influxdb`) and check status (`sudo service influxdb status`).
4. Open terminal and run `python3 monitor_ptc10.py`. It collects and sends data from PTC10 to InfluxDB.
5. Open terminal and run `python3 monitor_ezo_sensors.py`. It collects and sends data from EZO sensors to InfluxDB.

### Starting the Regeneration Process

 **Warm-up process:** The first thing is to warm up the filter to 250 C. Find below the steps taken during our first regeneration. The variables listed below are: `setpoint = temperature goal` and `HiLmt = upper limit for power provided to the heating tapes`.

- 2026-04-27
  - 13:17 | `setpoint = 50 C` and `HiLmt = 150 W`
  - 15:16 | `setpoint = 80 C`
  - 16:29 | `setpoint = 120 C`
- 2026-04-28
  - 10:25 | `HiLmt = 200 W`
  - 11:05 | `setpoint = 150 C`
  - 13:33 | `HiLmt = 230 W`
  - 15:16 | `setpoint = 180 C`
  - 15:24 | `HiLmt = 300 W`
- 2026-04-29
  - 09:25 | `setpoint = 210 C`
  - 10:52 | `setpoint = 220 C`
  - 14:13 | `HiLmt = 250 W`
  - 14:19 | `setpoint = 240 C`
  - 15:53 | `HiLmt = 400 W`
