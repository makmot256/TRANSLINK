import africastalking
import ssl
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

# Africa's Talking API credentials
username = 'agrigrow'  # Use 'sandbox' for testing in the sandbox environment
api_key = 'use_api_key from Africas Talking'

# Initialize SDK
africastalking.initialize(username, api_key)

# Get the SMS service
sms = africastalking.SMS

# SSL Adapter class for handling SSL/TLS versions
class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version
        super(SSLAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=self.ssl_version,
        )

# Instantiate the adapter with the desired SSL version
adapter = SSLAdapter(ssl_version=ssl.PROTOCOL_TLSv1_2)

# Create a session and mount the adapter
session = requests.Session()
session.mount('https://', adapter)

# Function to send SMS
def send_sms(recipient, message):
    try:
        response = session.post(
            'https://api.africastalking.com/version1/messaging',
            headers={'apiKey': api_key, 'Content-Type': 'application/x-www-form-urlencoded'},
            data={'username': username, 'to': recipient, 'message': message},
            verify=False
        )
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f'Encountered an error while sending SMS: {e}')

# Example usage
send_sms('+256771973013', 'Your produce has arrived')
