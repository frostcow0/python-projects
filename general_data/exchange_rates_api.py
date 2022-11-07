import requests


response = requests.get("https://api.apilayer.com/exchangerates_data/latest?symbols=EUR&base=USD", headers={'apikey':'EAUx341R7KqgfChSPs02kNJt02SCAXPF'})
print(response)
print(response.json())