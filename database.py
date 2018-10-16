import sqlite3 as lite
import sys
import os

crypto = (
    ('1','1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD','0x61b21c6ee787bc1df5ef873e5f6809711c62ab92','3MuR2ZgNtfRrkSvAnLewr4uQJiDYdhi2pU', 'DMYiX1DNzVMKKkYcESTN3MeGM2StU2Shxn'),
    ('2','23EP8i3QJCsomS4BSMY2RpU1upv62aGvhD','0x61asd1c6ee787bc1df5ef873e5f6809711c62ab92','3MuRasd2ZgNtfRrkSvAnLewr4uQJiDYdhi2pU', 'test'),
    ('3','1sEP8i3QJCsomS4BSMY2RpU1upv62aGvhD','0x61basdasdc6easde787bc1df5ef873e5f6809711c62ab92','3MuR2ZgNtfRrkSvAnLewr4uQJiDYdhi2pU','None'),
    ('4','8DEP8i3asdQJCsomS4BSMY2RpU1upv62aGvhD','0x61b212390ee787bc1df5ef873e5f6809711c62ab92','3MuR2ZgNtfRrkSvAnLewr4uQJiDYdhi2pU', 'None'),
)
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = basedir+'/crypto_db.db'
con = lite.connect(DATABASE)

with con:
    create_table = """CREATE TABLE IF NOT EXISTS crypto (id text PRIMARY KEY, btc text , eth text , ltc text, doge text )"""
    sql = '''INSERT INTO crypto(id,btc,eth,ltc,doge) VALUES(?,?,?,?,?) '''
    create_table = """CREATE TABLE IF NOT EXISTS crypto (id text PRIMARY KEY, btc text , eth text , ltc text, doge text )"""
    sql = '''INSERT INTO crypto(id,btc,eth,ltc,doge) VALUES(?,?,?,?,?) '''
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS crypto')
    cur.execute(create_table)
    for data in crypto:
        cur.execute(sql, data)
    con.commit()
