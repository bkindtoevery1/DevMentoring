import sqlite3


DB_NAME = "dev_montoring.db"


if __name__ == "__main__":
    conn = sqlite3.connect(DB_NAME)
    # Create account

    c = conn.cursor()
    # Create account table
    c.execute('''CREATE TABLE IF NOT EXISTS account (id text, password text)''')

    # 가계정 insert
    c.execute('''INSERT INTO account VALUES ('admin', 'brave'), ('a', 'a')''')

    conn.commit()

    conn.close()

    print("Create table done!")
