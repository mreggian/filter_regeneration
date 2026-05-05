Author: Marina Reggiani-Guzzo (Syracuse University)

Last modified: 2026-04-29

# Filter Regeneration

Hello, this repository contains all the scripts you need to monitor the variables of interest during the filter regeneration process.

Variables of interest, the the name of the device used for collecting this information:
1. Temperature in the body of the filter (device: PTC10)
2. Power provided to the heating tapes (device: PTC10)
3. Humidity, dew point and temperature on the top of the filter (device: EZO-HUM sensor)
4. Pressure at the top of the filter (device: EZO-PRS sensor)

## List of files in Repository

- `ModifiedArduinoScript_Environment.txt` and `ModifiedArduinoScript_Pressure.txt`: scripts to be uploaded to the Arduino boards to monitor the environment and pressure conditions.
- `back_up_files.sh`: backs up data from InfluxDB into CSV files. Information is retrieved from the PTC10, EZO-HUM and EZO-PRS devices. Back-up files are saved under `/daq/`.
- `backup_ezohum_data_compress.zip`, `backup_ezoprs_data_compress.zip` and `backup_ptc_data_compress.zip`: backup files with data collected during the regeneration process.
- `monitor_ezo_sensors.py`: reads information from Arduinos (already saved into a text file) and saves the good-quality data into InfluxDB.
- `monitor_ptc10.py`: reads information from PTC10 and saves it to InfluxDB.
- `plotting_temp_and_water_concentration.py`: plots temperature at filter (collected by the temperature probe installed on the body of the filter) and the water concentration in ppm, calculated from the dew point measured by the EZO-HUM sensor.
- `setup.py`: activates the virtual environment, activates the USB ports (used by the PTC10 and EZO sensors), opens two CoolTerm windows and prints instructions on how to set it up in order to save data from Arduino into a text file.
- `venv_regeneration.txt`: list of packages to be installed on virtual environment

## Hardware Preparation

