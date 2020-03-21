import requests
import json

data_url = "https://mattblackworld.com/api/countries"
        
req = requests.get(data_url)
response = json.loads(req.text)

print(len(response))