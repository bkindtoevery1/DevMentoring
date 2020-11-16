from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def main_menu():
    dic={'a':1, 'b':2, 'c':3}
    return render_template('get_dic.html', data=dic)

@app.route('/check', methods = ['POST'])
def check(data = None):
    if request.method == 'POST':
        Data = request.form['data']
    for key, value in Data:
        print(key, value)

if __name__ == '__main__':
    app.run(debug = True)