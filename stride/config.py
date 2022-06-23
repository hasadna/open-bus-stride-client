import os


STRIDE_API_BASE_URL = (os.environ.get('STRIDE_API_BASE_URL') or 'https://open-bus-stride-api.hasadna.org.il').rstrip('/')
URBANACCESS_DATA_PATH = os.environ.get('URBANACCESS_DATA_PATH') or '.data/urbanaccess'
