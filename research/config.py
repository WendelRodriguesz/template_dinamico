import json
from services.data import Information

config = Information().get_data_from_json('credentials.json')
EMAIL = config.get('EMAIL')
EMAIL_PASSWORD = config.get('EMAIL_PASSWORD')
