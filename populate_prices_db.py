import sqlite3, config
from alpaca_trade_api import REST, TimeFrame
import alpaca_trade_api as tradeapi


connection = sqlite3.connect(config.DB_FILE)

connection.row_factory = sqlite3.Row


cursor = connection.cursor()

cursor.execute("""
    SELECT id, symbol, name FROM stock
""")

rows = cursor.fetchall()

stock_symbols = []
stock_dict = {}

for row in rows:
    symbol = row['symbol']
    stock_symbols.append(symbol)
    stock_dict[symbol] = row['id']

# api = tradeapi.REST(config.POLYGON_API, config.SECRET_KEY, config.BASE_URL)
api = REST(config.API_KEY_ID, config.SECRET_KEY, config.BASE_URL)

call_size = 200

for i in range(0, len(stock_symbols), call_size):
    symbol_size = stock_symbols[i:i+call_size]

    barsets = api.get_bars(symbol_size, TimeFrame.Day, "2022-10-01")._raw

    for bar in barsets:
        name_symbol = bar["S"]
        print(f"processing symbol {name_symbol}")
        stock_id = stock_dict[bar["S"]]
        cursor.execute("""
            INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)               
        """, (stock_id, bar['t'], bar['o'], bar['h'], bar['l'], bar['c'], bar['v']))

connection.commit()
