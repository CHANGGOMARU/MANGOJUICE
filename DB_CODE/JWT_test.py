from flask import Flask, make_response, redirect
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = 'my-super-secret-key'

@app.route('/Generate')
def generate_and_redirect():
    # JWT 생성
    payload = {
        'id': 'Sparta',
        'passwd' : 'passwd',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'iss': 'flask-server'
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    # 응답 생성 + 쿠키 설정 + JSP 페이지로 리디렉션
    resp = make_response(redirect("http://localhost:8080/project/JWT_test_.jsp"))
    resp.set_cookie("jwt_token", token, httponly=True)
    return resp

if __name__ == '__main__':
    app.run(port=5000)
