from flask import Flask, request, url_for, redirect, render_template, send_file, session

app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16메가바이트
app.secret_key = b'brave_cookie is stronger than zombie_cookie'

accounts = {'admin':'brave', 'a':'a'} #a,a는 빠른 테스트를 위한 가계정
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
        if not id in accounts:
            accounts[id] = pw
        else:
            return render_template('duplicate_id.html')
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
        if id in accounts and accounts[id] == pw:
            # 여기서 session 추가하기 도전~
            session['username'] = request.form['ID']
            return redirect(url_for('session_check'))
            #end 도전~
            #return redirect(url_for('loggined_main_page', user_id = id))
    return render_template('login_fail.html')

@app.route('/session_check')
def session_check():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'></b>" + "click here to log in</b></a>"

@app.route('/main/<user_id>/')
def loggined_main_page(user_id):
    # 앞으로 나오는 아래 세 줄은 세션 유지를 위한 검사
    global signed_id
    if signed_id != user_id:
        return render_template('wrong_access.html')

    return render_template('loggined_main_page.html', user_id = user_id)

@app.route('/logout')
def logout():
    global signed_id
    signed_id = None
    return redirect(url_for('main_page'))

@app.route('/main/<user_id>/<board_type>')
def show_board(user_id, board_type):
    global signed_id
    if signed_id != user_id:
        return render_template('wrong_access.html')

    global cookie, free
    if board_type == 'cookie':
        return render_template('show_board.html',user_id = user_id, board_type = board_type, num = len(cookie), data = dict(sorted(cookie.items(), reverse=True)))
    elif board_type == 'free':
        return render_template('show_board.html',user_id = user_id, board_type = board_type, num = len(free), data = dict(sorted(free.items(), reverse=True)))
    return render_template('wrong_access.html')

if __name__ == '__main__':
    app.run(debug = True)