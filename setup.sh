# Author: Marina Reggiani-Guzzo
# Last edited: 2026-04-29

#!/bin/bash

# activate virtual environment
echo 'Activating virtual environment...'
source venv_regeneration/bin/activate

# activate usb ports
echo 'Activating USB ports...'
sudo chmod a+rw /dev/ttyUSB0 /dev/ttyACM0 /dev/ttyACM1

# Open two windows of CoolTerm
echo 'Opening CoolTerm...'
gnome-terminal -- bash -c "cd /home/syr-neutrino/Downloads/CoolTermLinux64Bit/ && ./CoolTerm"
gnome-terminal -- bash -c "cd /home/syr-neutrino/Downloads/CoolTermLinux64Bit/ && ./CoolTerm"

echo '\nSetup complete. Please configure CoolTerm as follows:'
echo '> 1. Click on Connection>Options>SerialPort and select "/dev/ttyACM0" for the environment data and "/dev/ttyACM1" for the pressure data. Click "Ok".'
echo '> 2. Click on Conection>Options>FileCapture and unselect "Leave file open after capture". Click "Ok".'
echo '> 3. Click on Connection>FileCapture>Start, it will prompt you to name your text file. Make sure to save it under /home/syr-neutrino/Desktop/filter_regeneration/daq/ and name it "env_YYYY-MM-DD.txt" for the environment data and "prs_YYYY-MM-DD.txt" for the pressure data, where YYYY-MM-DD is the current date. Click "Save".'

# Go back to original directory
cd /home/syr-neutrino/Desktop/filter_regeneration/
