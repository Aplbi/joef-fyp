import asyncio, os
from flask import Flask, jsonify

# import credentials
from cred import credentials
from functions.setup import setup
from functions.discover_devices import discover_devices


# retrieve credentials from cred.py
EMAIL = credentials["EMAIL"]
PASSWORD = credentials["PASSWORD"]

# checks if email/pass are nil
if not EMAIL or not PASSWORD:
    raise ValueError("Email and password must be provided.")

print("setting up http client and initializing manager...")
http_api_client, manager = asyncio.run(setup(EMAIL, PASSWORD))


app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    return asyncio.run(discover_devices(http_api_client, manager))
    
if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.run(port=5000)
