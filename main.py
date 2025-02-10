import asyncio, os
from flask import Flask, jsonify

from meross_iot.controller.mixins.electricity import ElectricityMixin
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

# import credentials
from cred import credentials
from setup import setup_http_client
from discover_devices import discover_devices

# retrieve credentials from cred.py
EMAIL = credentials["EMAIL"]
PASSWORD = credentials["PASSWORD"]

# checks if email/pass are nil
if not EMAIL or not PASSWORD:
    raise ValueError("Email and password must be provided.")

print("setting up http client...")
http_api_client = asyncio.run(setup_http_client(EMAIL, PASSWORD))  

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    return asyncio.run(discover_devices(http_api_client))
   
if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.run(port=5000)


