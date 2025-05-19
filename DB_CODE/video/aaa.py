import cv2
import torch
import time
from datetime import datetime

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # 또는 'yolov5m', 'yolov5l', 'yolov5x'
model.conf = 0.5  # 감지 확률 threshold

# 감지 기준 인원 수
PERSON_THRESHOLD = 2

# 웹캠 시작
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 모델에 프레임 전달
    results = model(frame)
    detections = results.pandas().xyxy[0]

    # 사람만 필터링
    person_detections = detections[detections['name'] == 'person']
    num_people = len(person_detections)

    # 감지된 사람 수 화면에 표시
    cv2.putText(frame, f'People: {num_people}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0), 2, cv2.LINE_AA)

    # 감지된 객체 박스 그리기
    for _, row in person_detections.iterrows():
        x1, y1, x2, y2 = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # 사람 수가 기준 이상이면 사진 저장
    if num_people >= PERSON_THRESHOLD:
        filename = f'photo_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        cv2.imwrite(filename, frame)
        print(f'[사진 저장] {filename}')
        time.sleep(5)  # 중복 저장 방지용 딜레이

    # 화면 출력
    cv2.imshow('YOLOv5 People Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료 처리
cap.release()
cv2.destroyAllWindows()