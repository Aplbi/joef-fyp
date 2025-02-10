
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

# setup http client
async def setup(EMAIL, PASSWORD):
    
 
    # Setup the HTTP client API from user-password
    print("setting up http client...")
    http_api_client = await MerossHttpClient.async_from_user_password(
        email=EMAIL,
        password=PASSWORD,
        api_base_url="https://iot.meross.com"
    )

    # Initialize at application level
    print("initializing manager...")
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    return http_api_client, manager

