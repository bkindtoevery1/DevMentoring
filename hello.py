from flask import Flask
app = Flask(__name__)

@app.route('/') # <function Flask.route.<locals>.decorator at ~~>
def show_main():
    ret = '메인 홈페이지</br> <a href="/sign_up">회원가입</a></br> <a href="/sign_in">로그인</a></br> <a href="/board">게시판</a></br>'
    for x in range(1, 11):
        ret += '<a href="/board/%d">%d번 게시판</a></br>' % (x, x)
    return ret #a라는 태그 : href(하이퍼링크 만들어주기)

# <a>회원가입</a> : a태그 안에 회원가입이라는 글자 포함.
# a는 변수명이 아니라 하이퍼링크를 만들어주는 태그!

@app.route('/sign_up')
def show_sign_up():
    return '회원가입 페이지'

@app.route('/sign_in')
def show_sign_in():
    return '로그인 페이지</br> <a href="/sign_up">회원가입</a>'

@app.route('/board/<number>') # 여기 number를 함수로 넘겨줌
def show_board_with_num(number):
    return 'Post %s' % number

if __name__ == '__main__':
    app.run()

# 4번 라인부터 6번 라인까지는 app.route('/')(hello_world)와 동일하다.
# 그래서 hello = app.route('/')(hello_world) 하고
# hello.run()하면 잘 됨!

# 과제
# 1. 다음주까지 지금가지 배운거로 스토리보드 구현해보기!
# 2. https://www.w3schools.com/html/default.asp 여기에서 html 태그 참고하기!