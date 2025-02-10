import asyncio, os, time
from flask import Flask, jsonify

from meross_iot.controller.mixins.electricity import ElectricityMixin
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

# Hardcoded credentials

from cred import credentials

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
async def get_data():
    # Placeholder data
    default_data = {
        "power": "123 W",
        "status": "On",
        "temperature": "21°C"
    }

    # checks if email/pass are nil
    if not EMAIL or not PASSWORD:
        raise ValueError("Email and password must be provided.")

    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(
        email=EMAIL,
        password=PASSWORD,
        api_base_url="https://iot.meross.com"
    )

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Discover devices
    await manager.async_device_discovery()

    # Find all MSS315 devices
    plugs = manager.find_devices(device_type="mss315")

    counter = 0
    while len(plugs) < 1 and counter <= 20:
        if len(plugs) < 1:
            print("No MSS315 plugs found...")
        else:
            dev = plugs[0]
            await dev.async_update()

            # Check if the device supports electricity metrics
            if isinstance(dev, ElectricityMixin):
                # Read electricity power/voltage/current metrics
                instant_consumption = await dev.async_get_instant_metrics()
                print(f"Current consumption data: {instant_consumption}")

            else:
                print(f"The device {dev.name} does not support electricity metrics.")
        counter += 1
        print("ping count:", counter)
        time.sleep(1)

    # Close the manager and logout from http_api

    print("ping count exceeds 20, closing manager")
    manager.close()
    await http_api_client.async_logout()

    return jsonify(default_data)


# retrieve credentials from cred.py
EMAIL = credentials["EMAIL"]
PASSWORD = credentials["PASSWORD"]

async def main():
    # checks if email/pass are nil
    if not EMAIL or not PASSWORD:
        raise ValueError("Email and password must be provided.")

    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(
        email=EMAIL,
        password=PASSWORD,
        api_base_url="https://iot.meross.com"
    )

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Discover devices
    await manager.async_device_discovery()

    # Find all MSS315 devices
    plugs = manager.find_devices(device_type="mss315")


    counter = 0
    while len(plugs) < 1 and counter <= 20:
        if len(plugs) < 1:
            print("No MSS315 plugs found...")
        else:
            dev = plugs[0]
            await dev.async_update()

            # Check if the device supports electricity metrics
            if isinstance(dev, ElectricityMixin):
                # Read electricity power/voltage/current metrics
                instant_consumption = await dev.async_get_instant_metrics()
                print(f"Current consumption data: {instant_consumption}")

            else:
                print(f"The device {dev.name} does not support electricity metrics.")
        counter += 1
        print("ping count:", counter)
        time.sleep(1)

    # Close the manager and logout from http_api

    print("ping count exceeds 20, closing manager")
    manager.close()
    await http_api_client.async_logout()



if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.run(port=5000)
