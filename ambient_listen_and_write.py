from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from influxdb_client import Point, InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import configparser
import os

class RequestHandler(BaseHTTPRequestHandler):
    # Writes GET request to a log file
    def log_request_to_file(self, query_string):
        with open('/home/konrad/scripts/logs/ambient_requests.log', 'a') as file:
            file.write("Path:" + query_string + '\n')

    # Formats data for InfluxDB
    def format_for_influx(self, data_dict):
        influx_data = []
        for key, value in data_dict.items():
            point = Point("ambientweather").field(key, float(value) if value.replace('.', '', 1).isdigit() else value)
            influx_data.append(point)
        return influx_data

    # Parses the latest log entry and writes to InfluxDB
    def parse_and_write_to_influx(self):
        with open('/home/konrad/scripts/logs/ambient_requests.log', 'r') as file:
            last_line = file.readlines()[-1]

        if last_line.startswith("Path:"):
            query_string = last_line.split("Path:", 1)[1].strip()
            query_string = query_string[1:] if query_string.startswith('/') else query_string
            data_dict = urllib.parse.parse_qs(query_string)
            data_dict = {k: v[0] for k, v in data_dict.items()}

            influx_points = self.format_for_influx(data_dict)
            for point in influx_points:
                write_api.write(bucket=bucket, org=org, record=point)

    # Handles GET requests
    def do_GET(self):
        query_string = self.path
        self.log_request_to_file(query_string)
        self.parse_and_write_to_influx()
        self.send_response(200)
        self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=3445):
    global bucket, org, write_api

    # Setup placeholder for state file check
    state_file = 'path/to/your/state/file.txt'
    if os.path.exists(state_file):
        print("Script is already running.")
        return
    else:
        open(state_file, 'w').close()

    # Load InfluxDB configuration from a config file
    config = configparser.ConfigParser()
    config.read('path/to/your/config.ini')
    influx_token = config['influx']['token']  # Replace with your InfluxDB token
    org = "your_org"  # Replace with your InfluxDB organization
    bucket = "your_bucket"  # Replace with your InfluxDB bucket

    # Setup InfluxDB client
    client = InfluxDBClient(url="your_influxdb_url", token=influx_token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Start the HTTP server
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting server on port", port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        os.remove(state_file)

if __name__ == '__main__':
    run()
