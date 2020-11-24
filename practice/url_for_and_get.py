from flask import Flask, url_for, render_template, request, redirect
app = Flask(__name__)

members = {'admin' : 'brave'} # admin account

@app.route('/')
def main_page():
    return redirect('/hello') # redirection이 되는구나!

"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return 'login success'
    return 'login fail'
"""

@app.route('/hello/')
@app.route('/hello/<username>')
def hello(username=None): #유저네임 없을 때 or 있을 때 -> 로그인 하기 전 or 한 후
    return render_template('example_html.html', name=username)

@app.route('/login/') # 여기가 고비구만...
# methods 없이 일단 redirect, args써서 넘겨주면 될 듯!
def login():
    id = request.args.get('id', '')
    password = request.args.get("pw", '')
    if id in members and members[id] == password:
        return redirect(url_for('hello') + id)
    return redirect(url_for('main_page'))
    """
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        elif request.method == 'GET':
            if request.form['username'] in members and request.form['password'] == members[request.form['username']]:
                return redirect(url_for('hello', request.form['username']))
            else:
                print("Wow")
        else:
            error = 'Invalid username/password'
        return render_template('login.html', error = error)
        """
@app.route('/user/<username>')
def profile(username):
    return url_for('login')
"""
with app.test_request_context():
    print(url_for('main_page'))
    print(url_for('login'))
    print(url_for('profile', username = 'Brave Cookie'))
    print(url_for('static', filename='style.css'))
"""
if __name__ == '__main__':
    app.run(debug = True)