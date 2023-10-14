import json
import os
import csv
from datetime import datetime
import re

# Set path to data directory with samples in JSON format
data_dir = "/Users/matthewturk/Desktop/speed-test/wifi-samples"

with open("/Users/matthewturk/Desktop/speed-test/wifi-samples/wifi.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write CSV header
    csv_writer.writerow(["time", "x", "y", "download_speed", "download_units",
                         "upload_speed", "upload_units", "latency", "latency_units",
                         "loss", "loss_units"])

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            # Extract coordinates from filename.
            coordinate_match = re.search(r"(\d+\.\d+)_(\d+\.\d+)", filename)
            x = coordinate_match.group(1)
            y = coordinate_match.group(2)

            with open(os.path.join(data_dir, filename)) as json_file:
                data = json.load(json_file)

            # Get timestamp from file modification time.
            print(os.stat(os.path.join(data_dir, filename)).st_mtime)
            time = datetime.fromtimestamp(os.path.getctime(os.path.join(data_dir, filename)))

            csv_writer.writerow([time, x, y, data["downloadSpeed"],
                                 data["downloadUnit"], data["uploadSpeed"],
                                 data["uploadUnit"], data["latency"],
                                 data["latencyUnit"], data["loss"],
                                 data["lossUnit"]])
