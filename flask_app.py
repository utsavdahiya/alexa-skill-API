import json
from flask import Flask,jsonify,request,send_file
from flask_api import status
from flask_cors import CORS
import os
import requests
import sqlite3
import bs4
import datetime
import time

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = basedir+'/crypto_db.db'

app = Flask(__name__)
app.config.from_object(__name__)

def get_news():
    hdr = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get("https://news.google.com/search?q=cryptocurrency", headers=hdr)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    headings = soup.body.find_all('p', attrs={'class': ["HO8did" ,"Baotjf"]})
    response = {}
    news = []
    for heading in headings:
        news.append(heading.text.strip())
    response['news'] = news
    return jsonify(response)

def c_get_uncomfirmed(crypto, address):
    if not address:
        return 0
    url = f"https://api.blockcypher.com/v1/{str(crypto)}/main/addrs/{str(address)}/balance"
    response = requests.get(url)
    data = json.loads(response.content)
    try:
        data['unconfirmed_n_tx']
    except:
        return 0
    return data['unconfirmed_n_tx']

def get_uncomfirmed(id):
    db = connect_db()
    cursor = db.cursor()
    query = 'SELECT * FROM crypto WHERE id=?'
    q = cursor.execute(query, (id,))
    addresses = q.fetchone()
    if not addresses:
        return jsonify({'response':'user does not exist'})
    total = 0
    cryptos = ['btc', 'eth', 'ltc', 'doge']
    response = {}
    for crypto, address in zip(cryptos,addresses[1:]):
        response[crypto] = c_get_uncomfirmed(crypto, address)
        total += response[crypto]
    response['total'] = total
    return jsonify(response)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def fetch_price(crypto, flag = 0, currency = 'USD'):
    if not flag:
        return 0
    url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto}&tsyms=USD,JPY,EUR"
    response = requests.get(url)
    data = json.loads(response.content)
    return data[currency]

def get_balance(crypto, address):
    if not address:
        return jsonify({'response':'user does not exist'})
    url = f"https://api.blockcypher.com/v1/{str(crypto)}/main/addrs/{str(address)}/balance"
    response = requests.get(url)
    data = json.loads(response.content)
    factors = {'btc':8, 'eth':18, 'ltc':8, 'doge':8}
    factor = factors[crypto]
    try:
        data['balance']
    except:
        return 0
    return data['balance']/10**factor

def fetch_value(id, crypto):
    db = connect_db()
    cursor = db.cursor()
    query = 'SELECT * FROM crypto WHERE id=?'
    q = cursor.execute(query, (id,))
    C = ['btc', 'eth', 'ltc', 'doge']
    addresses = q.fetchone()
    if not addresses:
        return jsonify({'response':'user does not exist'})
    if(crypto == "all"):
        cryptos = C
    else:
        cryptos = [crypto]
        addresses = [addresses[0],addresses[C.index(crypto) + 1]]
    value = 0
    response = {'id' : id}
    for crypto, address in zip(cryptos, addresses[1:]):
        b = get_balance(crypto, address)
        response[crypto] = b
        p = fetch_price(crypto.upper(), flag = address)
        response[crypto+'_USD'] = b*p
        value += b*p
    response['balance'] = value
    return jsonify(response)

def register(data):
    db = connect_db()
    cursor = db.cursor()
    sql = '''INSERT OR REPLACE INTO crypto(id, btc, eth, ltc, doge) VALUES(?,?,?,?,?) '''
    cursor.execute(sql, data)
    db.commit()
    return jsonify({'response':'new user registered'})

def return_price(crypto):
    crypto = crypto.upper()
    timestamp = int(time.time())
    timestamp_old = timestamp - 86400
    url = f"https://min-api.cryptocompare.com/data/pricehistorical?fsym={crypto}&tsyms=USD&ts={int(timestamp)}"
    response = requests.get(url)
    data = json.loads(response.content)
    current_price = data[crypto]['USD']
    url = f"https://min-api.cryptocompare.com/data/pricehistorical?fsym={crypto}&tsyms=USD&ts={int(timestamp_old)}"
    response = requests.get(url)
    data = json.loads(response.content)
    old_price = data[crypto]['USD']
    response = {'price' : current_price, 'price_old' : old_price, 'change' : current_price-old_price}
    return jsonify(response)

def market_cap(crypto):
    url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={crypto.upper()}&tsyms=USD"
    response = requests.get(url)
    data = json.loads(response.content)
    # current_price = data[crypto]['USD']
    print(data)
    cap = data['DISPLAY'][crypto.upper()]['USD']['MKTCAP']
    response = {"cap" : cap}
    return jsonify(response)

def get_index(date):
    if not date :
        return
    elif date == "tommorrow":
        return 1
    elif date == 'day_after':
        return 2
    else:
        date = datetime.datetime.strptime(date, "%d/%m/%Y")
        current_date = datetime.datetime.today()
        index = (date - current_date).days + 1
        if index > 1 and index < 29 :
            return index
    return

def get_prediction(crypto, date):
    index = get_index(date)
    if not index:
        return jsonify({'prediction':"invalid date"})
    file = str("/" +crypto) + '_predictions.csv'
    with open(basedir + file, 'r') as handle:
        data = handle.read()
    prediction = data.split('\n')[index].split(',')[2]
    price = "{:.2f}".format(float(prediction))
    response = {'prediction':price, 'days_from_now':index, 'crypto':crypto}
    return jsonify(response)

CORS(app)
@app.route("/",methods=['GET'])
def index():
    id = request.args.get('id')
    action = request.args.get('action')
    crypto = request.args.get('crypto')
    if action == "fetch":
        return fetch_value(id, crypto)
    if action == "register":
        data = (
        id,
        request.args.get('btc'),
        request.args.get('eth'),
        request.args.get('ltc'),
        request.args.get('doge'),
        )
        return register(data)
    if action == 'unconfirmed':
        return get_uncomfirmed(id)
    if action == 'news':
        return get_news()
    if action == "price":
        return return_price(crypto)
    if action == 'cap':
        return market_cap(crypto)
    if action == 'predict':
        date = request.args.get('date')
        return get_prediction(crypto, date)
    return "up and running"


# http://127.0.0.1:5000/?action=fetch&id=1&crypto=all
# http://127.0.0.1:5000/?action=fetch&id=1&crypto=eth
# http://127.0.0.1:5000/?action=unconfirmed&id=1
# http://127.0.0.1:5000/?action=price&crypto=btc
# http://127.0.0.1:5000/?action=cap&crypto=btc
# http://127.0.0.1:5000/?action=news&crypto=btc
# http://127.0.0.1:5000/?action=register&id=123&btc_addy=thislongshittieraddyisthenewaddyman
# http://127.0.0.1:5000/?action=register&id=666&btc=ayy&eth=ayy&ltc=ayy&doge=ayy2
# http://127.0.0.1:5000/?action=predict&date=21/10/2018&crypto=btc
# http://127.0.0.1:5000/?action=register&id=kumar.vaibhav_1o1@gmail.com&btc=ayy&eth=ayy&ltc=ayy&doge=ayy2
if __name__ == "__main__":
    app.run()
