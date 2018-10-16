import json, urllib.request
from flask import Flask,jsonify,request,send_file
from flask_api import status
from flask_cors import CORS
import os
import requests
import sqlite3

DATABASE = 'crypto_db.db'


def connect_db():
    return sqlite3.connect(DATABASE)

g = connect_db()
g_db = g.cursor()
query = 'SELECT * FROM crypto WHERE id=?'
query2 = 'SELECT * FROM crypto'
# cur = g_db.execute(query, d)
# x = cur.fetchone()


# data = ("111", "asjb1234h12832k3h4")
# sql = '''INSERT INTO crypto(id,address) VALUES(?,?) '''
# g_db.execute(sql, data)
# g.commit()
<<<<<<< HEAD
# cur = g_db.execute(query,(1,))
cur = g_db.execute(query2)
x = cur.fetchall()
=======
cur = g_db.execute(query,(1,))
x = cur.fetchone()
>>>>>>> facbff95e19e8ada55f236a083a73a04b853c9fe
for a in x:
    if a:
        print(a)
