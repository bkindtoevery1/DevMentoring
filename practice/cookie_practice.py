from flask import Flask, request, url_for, make_response, redirect

app = Flask(__name__)

@app.route('/')
def main():
	ret = make_response(url_for('cookie_check'))
	ret.set_cookie('username', 'cookie')
	return redirect(url_for('cookie_check'))

@app.route('/check')
def cookie_check():
	if request.cookies.get('username') == 'cookie':
		return "success!"
	else:
		return "fail.."

if __name__ == '__main__':
	app.run(debug = True)