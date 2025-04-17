from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask!'


@app.route('/login', methods=['POST'])
def Login():
    ID = request.form['id']
    Passwd = request.form['passwd']

    # DB_open.py에서 check_login 함수를 가져와서 사용
    from DB_open import check_login

    if check_login(ID, Passwd):
        return redirect('http://localhost:8080/project/login/reponseLogin_success.jsp')
    else:
        return redirect('http://localhost:8080/project/login/reponseLogin_failure.jsp')
    


@app.route('/register', methods=['POST'])
def Register():
    ID = request.form['userId']
    Passwd = request.form['password']
    name = request.form['name']
    email = request.form['email']
    phone_number = request.form['phone']

    # DB_open.py에서 make_user 함수를 가져와서 사용
    from DB_open import make_user

    if make_user(ID, Passwd, name, email, phone_number):
        return redirect('http://localhost:8080/project/login/SessionCreate.jsp')
    else:
        return alert('회원가입 실패', '회원가입에 실패했습니다.')

if __name__ == '__main__':
    app.run(debug=True)