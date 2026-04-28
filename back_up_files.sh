# Author: Marina Reggiani-Guzzo
# Last edited: 2026-04-28

#!/bin/bash

org=$(python3 -c "import influxdb_config; print(influxdb_config.ORG)")
bucket=$(python3 -c "import influxdb_config; print(influxdb_config.BUCKET)")
export INFLUX_TOKEN=$(python3 -c "import influxdb_config; print(influxdb_config.token)")

echo "Backing up data from PTC10..."
eval "influx query --org \"${org}\" --token \"${INFLUX_TOKEN}\" 'from(bucket: \"${bucket}\") |> range(start:2026-04-24T17:00:00Z) |> filter(fn: (r) => r._measurement==\"ptc10\")' > daq/backup_ptc_data.txt"
echo "Backing up data from EZO Humidity sensor..."
eval "influx query --org \"${org}\" --token \"${INFLUX_TOKEN}\" 'from(bucket: \"${bucket}\") |> range(start:2026-04-24T17:00:00Z) |> filter(fn: (r) => r._measurement==\"ezohum\")' > daq/backup_ezohum_data.txt"
echo "Backing up data from EZO Pressure sensor..."
eval "influx query --org \"${org}\" --token \"${INFLUX_TOKEN}\" 'from(bucket: \"${bucket}\") |> range(start:2026-04-24T17:00:00Z) |> filter(fn: (r) => r._measurement==\"ezoprs\")' > daq/backup_ezoprs_data.txt"