Please grab the "Filter Regeneration Kit", it should contain the following items:
* 1x [PTC10 Temperature Controller](https://www.thinksrs.com/products/ptc10.html) with PTC330K and PTC420 cards
* 2x [heating tapes](https://www.mcmaster.com/3641K17/)
* 1x extension cord
* 1x [EZO-PRS](https://atlas-scientific.com/product/pressure-sensor/?srsltid=AfmBOopZfapj54Jq4X8SrQzSNvsDnx7D30NAhOcFSfpvjAbZaWylhGV-) sensor
* 1x [EZO-HUM](https://atlas-scientific.com/probes/humidity-probe/?srsltid=AfmBOooUSNPaoxlnDZgBcq05bG310ZNOctu_RlRq1W5-tr1qAW-cpYpQ) sensor
* Acrylic board with two arduinos
* 3x USB cables (2 long, 1 short)
* System to connect argon gas dewar to filter:
  * [Regulator](https://harrisweldingsupplies.com/harris-model-425-hydrogen-methane-single-stage-regulator-425-50a-350-3000784/)
  * [Flowmeter](https://harrisweldingsupplies.com/harris-model-55-2he-h2-90-9-16-in-18-f-compensated-flowmeter-5400612/) -- replace connector
  * [5/18”-18 UNF M — 1/4” NPT M adapter](https://www.mcmaster.com/7919A52/)
  * [Hose](https://www.mcmaster.com/5665K61/)
  * [1/4" NPT F - 3/8" NPT M Adapter](https://www.mcmaster.com/4452K163/)
  * [3/8" NPT F - 1/2" VNC F Adapter](https://products.swagelok.com/en/c/straights/p/SS-8-VCR-7-6?q=:relevance:connection1Size:1%2F2+in.:connection2Type:Female+NPT)
* Connectors to install EZO sensors and exhaust hose;
* Orange hose;
* Exhaust fan and black hose;
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
  - Connect EZO-HUM and EZO-PRS sensors to the arduino boards (red cable=5V, black cable=GND, green cable=Digital Channel 2, white cable=Digital Channel 3, for both sensors), follow labels, and then connect them to your computer using a USB cable.
<img width="1343" height="529" alt="Screenshot 2026-04-29 at 14 58 54" src="https://github.com/user-attachments/assets/a34fed16-c4bb-4718-94c1-9f585a397918" />

- Connect the PTC10 device to a computer using a USB cable.
- Place the fan on the top of the structure and connect it to the ventilation system of the lab.
- Cover the structure holding the filter with plastic, to avoid the smell of burn and any other evaporated chemical to spread in the lab.

### Calibrating sensors

The EZO-HUM and EZO-PRS sensors should already be calibrated from the previous time we regenerated the filter. But, follow steps below in case you need to re-calibrate them.
* **EZO-PRS sensor**. Use the 1/4" NPTM-1/2" VCRF adaptor to connect the EZO-PRS sensor directly to the hose coming from the argon-gas-mix dewar. Set pressure on regulator to 5 PSI, and use command `Cal,5` on ArduinoUNO software.
* **EZO-HUM sensor**. We used the temperature probe connected to the body of the filter as our thermometer. We want both temperature sensors (EZO-HUM and Temperature Probe type K) to have the same initial reading. Once you know the room temperature use command `Cal,20` (if temperature is 20C) on ArduinoUNO software.

### Calibrating the PTC10 device

Calibrating the PTC10 device is a crucial step, without whose the PID feedback does not work. The calibration should be done with the system ready for the regeneration process, meaning: the heating tapes placed around the filter, the temperature probe installed in the filter, and everything surrounded by the thermally insulating blanket. This is important because we want the temperature controller to have a real sense of how much it takes for the system to warm up and to cool down. Once everything is installed, the calibration was done by choosing the following parameters:
- Output channel: under Tune, `Step Y = 150.0 W` and `Lag = 600 s` and `Type = moderate`. For the calibration step, `HiLmt = 150.0 W`.
- Temperature probe channel: `Lopass = 300 s`.

The calibration is then performed by clicking on `Tune > Mode > Auto`. See below a picture of the overall configuration for both channels of interest: output and temperature probe.

Settings for the output channel:
<img width="554" height="410" alt="Screenshot 2026-04-29 at 16 06 45" src="https://github.com/user-attachments/assets/4786cdf0-c49c-48c2-bafd-5f47090f445f" />

Settings for the temperature probe channel, 3A:
<img width="554" height="410" alt="Screenshot 2026-04-29 at 16 07 49" src="https://github.com/user-attachments/assets/26166f30-8337-458f-a9fd-7141efd3e4ac" />



## Software Preparation

The steps below will consider that you already have all the devices properly installed and ready for data acquisition.

1. [Install InfluxDB](https://docs.influxdata.com/influxdb/v2/install/) on your computer, and create a database to storage the data. Make sure to write down the root token displayed on the screen when you create a new database, it will not be able to generate it again, and it is needed to backup your files later on! Activate the InfluxDB server (`sudo service influxdb`) and check if status is listed as "Active" (`sudo service influxdb status`).
2. [Only required on first time] Download files and prepare environment
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
3. [From second time] Setup environment by running `source setup.sh`, and follow instructions on terminal on how to set up CoolTerm and save data from Arduino to a text file.
4. Open terminal and run `python3 monitor_ptc10.py`. It collects and sends data from PTC10 to InfluxDB.
5. Open terminal and run `python3 monitor_ezo_sensors.py`. It collects and sends data from EZO sensors to InfluxDB.
6. Back up data from InfluxDB into a CSV file by running `source back_up_files.sh`. It will create a CSV backup file for all the data collected (from PTC10 and EZO sensors) in the /daq/ folder.

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
  - 16:23 | Open gas flow, pressure=10, flow=30
  - 16:35 | pressure=10, flow=85
  - 16:40 | `setpoint = 250 C` and `HiLmt = 450 W`
  - 16:51 | pressure=10, flow=40 (cylinder pressure = 2,600PSI)
- 2026-05-01, 9:40 | Stopped flow of Ar/H gas since the bottle pressure was getting very low, and we don't want atmosphere to flow back into the dry filter
- 2026-05-04, 10:50 | Turned off all DAQ, new backup files


