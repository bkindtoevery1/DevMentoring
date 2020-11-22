from flask import Flask, request, url_for, redirect, render_template, send_file, session
import os, time, threading
import sqlite3

lock = threading.Lock()

# Create Database Session
DB_NAME = "dev_montoring.db"

app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16메가바이트
app.secret_key = b'6rav3_C00k!e Is Str0n93r than Z0m6!3_c00k13'

cookie = {1 : ['떼탈출 언제하지..', 'a', 0, '떼탈출 재밌긴 한데.. 살짝 귀찮음'], 2 : ['그챔 끝!', 'a', 0, '명랑한 쿠키양은 명랑했다.']}
cookie_count = 2
free = {}
free_count = 0
signed_id = None
"""
def check_session(id):
    global signed_id
    if signed_id != id:
        return render_template('wrong_access.html')
""" #이렇게 따로 함수를 불러서 하면 안되는걸까?

def session_check(user_id): #얘는 user_id 받아서 html을 올리라고 해주니 이렇게 함수로 선언해도 괜찮다!
    if not user_id in session['username']:
        return render_template('wrong_access.html')

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/sign_up/')
def sign_up():
    return render_template('sign_up.html')

@app.route('/add_account', methods =['POST', "GET"])
def add_account(ID=None, PW=None, PWcheck=None):
    if request.method == 'GET':
        return render_template('wrong_access.html')
    if request.method == "POST":
        id = request.form['ID']
        pw = request.form['PW']
        pwcheck = request.form['PWcheck']
        if pw != pwcheck: #아이디 존재여부보다 이거먼저하는게 보안에 좀 더 나을듯
            return render_template('pwcheck_fail.html')
        # Account가 존재하는지?
        conn = sqlite3.connect(DB_NAME)
        curr = conn.cursor()

        account = curr \
            .execute(f"SELECT id FROM account WHERE id = '{id}'") \
            .fetchone()
        if account:
            conn.close()
            return render_template('duplicate_id.html')
        else:
            curr.execute(f"INSERT INTO account VALUES ('{id}', '{pw}')")
            conn.commit()
            conn.close()
        return redirect(url_for('sign_in'))
    return render_template('wrong_access.html') #위에서 sign_up이 되든 안되든 딴 곳으로 감

@app.route('/sign_in/')
def sign_in():
    return render_template('login.html')

@app.route('/auth', methods = ['POST', 'GET'])
def auth(ID = None, PW = None):
    if request.method == 'GET':
        pass
    if request.method == "POST":

        id = request.form['ID']
        pw = request.form['PW']
        # Get password from sqlite3 db
        conn = sqlite3.connect(DB_NAME)
        curr = conn.cursor()
        passwd = curr \
            .execute(f"SELECT password FROM account WHERE id = '{id}'") \
            .fetchone()[0]
        conn.close()
        if pw == passwd:
            session['username'] = request.form['ID']
            return redirect(url_for('loggined_main_page', user_id = id))
    return render_template('login_fail.html')

@app.route('/main/<user_id>/')
def loggined_main_page(user_id):
    # 앞으로 나오는 아래 세 줄은 세션 유지를 위한 검사
    session_check(user_id)

    return render_template('loggined_main_page.html', user_id = user_id)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main_page'))

@app.route('/main/<user_id>/<board_type>')
def show_board(user_id, board_type):
    session_check(user_id)

    global cookie, free
    if board_type == 'cookie':
        return render_template('show_board.html',user_id = user_id, board_type = board_type, num = len(cookie), data = dict(sorted(cookie.items(), reverse=True)))
    elif board_type == 'free':
        return render_template('show_board.html',user_id = user_id, board_type = board_type, num = len(free), data = dict(sorted(free.items(), reverse=True)))
    return render_template('wrong_access.html')

@app.route('/main/<user_id>/<board_type>/<post_num>')
def show_post(user_id, board_type, post_num):
    session_check(user_id)

    global cookie, free
    if board_type == 'cookie':
        return render_template('show_post.html',user_id = user_id, board_type = board_type, post_num = post_num, data = cookie[int(post_num)])
    else:
        return render_template('show_post.html',user_id = user_id, board_type = board_type, post_num = post_num, data = free[int(post_num)])

@app.route('/main/<user_id>/<board_type>/write')
def show_write(user_id, board_type):
    session_check(user_id)
    return render_template('write_post.html', user_id = user_id, board_type = board_type)

@app.route('/main/<user_id>/<board_type>/add_post', methods = ['POST'])
def add_post(user_id, board_type, Title=None, Content=None):
    session_check(user_id)

    global cookie, free, cookie_count, free_count
    post = [] #현재 쓴 글에 대한 정보
    title = request.form['Title']
    content = request.form['Content']
    post_num = -1
    if board_type == 'cookie':
        lock.acquire()
        cookie_count += 1
        time.sleep(5)
        post_num = cookie_count
        lock.release()
    elif board_type == 'free':
        lock.acquire()
        free_count += 1
        time.sleep(5)
        post_num = free_count
        lock.release()
    else:
        return render_template('wrong_access.html')
    post.append(title)
    post.append(user_id)
    post.append(0) #처음 쓴 글의 좋아요 수는 0
    post.append(content)
    if board_type == 'cookie':
        cookie[post_num] = post
    else:
        free[post_num] = post
    return redirect(url_for('show_post', user_id = user_id, board_type = board_type, post_num = post_num))

@app.route('/main/<user_id>/<board_type>/rewrite/<post_num>')
def show_rewrite(user_id, board_type, post_num):
    session_check(user_id)

    if board_type == 'cookie':
        return render_template('rewrite_post.html', user_id = user_id, board_type = board_type, post_num = post_num, data = cookie[int(post_num)-1])
    elif board_type == 'free':
        return render_template('rewrite_post.html', user_id = user_id, board_type = board_type, post_num = post_num, data = free[int(post_num)-1])
    return render_template('wrong_access.html')

@app.route('/main/<user_id>/<board_type>/fix_post/<post_num>/<post_index>', methods = ['POST'])
def fix_post(user_id, board_type, post_num, post_index, Title = None, Content = None):
    session_check(user_id)

    title = request.form['Title']
    content = request.form['Content']
    index = int(post_index)
    if board_type != 'cookie' and  board_type != 'free':
        return render_template('wrong_access.html')

    elif board_type == 'cookie':
        cookie[index][0] = title
        cookie[index][3] = content
    else:
        free[index][0] = title
        free[index][3] = content
    return redirect(url_for('show_post', user_id = user_id, board_type = board_type, post_num = post_num))

@app.route('/main/<user_id>/<board_type>/delete/<post_num>', methods = ['POST'])
def delete(user_id, board_type, post_num, Data = None):
    session_check(user_id)
    global cookie, free
    if board_type == 'cookie':
        cookie.pop(int(post_num))
        return redirect(url_for('show_board', user_id = user_id, board_type = board_type))
    elif board_type == 'free':
        free.pop(int(post_num))
        return redirect(url_for('show_board', user_id = user_id, board_type = board_type))
    return render_template('wrong_access.html')

if __name__ == '__main__':
    app.run(debug = True)
