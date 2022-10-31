from email.utils import collapse_rfc2231_value
import sqlite3


import sqlite3, config


connection = sqlite3.connect(config.DB_FILE)

cursor = connection.cursor()

cursor.execute("""
    DROP TABLE stocK
""" )


cursor.execute("""
    DROP TABLE stock_price
""")

connection.commit