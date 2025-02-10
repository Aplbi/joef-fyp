
from meross_iot.http_api import MerossHttpClient

# setup http client
async def setup_http_client(EMAIL, PASSWORD):
    
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(
        email=EMAIL,
        password=PASSWORD,
        api_base_url="https://iot.meross.com"
    )
    return http_api_client

