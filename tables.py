import sqlite3, bcrypt


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
    salt = bcrypt.gensalt()
    admin_pw = bcrypt.hashpw('brave'.encode('utf-8'), salt)
    a_pw = bcrypt.hashpw('a'.encode('utf-8'), salt)
    NULL_pw = bcrypt.hashpw('d336132dbbd2be791aed44dfdf1ac806efa8ddcab05faff75b6f412ef387cbd944983da12cce87fe0c485ce0fe35790d44e4a87bb532efdd901a19464f653831'.encode('utf-8'), salt)
    c.execute('''INSERT INTO account VALUES 
        ('admin', ?), 
        ('a', ?),
        ('NULL', ?)
    ''', (admin_pw.decode('utf-8'), a_pw.decode('utf-8'), NULL_pw.decode('utf-8')))
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

    # create table of cookie names
    c.execute('''CREATE TABLE IF NOT EXISTS random_cookie (
        number integer PRIMARY KEY,
        cookie text
    )''')

    c.execute('''INSERT INTO random_cookie (number, cookie) VALUES
        (0, 'brave_cookie'),
        (1, 'moonlight_cookie'),
        (2, 'popping_candy_cookie'),
        (3, 'timekeeper_cookie'),
        (4, 'croissant_cookie'),
        (5, 'space_doughnut'),
        (6, 'sorbet_shark_cookie'),
        (7, 'sea_fairy_cookie'),
        (8, 'cocoa_cookie'),
        (9, 'DJ_cookie')
    ''')

    #create table of logs
    c.execute('''CREATE TABLE IF NOT EXISTS log (
        user_id text PRIMARY KEY,
        datetime text,
        random_cookie integer
    )''')

    conn.commit()

    conn.close()

    print("Create table done!")