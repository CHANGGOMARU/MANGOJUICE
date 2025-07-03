from flask import Flask, Response
import cv2
import time
from collections import deque
from skimage.metrics import structural_similarity as ssim
import asyncio
import threading
import os
import datetime
from Gemma3_ollama import roll_fallAssistant  # Gemma3_ollama.py의 함수 임포트


FRAME_RATE = 30           # 초당 프레임 수
QUEUE_DURATION = 30       # 초
MAX_FRAMES = FRAME_RATE * QUEUE_DURATION
COMPARE_TIME = 10        # 10초 전 프레임과 비교
SAVE_FRAME_RATE = 6      # 저장할 때의 초당 프레임 수

# 디버그용 프레임 저장 경로
DEBUG_FRAMES_DIR = "debug_frames"

# 프레임 큐 (컬러 프레임 저장)
frame_queue = deque()
# 움직임이 없을 때 저장할 프레임 리스트
Send_frame = []
# 마지막으로 프레임을 저장한 시간을 추적
last_save_time = 0

frame = None

# 디버그 프레임 저장 폴더 생성
if not os.path.exists(DEBUG_FRAMES_DIR):
    os.makedirs(DEBUG_FRAMES_DIR)
    print(f"디버그 프레임 저장 폴더 생성: {DEBUG_FRAMES_DIR}")

# 웹캠 열기
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

print("웹캠에서 캡처 시작...")


def save_frames_to_disk(frames, folder_name=None):
    """디버그용으로 프레임을 디스크에 저장하는 함수"""
    # 타임스탬프로 폴더 이름 생성 (지정된 폴더가 없는 경우)
    if folder_name is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{timestamp}"
    
    # 저장 경로 생성
    save_dir = os.path.join(DEBUG_FRAMES_DIR, folder_name)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 각 프레임 저장
    for i, frame in enumerate(frames):
        filename = os.path.join(save_dir, f"frame_{i:05d}.jpg")
        cv2.imwrite(filename, frame)
    
    print(f"총 {len(frames)}개 프레임을 {save_dir}에 저장했습니다.")
    return save_dir


def noact_check(secondact):
    print(f"\r 같은 프레임 감지 시간: {secondact}초", end="")
    if secondact > 60:
        print("\r \n 일분 이상 움직임 미감지!!!", end="")


secondact = 0
frameact = 0
def camera_running():
    global secondact, frameact, last_save_time, Send_frame
    
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
            
            # secondact가 10 이상이고 마지막 저장 이후 최소 10초가 지났을 때 프레임 저장
            current_time = time.time()
            if secondact >= 10 and (current_time - last_save_time >= 10):
                print(f"\n secondact가 {secondact}초로 10초 이상이므로 프레임 저장합니다.")
                
                # 초당 6프레임만 저장하기 위해 적절한 간격으로 프레임 선택
                # FRAME_RATE(30) / SAVE_FRAME_RATE(6) = 5, 즉 매 5번째 프레임만 선택
                frame_list = list(frame_queue)
                Send_frame = frame_list[::FRAME_RATE//SAVE_FRAME_RATE]
                
                print(f"저장된 프레임 수: {len(Send_frame)} (초당 {SAVE_FRAME_RATE}프레임)")
                
                # 디버그용: 프레임을 디스크에 저장
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                folder_name = f"noact_{secondact}sec_{timestamp}"
                save_dir = save_frames_to_disk(Send_frame, folder_name)
                print(f"디버그용 프레임 저장 완료: {save_dir}")
                
                last_save_time = current_time


def start_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(gemma3_periodic_runner())

async def gemma3_periodic_runner():
    while True:
        try:
            print("[Gemma3] 30초마다 분석 실행...")
            roll_fallAssistant()
        except Exception as e:
            print(f"[Gemma3] 오류 발생: {e}")
        await asyncio.sleep(30)


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

    # asyncio 루프를 별도 스레드에서 실행
    gemma_loop = asyncio.new_event_loop()
    gemma_thread = threading.Thread(target=start_asyncio_loop, args=(gemma_loop,), daemon=True)
    gemma_thread.start()

    camera_running()


