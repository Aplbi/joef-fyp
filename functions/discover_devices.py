import asyncio 
from itertools import count
import time
from quart import jsonify
from meross_iot.manager import MerossManager
from meross_iot.controller.mixins.electricity import ElectricityMixin


async def discover_devices(http_api_client, manager):
    # Placeholder data
    default_data = {
        "power": "123 W",
        "status": "On",
        "temperature": "21°C"
    }
    if http_api_client is None:
        raise ValueError("HTTP client is not set up.")

    # Discover devices
    await manager.async_device_discovery()

    # Find all MSS315 devices
    plugs = manager.find_devices(device_type="mss315")

    counter = 0
    max_count = 20
    while len(plugs) < 1 and counter <= max_count:
        print(counter)
        if len(plugs) < 1:
            print("No MSS315 plugs found...")
            # Try discovering devices again
            await manager.async_device_discovery()
            plugs = manager.find_devices(device_type="mss315")
        else:
            dev = plugs[0]
            await dev.async_update()
            print("plug:", dev)
            # Check if the device supports electricity metrics
            if isinstance(dev, ElectricityMixin):
                # Read electricity power/voltage/current metrics
                instant_consumption = await dev.async_get_instant_metrics()
                print(f"Current consumption data: {instant_consumption}")
                return jsonify({
                    "power": str(instant_consumption.power),
                    "voltage": str(instant_consumption.voltage),
                    "current": str(instant_consumption.current),
                    "timestamp": str(instant_consumption.sample_timestamp)
                })
            else:
                print(f"The device {dev.name} does not support electricity metrics.")
        
        print("ping count:", counter)
        counter += 1
        await asyncio.sleep(1)  # Use asyncio.sleep instead of time.sleep

    # No need to close manager since it's managed at the application level
    if len(plugs) > 0:
        instant_consumption = await plugs[0].async_get_instant_metrics()
        print(f"Current consumption data: {instant_consumption}")
        
        return jsonify({
            "power": str(instant_consumption.power),
            "voltage": str(instant_consumption.voltage),
            "current": str(instant_consumption.current),
            "timestamp": str(instant_consumption.sample_timestamp)
        })
    
    print("ping count exceeds", max_count, ", no devices found", "returning default data")
    return jsonify(default_data)