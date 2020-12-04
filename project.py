from flask import Flask, request, url_for, redirect, render_template, send_file, session, make_response
import os, threading, sqlite3, bcrypt
from hashlib import sha256
from datetime import datetime, timedelta
from random import randint

lock = threading.Lock()

# Create Database
DB_NAME = "dev_mentoring.db"

app = Flask(__name__)

#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16메가바이트

salt = bcrypt.gensalt()

app.secret_key = '6rav3_C00k!e Is Str0n93r than Z0m6!3_c00k13'


def gen_hash(user_id):
    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()
    rand = randint(0, 9)
    random_cookie = curr \
        .execute('''SELECT cookie from random_cookie WHERE number = ?''', (rand,)) \
        .fetchone()[0]
    hash = bcrypt.hashpw((user_id + random_cookie).encode(), salt) \
        .decode()
    return hash, rand


def check_session():
    #get cookie, id info
    value = request.cookies.get('session')
    length = int(value[0])
    id = value[1:1+length]
    #get hash for user
    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()
    
    user_log = curr.execute('''
            SELECT * FROM log WHERE user_id = ?
        ''', (id,)) \
            .fetchone()
    if user_log is None:
        return False

    rand = user_log[2]
    random_cookie = curr \
        .execute('''SELECT cookie from random_cookie WHERE number = ?''', (rand,)) \
        .fetchone[0]
    check = user_log[0] + user_log[1] + random_cookie
    # not complete


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/sign_up/')
def sign_up():
    return render_template('sign_up.html')


@app.route('/add_account', methods =['POST'])
def add_account(ID=None, PW=None, PWcheck=None):
    id = request.form['ID']
    pw = request.form['PW']
    pwcheck = request.form['PWcheck']
    if pw != pwcheck: #아이디 존재여부보다 이거먼저하는게 보안에 좀 더 나을듯
        return render_template('pwcheck_fail.html')
    # Account가 존재하는지?
    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()

    account = curr \
        .execute("SELECT id FROM account WHERE id = ?", (id,)) \
        .fetchone()
    if account:
        conn.close()
        return render_template('duplicate_id.html')
    else:
        hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), salt)
        curr.execute("INSERT INTO account VALUES (?, ?)", (id, hashed_pw.decode('utf-8')))
        conn.commit()
        conn.close()
        return redirect(url_for('sign_in'))
    return render_template('wrong_access.html') #위에서 sign_up이 되든 안되든 딴 곳으로 감


@app.route('/sign_in/')
def sign_in():
    return render_template('login.html')


@app.route('/auth', methods = ['POST'])
def auth(ID = None, PW = None):
    id = request.form['ID']
    pw = request.form['PW']
    # Get password from sqlite3 db
    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()
    passwd = curr \
        .execute("SELECT password FROM account WHERE id = ?", (id,)) \
        .fetchone()[0]
    conn.close()
    if bcrypt.checkpw(pw.encode('utf-8'), passwd.encode('utf-8')):
        logged_main_page = make_response(url_for('logged_main_page', user_id = id))
        #set_cookie -> error!
        (hashed_id, rand) = gen_hash(id)
        logged_main_page.set_cookie('session', hashed_id)
        print(hashed_id)
        print(request.cookies.get('session'))
        return redirect(url_for('logged_main_page', user_id = id))

    return render_template('login_fail.html')


@app.route('/main/<user_id>')
def logged_main_page(user_id):
    #session_check(user_id)
    cookie = request.cookies.get('session')
    ret = make_response(render_template('logged_main_page.html', 
        user_id = user_id))
    ret.set_cookie('session', cookie)
    return render_template('logged_main_page.html', 
        user_id = user_id)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main_page'))


@app.route('/main/<user_id>/<board_type>')
def show_board(user_id, board_type):
    session_check(user_id)

    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()
    
    if board_type == 'cookie' or board_type == 'free':
        posts = curr \
            .execute("SELECT * FROM {}_board".format(board_type)) \
            .fetchall()
        conn.close()
        return render_template('show_board.html', 
            user_id = user_id, board_type = board_type, num = len(posts), data = posts)

    return render_template('wrong_access.html')


