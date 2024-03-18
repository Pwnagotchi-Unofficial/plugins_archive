import json
import os
import csv
import sys

# Converts a folder of JSON's to Wigle compatible CSV's. Creates the CSV's in the folder the script is in.
# Usage $ python Pwnagotchi-JSON-to-Wigle-CSV.py /home/pi/loot
# Currently does not work with the Tracker plugin's JSON's. May create a Tracker version eventually.

def convert_json_to_csv(json_folder):
    # Check if the given path is a directory
    if not os.path.isdir(json_folder):
        print(f"Error: {json_folder} is not a directory.")
        return

    # Iterate through all files in the directory
    for json_file in os.listdir(json_folder):
        if json_file.endswith('.json'):
            json_file_path = os.path.join(json_folder, json_file)
            try:
                convert_single_json_to_csv(json_file_path)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file '{json_file}': {e}")
                continue

def convert_single_json_to_csv(json_file):
    with open(json_file, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON in file '{json_file}': {e}", doc=e.doc, pos=e.pos)

    # Extracting information from file name
    file_name = os.path.basename(json_file)
    
    # Use everything before the last underscore as SSID
    ssid = '_'.join(file_name.split('_')[:-1])
    
    # Use the last part after the last underscore as BSSID
    bssid = file_name.split('_')[-1].split('.')[0]
    bssid_with_colons = ':'.join([bssid[i:i+2] for i in range(0, len(bssid), 2)])

    # Extracting required information from JSON data
    capabilities = data.get('Capabilities', 'WPA2')
    
    # Extract timestamp and format it
    timestamp_str = data.get('Updated', '')
    formatted_timestamp = format_timestamp(timestamp_str)

    channel = data.get('Channel', '1')
    rssi = data.get('RSSI', 0)
    accuracy = data.get('Accuracy', 50)

    # Extracting Latitude, Longitude, and Altitude from JSON data
    latitude = data.get('Latitude', '')
    longitude = data.get('Longitude', '')
    altitude = data.get('Altitude', '')

    # Creating CSV rows
    csv_file_name = f"{ssid}_{bssid}.csv"
    with open(csv_file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Add the lines
        csv_writer.writerow(["WigleWifi-1.6", "appRelease=2.53", "model=pwnagotchi", "release=11", "device=pwnagotchi", "display=kismet", "board=kismet", "brand=pwnagotchi", "star=Sol", "body=3", "subBody=0"])
        csv_writer.writerow([
            "MAC", "SSID", "AuthMode", "FirstSeen", "Channel", "Frequency", "RSSI",
            "CurrentLatitude", "CurrentLongitude", "AltitudeMeters", "AccuracyMeters",
            "RCOIs", "MfgrId", "Type"
        ])
        
        # Add the data from JSON
        csv_row = [
            bssid_with_colons,
            ssid,
            capabilities,
            formatted_timestamp,
            channel,
            '2437',
            rssi,
            latitude,
            longitude,
            altitude,
            accuracy,
            'WIFI'
        ]
        csv_writer.writerow(csv_row)

    print(f"CSV file '{csv_file_name}' created successfully.")

def format_timestamp(timestamp_str):
    try:
        # Use the first 10 characters and replace 'T' with a space
        date_part = timestamp_str[:10].replace('T', ' ')
        # Use the next 8 characters
        time_part = timestamp_str[11:19]
        # Combine date and time parts
        formatted_timestamp = f"{date_part} {time_part}"
        return formatted_timestamp
    except IndexError:
        print(f"Error formatting timestamp: '{timestamp_str}'")
        return ''

# Example usage
if len(sys.argv) != 2:
    print("Usage: python Test-JSON-toCSV.py <json_folder_path>")
    sys.exit(1)

json_folder_path = sys.argv[1]
convert_json_to_csv(json_folder_path)
