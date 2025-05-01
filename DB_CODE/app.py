from flask import Flask, request, redirect, url_for
from DB_open import check_login,  make_user
from login_check import get_client_ip, is_ip_blocked, record_failed_attempt, reset_ip_record, get_block_time_remaining
import time
app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello, Flask!'


@app.route('/Welcome_world')
def welcomepage():
    return redirect('http://localhost:8080/project/welcome/session.jsp')



#로그인 받아오기 / 정보확인 / 결과 전송 매커니즘
@app.route('/debug/login_fail')
async def Login_fail_five():
    ip = get_client_ip()
    for i in range(5):
        record_failed_attempt("127.0.0.1")
    return redirect('http://localhost:8080/project/login/sessionCreate.jsp')



@app.route('/login', methods=['POST'])
async def Login():
    ip = get_client_ip()
    if is_ip_blocked(ip):
        remaining = get_block_time_remaining(ip)
        minutes = remaining // 60
        return f"이 IP는 로그인 시도 제한으로 인해 차단되었습니다. 남은 시간: {minutes}분", 403

    ID = request.form['id']
    Passwd = request.form['passwd']
    #혹시모르니까 쓰는건데 passwd 받을때 이거 한번 sha-256으로 변환한번 하는게 낫겠지? 

    #이거 쿠키나 세션 적용되는지 확인해봐야 할거 같기도 한데 될지 모르것다. 미래의 내가 테스트 해주겠지지
    if check_login(ID, Passwd):
        reset_ip_record(ip)
        return redirect('http://localhost:8080/project/login/reponseLogin_success.jsp')
    else:
        record_failed_attempt(ip)
        return redirect('http://localhost:8080/project/login/reponseLogin_failure.jsp')
    


# 회원가입 받아오기 / 결과 출력 매커니즘

@app.route('/register', methods=['POST'])
async def Register():
    ID = request.form['userId']
    Passwd = request.form['password']
    name = request.form['name']
    email = request.form['email']
    phone_number = request.form['phone']

    if make_user(ID, Passwd, name, email, phone_number):
        return redirect('http://localhost:8080/project/login/SessionCreate.jsp')
    else:
        return alert('회원가입 실패', '회원가입에 실패했습니다.')

if __name__ == '__main__':
    app.run(debug=True)