import sqlite3
from tkinter import E
import alpaca_trade_api as tradeapi
import config

# Creating connection into a sqlite database and geting data from the alpaca api
connection = sqlite3.connect('/Users/king_michael/projects/Trading_app/app.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, company FROM stock
""")

rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]

api = tradeapi.REST(config.API_KEY_ID, config.SECRET_KEY, config.BASE_URL)
assets = api.list_assets()

# looping each assets from list of assets.
for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()
