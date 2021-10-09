import re
from django.core.exceptions import ValidationError
import requests,json

def validate_address(value):






    if len(re.findall('[^a-zA-Z\d]',value))>0:
        raise ValidationError('sorry this is not a valid address')


    
    url = 'https://api.ergoplatform.com/api/v0/addresses/'
    response = requests.get(url + value)
    asset = json.loads(response.content.decode())

    for key in asset:
        if key == 'status':
            raise ValidationError('sorry this is not a valid address')
