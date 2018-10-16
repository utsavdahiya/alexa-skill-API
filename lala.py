# import blockcypher
# a = blockcypher.get_address_details('3MuR2ZgNtfRrkSvAnLewr4uQJiDYdhi2pU','ltc')
# print(a['balance'])
import requests, json
def fetch_price(crypto):
    url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto}&tsyms=USD,JPY,EUR"
    response = requests.get(url)
    data = json.loads(response.content)
    return data['USD']

print(fetch_price('ETH'))
print(fetch_price('BTC'))
print(fetch_price('LTC'))
