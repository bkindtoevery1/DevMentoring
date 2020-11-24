from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_menu():
    num = 1
    return render_template('get_var.html', number = num)

if __name__ == '__main__':
    app.run(debug = True)