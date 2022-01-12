# 리스트 s의 모든 요소에 제곱값을 가지는 새로운 리스트 생성 예제
s = [1, 2, 3, 4, 5]

# 1. 일반 파이썬 프로그래밍
def make_square(s) :
    r = []
    for i in s :
        r.append(i * i)
    return r

for i in make_square(s) :
    print(i, end=' ')
print()

# 2. 함수를 일급 객체로 취급하는 map을 이용한 프로그래밍
def square(x) :
    return x * x

m = map(square, s)    # map 객체는 함수, 리스트를 보관

for i in m :
    print(i, end=' ')
print()