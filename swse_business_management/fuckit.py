import sqlite3

con = sqlite3.connect("swsebm.db")


def add_session_id_to_transactions():
    con.execute('''
    CREATE TABLE temp (
        transaction_id INTEGER PRIMARY KEY,
        session_id INTEGER,
        trans_type TINYINT,
        client_name VARCHAR(40),
        item VARCHAR(40),
        quantity INTEGER,
        price INTEGER,
        FOREIGN KEY (session_id) REFERENCES sessions(session_id)
    )
    ''')

    con.execute('''
    INSERT INTO temp (trans_type, client_name, item, quantity, price)
    SELECT trans_type, client_name, item, quantity, price
    FROM transactions
    ''')

    con.execute("""
    UPDATE temp
    SET session_id = 1
    """)

    con.execute("COMMIT")

con.execute("UPDATE transactions SET item = 'GLITTERSTIM' WHERE item = 'GLITTERSTEM'")
con.execute("COMMIT")
