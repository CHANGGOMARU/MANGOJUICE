
import cv2
import torch
import time
from datetime import datetime
import asyncio

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.conf = 0.5  # 감지 정확도 기준

# 웹캠 시작
cap = cv2.VideoCapture(0)

# 직전 프레임의 사람 수를 기억할 변수
 # 처음에는 아무 값도 없는 상태로 시작
async def run():
    prev_num_people = -1 
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # YOLO에 현재 프레임 전달
        results = model(frame)
        detections = results.pandas().xyxy[0]

        # 사람만 필터링
        person_detections = detections[detections['name'] == 'person']
        num_people = len(person_detections)

        # 화면에 현재 사람 수 출력
        cv2.putText(frame, f'People: {num_people}', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 사람 감지 박스 그리기
        for _, row in person_detections.iterrows():
            x1, y1, x2, y2 = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # 사람 수가 이전과 다르면 사진 저장
        if num_people != prev_num_people:
            filename = f'photo_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
            cv2.imwrite(filename, frame)
            print(f'[사진 저장] {filename} - 사람 수: {num_people}')
            prev_num_people = num_people  # 현재 인원 수를 기록
            asyncio.sleep(2)  # 너무 자주 저장되지 않도록 약간의 딜레이

        # 화면 출력
        cv2.imshow('YOLOv5 People Detection', frame)

        # 종료 조건
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 종료 처리
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.run(run())