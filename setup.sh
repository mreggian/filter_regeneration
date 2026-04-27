# Author: Marina Reggiani-Guzzo
# Last edited: 2024-06-17

#!/bin/bash

# activate virtual environment
echo 'Activating virtual environment...'
source venv_regeneration/bin/activate

# activate usb ports
echo 'Activating USB ports...'
sudo chmod a+rw /dev/ttyUSB0 /dev/ttyACM0 /dev/ttyACM1