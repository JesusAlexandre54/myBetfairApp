import requests
import json

username = "tan.olive@bol.com.br"
pw = "@Duda150613"
app_key = "yIfCUygZyO0iXBM2"
SSOID = 'k3XXMtVBLeP/qQkOd9RsAAR6SMH3JzmgVMzoLiamtXk='

endpoint = "https://api.betfair.com/exchange/betting/rest/v1.0/"
header = {'X-Application': app_key,	'X-Authentication': SSOID, 'content-type': 'application/json'}
json_req = '{"filter":{ }}'
url = endpoint + "listEventTypes/"

response = requests.post(url, data=json_req, headers=header)

print(json.dumps(json.loads(response.text), indent=3))
