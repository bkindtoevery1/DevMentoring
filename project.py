from flask import Flask, request, url_for, redirect, render_template, send_file, session
import os, time, threading, sqlite3, bcrypt

lock = threading.Lock()

# Create Database
DB_NAME = "dev_mentoring.db"

app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16메가바이트

app.secret_key = b'6rav3_C00k!e Is Str0n93r than Z0m6!3_c00k13'
salt = bcrypt.gensalt()

def session_check(user_id): #얘는 user_id 받아서 html을 올리라고 해주니 이렇게 함수로 선언해도 괜찮다!
    try:
        if user_id in session['username']:
            return True
    except:
         return render_template('wrong_access.html')


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
        session['username'] = id
        return redirect(url_for('loggined_main_page', 
            user_id = id))

    return render_template('login_fail.html')


@app.route('/main/<user_id>/')
def loggined_main_page(user_id):
    session_check(user_id)
    return render_template('loggined_main_page.html', 
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
        .execute("SELECT * FROM ?_board ", (board_type)) \
        .fetchall()
        conn.close()
        print(posts)
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
            .execute("SELECT * FROM ?_board WHERE number = ?", (board_type, post_num)) \
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
        curr.execute("INSERT INTO ?_board (title, author, like, content) VALUES \
            (?, ?, ?, ?)", (board_type, title, user_id, like, content))
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
        .execute("SELECT * FROM ?_board WHERE number = ?", (board_type, post_num)) \
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
        curr.execute("UPDATE ?_board \
            SET title = ?, content = ? WHERE number = ?", (board_type, title, content, post_num))

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

        curr.execute("DELETE FROM ?_board WHERE number = ?", (board_type, post_num))

        conn.commit()
        conn.close()
        return redirect(url_for('show_board', user_id = user_id, board_type = board_type))
    else:
        return render_template('wrong_access.html')


if __name__ == '__main__':
    app.run(debug = True)