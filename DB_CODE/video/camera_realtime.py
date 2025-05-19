from flask import Flask, Response
import cv2
import time
from collections import deque
from skimage.metrics import structural_similarity as ssim
import asyncio
import threading


FRAME_RATE = 30           # 초당 프레임 수
QUEUE_DURATION = 30       # 초
MAX_FRAMES = FRAME_RATE * QUEUE_DURATION
COMPARE_TIME = 10        # 10초 전 프레임과 비교


# 프레임 큐 (컬러 프레임 저장)
frame_queue = deque()

frame = None

# 웹캠 열기
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

print("웹캠에서 캡처 시작...")



def noact_check(secondact):
    print(f"\r 같은 프레임 감지 시간: {secondact}초", end="")
    if secondact > 60:
        print("\r \n 일분 이상 움직임 미감지!!!", end="")


secondact = 0
frameact = 0
def camera_running():
    while True:
        global frame

        ret, frame = cap.read()
        if not ret:
            print("프레임 캡처 실패. 웹캠이 연결되었는지 확인하세요.")
            break

        # 프레임 리사이즈 (성능 고려)
        frame_resized = cv2.resize(frame, (320, 240))

        # 일정한 프레임 속도로 제한
        time.sleep(1 / FRAME_RATE)

        # 프레임 큐에 저장
        frame_queue.append(frame_resized)

        # 큐 길이가 30초 분량을 초과하면 가장 오래된 프레임 삭제
        if len(frame_queue) > MAX_FRAMES:
            frame_queue.popleft()

        # 10초 전 프레임과 현재 프레임 비교
        if len(frame_queue) >= COMPARE_TIME * FRAME_RATE:
            # 10초 전 프레임을 꺼내서 비교
            past_frame = frame_queue[-COMPARE_TIME * FRAME_RATE]  # 10초 전 프레임
            similarity, _ = ssim(past_frame, frame_resized, channel_axis=-1, full=True)
            if similarity >= 0.94:
                frameact += 1
                if frameact >= FRAME_RATE:
                    secondact += 1
                    frameact = 0
            else:
                frameact = 0
                secondact = 0
            noact_check(secondact)
            


    

app = Flask(__name__)





def generate_video():
    global frame
    while True:
        if frame is not None:
            _, encoded_image = cv2.imencode('.jpg', frame)
            frame_bytes = encoded_image.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '<img src="/video_feed">'

def start_flask():
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    camera_running()


