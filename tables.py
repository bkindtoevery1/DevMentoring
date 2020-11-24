import sqlite3


DB_NAME = "dev_mentoring.db"


if __name__ == "__main__":
    conn = sqlite3.connect(DB_NAME)
    # Create account

    c = conn.cursor()
    # Create account table
    c.execute('''CREATE TABLE IF NOT EXISTS account (
        id text PRIMARY KEY, 
        password text
    )''')
    # 처음에 따옴표 세 개로 하길래 이게 뭐지.. 파이썬에서는 따옴표 세 개면 주석인데 싶었는데..
    # 알고 보니 여러 줄 문자열이었던 것이다!

    # 가계정 insert
    c.execute('''INSERT INTO account VALUES 
        ('admin', 'brave'), 
        ('a', 'a'),
        ('NULL', 'd336132dbbd2be791aed44dfdf1ac806efa8ddcab05faff75b6f412ef387cbd944983da12cce87fe0c485ce0fe35790d44e4a87bb532efdd901a19464f653831')
    ''')
    # NULL의 비밀번호는 NULL...을 SHA-512로 암호화한 것!

    #Create Boards

    #Create free board table
    c.execute('''CREATE TABLE IF NOT EXISTS free_board (
        number integer PRIMARY KEY AUTOINCREMENT, 
        title text, 
        author text, 
        like integer, 
        content text
    )''' )
    
    #Create free board table
    c.execute('''CREATE TABLE IF NOT EXISTS cookie_board (
        number integer PRIMARY KEY AUTOINCREMENT, 
        title text, 
        author text, 
        like integer, 
        content text
    )''' )

    c.execute('''INSERT INTO cookie_board (title, author, like, content) VALUES
        ('떼탈출 언제하지..', 'a', 0, '떼탈출 재밌긴 한데.. 살짝 귀찮음'),
        ('그챔 끝!', 'a', 0, '명랑한 쿠키양은 명랑했다.')
    ''')

    # create meta-datas like global variables

    conn.commit()

    conn.close()

    print("Create table done!")