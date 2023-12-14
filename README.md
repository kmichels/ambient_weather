# Ambient Weather Station Data to InfluxDB Script

## Overview
This script is specifically designed to handle data from Ambient Weather Stations. It functions as an HTTP server, listening for GET requests with weather data, and processes this information for storage in InfluxDB v2.

## Features
- **Data Logging**: Logs incoming weather data from GET requests to a file.
- **Data Parsing & Formatting**: Parses logged data and formats it for compatibility with InfluxDB v2.
- **InfluxDB Integration**: Seamlessly writes formatted data to an InfluxDB v2 instance.
- **Single Instance Safeguard**: Ensures that only one instance of the script runs at a time.

## Configuration
Before use, configure the script with your InfluxDB credentials and server details in the `config.ini` file.

---

*Note: Replace placeholders in the script with your actual InfluxDB credentials and server details for proper operation.*
