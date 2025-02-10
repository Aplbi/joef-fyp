import asyncio 
from flask import jsonify
from meross_iot.manager import MerossManager
from meross_iot.controller.mixins.electricity import ElectricityMixin

from flask import jsonify

async def discover_devices(http_api_client):
    # Placeholder data
    default_data = {
        "power": "123 W",
        "status": "On",
        "temperature": "21°C"
    }
    if http_api_client is None:
        raise ValueError("HTTP client is not set up.")
    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Discover devices
    await manager.async_device_discovery()

    # Find all MSS315 devices
    plugs = manager.find_devices(device_type="mss315")

    counter = 0
    max_count = 20
    while len(plugs) < 1 and counter <= max_count:
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
                return jsonify(instant_consumption)
            else:
                print(f"The device {dev.name} does not support electricity metrics.")
        
        print("ping count:", counter)
        counter += 1
        await asyncio.sleep(1)

    # Close the manager and logout from http_api
    print("ping count exceeds", max_count, ", closing manager")
    manager.close()
    await http_api_client.async_logout()

    print("No MSS315 plugs found..., returning default data")
    return jsonify(default_data)
    