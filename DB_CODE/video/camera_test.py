import cv2
import time
from collections import deque
from skimage.metrics import structural_similarity as ssim

# 설정값
FRAME_RATE = 10           # 초당 프레임 수
QUEUE_DURATION = 30       # 초
MAX_FRAMES = FRAME_RATE * QUEUE_DURATION
COMPARE_TIME = 10         # 10초 전 프레임과 비교

# 프레임 큐 (컬러 프레임 저장)
frame_queue = deque()

# 웹캠 열기
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

print("웹캠에서 캡처 시작...")

try:
    while True:
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

        # 화면 출력
        cv2.imshow("Live Feed", frame_resized)

        # 종료 조건 (q 키)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("종료 키 입력됨. 종료합니다.")
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
