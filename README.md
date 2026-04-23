Author: Marina Reggiani-Guzzo (Syracuse University) | Last modified: April 23, 2023

# Filter Regeneration

Hello, this repository contains all the scripts you need to monitor the variables of interest during the filter regeneration process.

Variables of interest, the the name of the device used for collecting this information:
1. Temperature in the body of the filter (device: PTC10)
2. Power provided to the heating tapes (device: PTC10)
3. Humidity, dew point and temperature on the top of the filter (device: EZO-HUM sensor)
4. Pressure at the top of the filter (device: EZO-PRS sensor)

## Hardware Preparation

Please grab the "Filter Regeneration Kit", it should contain the following items:
* 1x [PTC10 Temperature Controller](https://www.thinksrs.com/products/ptc10.html) with PTC330K and PTC420 cards
* 2x [heating tapes](https://www.mcmaster.com/3641K17/);
* Extantion cord (to be used with heating tapes);
* [EZO-PRS](https://atlas-scientific.com/product/pressure-sensor/?srsltid=AfmBOopZfapj54Jq4X8SrQzSNvsDnx7D30NAhOcFSfpvjAbZaWylhGV-) and [EZO-HUM](https://atlas-scientific.com/probes/humidity-probe/?srsltid=AfmBOooUSNPaoxlnDZgBcq05bG310ZNOctu_RlRq1W5-tr1qAW-cpYpQ) sensors;
* Acrylic board with two arduinos;
* 3x USB cables (2 long, 1 short);
* Connectors to install EZO sensors and exhaust hose;
* Orange hose (for exhaust system);
* Exhaust fan and black hose;
* Regulator, flowmeter and hose system (to be connected to dewar);
* VCR to NPT adapter;
* Purchase:
  * Gas mix (95% argon and 5% hydrogen)
  * Fiberglass blanket (https://www.mcmaster.com/4579N12/)

Follow the instructions below:

1. Wrap the heating tape around the filter, cover it with a fiberglass blanket and tape. Ensure to leave both plugs close together to make it easier to connect them to power later on. Plug both tapes to the same extension, and connect extention to output plug of the PTC10 device.
3. Install temperature probe on the body of the filter, and to PTC10 on port 3A (pay attention to the orientation).
4. Connect PTC10 device to computer via a USB cable.
5. Connect adapters on the top of the filter, and hose to the exhaust pipe.
6. Install EZO-HUM and EZO-PRS sensors, and connect them to the board with two arduinos. Each arduino is properly labelled, make sure to connect them correctly. Connect each arduino to the computer.
7. Connect fan hose to exhaust venting system of the lab.

The EZO-HUM and EZO-PRS sensors should already be calibrated from the previous time we regenerated the filter. But, follow steps below in case you need to re-calibrate them.
* **EZO-PRS sensor**.
* **EZO-HUM sensor**.


## Software Preparation

The steps below will consider that you already have all the devices properly installed and ready for data acquisition.

1. Download files and prepare environment
    1. Download repository on the computer you're going to use for the procedure
    2. Open the repository on a terminal
    3. Create a virtual environment: `python3 -m venv venv_regeneration`
    4. Activate your virtual environment: `source venv_regeneration/bin/activate`
    5. Install packages: `pip install -r venv_regeneration.txt`
2. Make sure devices are conn

### Starting the Regeneration Process
