def my_deco(f):
    def inner():
        print("start")
        ret = f()
        print("end")
        return ret
    return inner

@my_deco
def c():
    print("I'm c!")

# >>> c() 출력 결과는
# start
# I'm c!
# end

# 데코레이터는 함수를 parameter로 하는 함수라고 생각할 수 있다!
# 데코레이터도 함수의 일종인듯.