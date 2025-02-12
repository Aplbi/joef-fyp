import asyncio, os
from quart import Quart, jsonify

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

app = Quart(__name__)
http_api_client = None
manager = None

@app.before_serving
async def initialize():
    global http_api_client, manager
    print("setting up http client and initializing manager...")
    http_api_client, manager = await setup(EMAIL, PASSWORD)

# route for /api/data
@app.route('/api/data', methods=['GET'])
async def get_data():
    return await discover_devices(http_api_client, manager)
    
if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.run(port=5000)