@app.route('/main/<user_id>/<board_type>/<post_num>')
def show_post(user_id, board_type, post_num):
    session_check(user_id)

    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()

    # try/except because the post which queried can be deleted by the author
    try:
        if board_type == 'cookie' or board_type == 'free':
            post = curr \
            .execute("SELECT * FROM {}_board WHERE number = ?".format(board_type), (post_num,)) \
            .fetchone()
            conn.close()
            return render_template('show_post.html',
                user_id = user_id, board_type = board_type, post_num = post_num, data = post)

        else:
            conn.close()
            return render_template('wrong_access.html')

    except:
        conn.close()
        return render_template('find_post_failure.html',
            user_id = user_id, board_type = board_type)


@app.route('/main/<user_id>/<board_type>/write')
def show_write(user_id, board_type):
    session_check(user_id)
    return render_template('write_post.html', user_id = user_id, board_type = board_type)


@app.route('/main/<user_id>/<board_type>/add_post', methods = ['POST'])
def add_post(user_id, board_type, Title=None, Content=None):
    session_check(user_id)

    lock.acquire()

    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()

    title = request.form['Title']
    content = request.form['Content']
    like = 0
    post_num = 0

    if board_type == 'cookie' or board_type == 'free':
        curr.execute("INSERT INTO {}_board (title, author, like, content) VALUES \
            (?, ?, ?, ?)".format(board_type), (title, user_id, like, content))
        conn.commit()

        # 방금 INSERT한 친구의 number를 갖고오는 SQLite 내장 함수!
        post_num = curr.execute("SELECT LAST_INSERT_ROWID()").fetchone()[0]
    
    conn.close()

    lock.release()
    return redirect(url_for('show_post', 
        user_id = user_id, board_type = board_type, post_num = post_num))


@app.route('/main/<user_id>/<board_type>/rewrite/<post_num>')
def show_rewrite(user_id, board_type, post_num):
    session_check(user_id)

    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()

    post = curr \
        .execute("SELECT * FROM {}_board WHERE number = ?".format(board_type), (post_num,)) \
        .fetchone()
    conn.close()

    if board_type == 'cookie':
        return render_temp/late('rewrite_post.html', 
            user_id = user_id, board_type = board_type, post_num = post_num, data = post)
    elif board_type == 'free':
        return render_template('rewrite_post.html', 
            user_id = user_id, board_type = board_type, post_num = post_num, data = post)
    
    return render_template('wrong_access.html')


@app.route('/main/<user_id>/<board_type>/fix_post/<post_num>', methods = ['POST'])
def fix_post(user_id, board_type, post_num, Title = None, Content = None):
    session_check(user_id)

    conn = sqlite3.connect(DB_NAME)
    curr = conn.cursor()

    title = request.form['Title']
    content = request.form['Content']
    if board_type == 'cookie' or board_type == 'free':
        curr.execute("UPDATE {}_board \
            SET title = ?, content = ? WHERE number = ?".format(board_type), (title, content, post_num))

        conn.commit()
        conn.close()
        return redirect(url_for('show_post', user_id = user_id, board_type = board_type, post_num = post_num))
    
    else:
        return render_template('wrong_access.html')


@app.route('/main/<user_id>/<board_type>/delete/<post_num>', methods = ['POST'])
def delete(user_id, board_type, post_num, Data = None):
    session_check(user_id)
    
    if board_type == 'cookie' or  board_type == 'free':
        conn = sqlite3.connect(DB_NAME)
        curr = conn.cursor()

        curr.execute("DELETE FROM {}_board WHERE number = ?".format(board_type), (post_num,))

        conn.commit()
        conn.close()
        return redirect(url_for('show_board', user_id = user_id, board_type = board_type))
    else:
        return render_template('wrong_access.html')


if __name__ == '__main__':
    app.run(debug = True)