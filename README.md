# Alexa API for crypto portfolio
An alexa API for making crypto related queries for every user
Currently only supported for BTC, ETH, LTC with XRP in beta
stack :-
- Using sqlite3 database
- Using flask to register users as well as perform several other requests
- Using blockcypher API for fetch crypto balance at address stored in the database

## tldr how to
- run `databse.py` to make the database
- run `python flask_app.py` to start the app
- make queries such as :  
1. register: `http://127.0.0.1:5000/?action=register&id=99&btc=btc_add&eth=eth_add&ltc=ltc_add&xrp=xrp_add`
2. fetch total balance: `http://127.0.0.1:5000/?action=fetch&id=1`
3. fetch only btc (or some other crypto only) balance: `http://127.0.0.1:5000/?action=fetch&id=1&crypto=btc`
4. fetch crypto news (coming soon)
5. fetch predictions (coming soon)
6. fetch price (coming soon)

## Requirements :-
- python3
- sqlite
- sqlitebrowser (optional to view the db schema in a GUI)

Pip install :-
- flask
<<<<<<< HEAD
- jsonify
- requests
- flask_cors
- flask_api
=======
- json
- requests
>>>>>>> facbff95e19e8ada55f236a083a73a04b853c9fe

![kawaii](https://raw.githubusercontent.com/TimeTraveller-San/alexa-skill-API/master/kawaii.png)
