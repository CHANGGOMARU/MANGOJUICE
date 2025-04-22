import time
from flask import request

# 설정 값
MAX_ATTEMPTS = 5
BLOCK_TIME = 5 * 60  # 5분

# 내부 기록 저장
login_attempts = {}

def get_block_time_remaining(ip):
    current_time = time.time()
    record = login_attempts.get(ip)
    if record and record.get('blocked_until', 0) > current_time:
        return int(record['blocked_until'] - current_time)
    return 0

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

def is_ip_blocked(ip):
    current_time = time.time()
    record = login_attempts.get(ip)

    if record and current_time < record.get('blocked_until', 0):
        return True
    return False

def record_failed_attempt(ip):
    current_time = time.time()
    record = login_attempts.setdefault(ip, {'count': 0, 'last_failed': 0, 'blocked_until': 0})
    record['count'] += 1
    record['last_failed'] = current_time

    if record['count'] >= MAX_ATTEMPTS:
        print("IP 차단 발생 : 차단 IP : " + str(ip))
        record['blocked_until'] = current_time + BLOCK_TIME
    print(str(record['count']) + "회")
    print(str(ip))

def reset_ip_record(ip):
    login_attempts[ip] = {'count': 0, 'last_failed': 0, 'blocked_until': 0}