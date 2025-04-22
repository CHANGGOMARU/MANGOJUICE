from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from datetime import datetime, timedelta
from DB_open import check_login, make_user

app = FastAPI()



login_attemps = {}
MAX_ATTEMPTS = 5
LOCKOUT_TIMES = timedelta(minutes=5)

def get_client_ip(request: Request) -> str:
    return request.client.host

def is_login_allowed(request: Request, success: bool) -> (bool, HTMLResponse | None):
    now = datetime.now()
    ip = get_client_ip(request)
    attempt = login_attempts.get(ip, {"count": 0, "locked_until": None})

    # 차단된 상태인지 확인
    if attempt["locked_until"] and attempt["locked_until"] > now:
        html = """
        <script>
            alert('로그인 시도가 너무 많습니다. 5분 후 다시 시도해주세요.');
            window.history.back();
        </script>
        """
        return False, HTMLResponse(content=html, status_code=200)

    if success:
        login_attempts.pop(ip, None)
        return True, None

    # 로그인 실패 처리
    attempt["count"] += 1
    if attempt["count"] >= MAX_ATTEMPTS:
        attempt["locked_until"] = now + LOCKOUT_TIME
        html = """
        <script>
            alert('로그인 실패가 5회 초과되었습니다. 5분 후 다시 시도해주세요.');
            window.history.back();
        </script>
        """
    else:
        html = f"""
        <script>
            alert('로그인 실패. 현재 실패 횟수: {attempt["count"]}회');
            window.history.back();
        </script>
        """
    login_attempts[ip] = attempt
    return False, HTMLResponse(content=html, status_code=200)  







@app.get("/")
async def hello_world():
    return "X"

# 로그인 처리 엔드포인트
@app.post("/login")
async def login(id: str = Form(...), passwd: str = Form(...)):
    allowed, response = is_login_allowed(Request, login_success)

    # 여기서 passwd를 SHA-256으로 해시하려면 hashlib 사용 가능
    if check_login(id, passwd):
        return RedirectResponse(url="http://localhost:8080/project/login/reponseLogin_success.jsp", status_code=302)
    else:
        return RedirectResponse(url="http://localhost:8080/project/login/reponseLogin_failure.jsp", status_code=302)

# 회원가입 처리 엔드포인트
@app.post("/register")
async def register(
    userId: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...)
):
    if make_user(userId, password, name, email, phone):
        return RedirectResponse(url="http://localhost:8080/project/login/SessionCreate.jsp", status_code=302)
    else:
        # 단순 alert 창 띄우기 위한 HTML 응답 처리
        html_content = """
        <script>
            alert('회원가입에 실패했습니다.');
            window.history.back();
        </script>
        """
        return HTMLResponse(content=html_content, status_code=200)

