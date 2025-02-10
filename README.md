# Meross IoT API

A Flask-based REST API for monitoring Meross smart plug devices, specifically designed for the MSS315 model. This API provides real-time power consumption data and device status information.

## Features

- Real-time power consumption monitoring
- Device discovery and status checking
- Asynchronous operations for better performance
- RESTful API endpoints
- Support for Meross MSS315 smart plugs

## Prerequisites

- Python 3.7+
- Meross IoT account credentials
- Meross MSS315 smart plug device(s)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/joef-fyp-api.git
cd joef-fyp-api
```

2. Install the required dependencies:

```bash
pip install flask meross-iot
```

3. Create a `cred.py` file with your Meross account credentials:

```python
credentials = {
    "EMAIL": "your.email@example.com",
    "PASSWORD": "your_password"
}
```

## API Endpoints

### GET /api/data

Returns real-time power consumption data from the Meross smart plug.

Response format:

```json
{
  "power": "10.5", // Current power consumption in watts
  "voltage": "230.0", // Current voltage
  "current": "0.045" // Current amperage
}
```

## Project Structure

```
joef-fyp-api/
├── functions/
│   ├── discover_devices.py  # Device discovery and power monitoring logic
│   └── setup.py            # HTTP client and manager setup
├── main.py                 # Main Flask application and route definitions
├── cred.py                 # Credentials configuration (not included in repository)
└── README.md              # Project documentation
```

## Running the Application

Start the Flask server:

```bash
python main.py
```

The server will run on `http://localhost:5000` by default.
Access the API endpoints at `http://localhost:5000/api/data`.

## Security Notes

- Never commit your `cred.py` file to version control
- Store sensitive credentials securely
- Use environment variables for production deployment

## Error Handling

The API includes error handling for common scenarios:

- Device not found (returns default data)
- Connection issues
- Authentication failures
- Invalid credentials

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
