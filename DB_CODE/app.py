from flask import Flask, request, redirect, session, make_response
from flask_cors import CORS  # CORS를 처리하기 위한 모듈 추가
from DB_open import *
from DB_open import get_user_info  # get_user_info 함수 가져오기
from login_check import *
import time
import datetime
import jwt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션 암호화를 위한 키

# JWT 비밀키 (JSP에서도 동일한 키로 검증해야 함)
SECRET_KEY = 'my-super-secret-key'


# CORS 설정 개선
CORS(app, 
     resources={r"/*": {"origins": "http://127.0.0.1:8080"}}, 
     supports_credentials=True, 
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"])


#로그인 받아오기 / 정보확인 / 결과 전송 매커니즘
@app.route('/debug/login_fail')
async def Login_fail_five():
    ip = get_client_ip()
    for i in range(5):
        record_failed_attempt("127.0.0.1")
    return redirect('http://127.0.0.1:8080/project/login/sessionCreate.jsp')


@app.route('/login', methods=['POST'])
async def Login():
    ip = get_client_ip()
    if is_ip_blocked(ip):
        remaining = get_block_time_remaining(ip)
        minutes = remaining // 60
        return f"이 IP는 로그인 시도 제한으로 인해 차단되었습니다. 남은 시간: {minutes}분", 403

    ID = request.form['id']
    Passwd = request.form['passwd']
  
    if check_login(ID, Passwd):
        # 쿠키 설정 개선
        reset_ip_record(ip)

        user_infomation = get_user_info(ID,Passwd)


        print(user_infomation['name'])

        payload = {
        'id': user_infomation['ID'],
        'passwd' : user_infomation['Passwd'],
        'name' : user_infomation['name'],
        'age' : user_infomation['age'],
        'name' : user_infomation['name'],
        'email' : user_infomation['email'],
        'phone_number' : user_infomation['phone_number'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'iss': 'flask-server'
    }



        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        resp = make_response(redirect('http://127.0.0.1:8080/project/login/reponseLogin_success.jsp'))
        resp.set_cookie("jwt_token", token, httponly=True)
        return resp
    else:
        record_failed_attempt(ip)
        return redirect('http://127.0.0.1:8080/project/login/reponseLogin_failure.jsp')
    


# 회원가입 받아오기 / 결과 출력 매커니즘

@app.route('/register', methods=['POST'])
async def Register():
    ID = request.form['userId']
    Passwd = request.form['password']
    name = request.form['name']
    email = request.form['email']
    phone_number = request.form['phone']

    if make_user(ID, Passwd, name, email, phone_number):
        return redirect('http://127.0.0.1:8080/project/login/SessionCreate.jsp')
    else:
        return alert('회원가입 실패', '회원가입에 실패했습니다.')
    



if __name__ == '__main__':
    app.run(debug=True)