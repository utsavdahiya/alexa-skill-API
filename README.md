# Alexa API for crypto portfolio
An alexa API for making crypto related queries for every user
Currently only supported for BTC, ETH, LTC with XRP in beta
stack :-
- Using sqlite3 database
- Using flask to register users as well as perform several other requests
- Using blockcypher API for fetch crypto balance at address stored in the database

## tldr how to use
Currently setup is at http://alexaskill.pythonanywhere.com/  
Account independent features :-  
1. Price fetch  
  http://alexaskill.pythonanywhere.com/?action=price&crypto=[CRYPTO]
  replace [CRYPTO] with btc, eth, doge, ltc, xrp, anything... 
  resposne will be a JSON with three fields :-
    1. change: change in the price in last 24 hours in USD
    2. price: current price of crypto in USD
    3. price_old: price 24 hours ago in USD

2. Market cap  
  http://alexaskill.pythonanywhere.com/?action=cap&crypto=[CRYPTO]  
    replace [CRYPTO] with btc, eth, doge, ltc, xrp, anything...   
    reponse will be a single field:-  
      1. cap: the total amount of coins in market. Speak this in millions/billions
      2. cap in USD: market cap in USD
      3. crypto: the name of crypto

3. Crypto news       
  http://alexaskill.pythonanywhere.com/?action=news    
  will have a single field:  
    1. news: its an array of strings which are the news headlines
     THIS IS NOT WORKING ON PYTHONANYWHERE AS THEY BAN THIRD PARTY https URLs, fix coming by sunset today

Account dependent features:-  
NOTE: for testing purpose use ALEXA_ID = 1, i have added this to the database, it will get your results. In other cases, replace the alexa ID by the actual alexa ID, if its registered you will get a response, if not you won't get any response in that case say "Sorry you are not registerd with us, please register your alexa id on the link written in description".
I am handling the registration process so dont worry about it, for now assume ID=1 is registered with all four addresses in our database. 

1. fetch value of porfolio:   
  http://alexaskill.pythonanywhere.com/?action=fetch&id=[ALEXA ID]&crypto=[CRYPTO_LIMITED]  
  replace [ALEXA_ID] with alexa_id, dahiya should know how to get it. For testing use id = 1  
  replace [CRYPTO_LIMITED] with :-  
    1. all: fetch the value of the complete portfolio, all of it
    2. btc: fetch the amount of bitcoins held
    3. eth: fetch the amount of ether held
    4. ltc: same
    5. doge: same
  the reponse will have :-  
    1. balance: total balance in USD
    2. x: number of crypto x held
    3. x_usd: amount of cryptp held in USD
    4. id: alexa ID of user

2. unconfirmed transactions  
  http://alexaskill.pythonanywhere.com/?action=unconfirmed&id=[ALEXA_ID]  
  replace [ALEXA_ID] with alexa_id, dahiya should know how to get it. For testing use id = 1
  reponse will have the follwing fields :-  
    1. btc: no of btc unconfirmed transactions
    2. doge: no of doge...
    3. ltc: no of...
    5. eth: ...
    5. total: total unconfirmed transactions
   tip: first speak the total uncofimed transactions then speak only the non zero uncofimed for example: "you have 4 total unconfirmed      transactions, 2 bitcoin, 1 ethereum and 1 doge" 

3. Register new user  
  http://alexaskill.pythonanywhere.com/?action=register&id=[ALEXA_ID]&btc=ayy&eth=ayy&ltc=ayy&doge=ayy2   
  DONT BOTHER WITH IT, I AM HANDLING THIS  
  it will register the [ALEXA_ID] with the btc address ayy, eth address ayy, ltc address ayy, doge address ayy2 on our databse and then can be used by above API features. 

  

## tldr how to set up 
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
