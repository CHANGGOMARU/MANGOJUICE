from flask import Flask, Response
import cv2
import time
from collections import deque
from skimage.metrics import structural_similarity as ssim
import asyncio


FRAME_RATE = 10           # 초당 프레임 수
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

def camera_running():
    while True:
        global frame
        ret, frame = cap.read()
        if not ret:
            print("프레임 캡처 실패.")
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
            print(f"이미지 유사도 (SSIM - 컬러): {similarity:.4f}")


app = Flask(__name__)

def generate_video():
    global frame
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




if __name__ == '__main__':
    asyncio.run(camera_running())
    app.run(debug=True)


