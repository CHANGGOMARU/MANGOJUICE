import cv2
import os
import sys

def extract_frames_from_video(video_path, output_dir, output_fps=12, max_height=512):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    input_fps = cap.get(cv2.CAP_PROP_FPS)
    if input_fps == 0:
        print("Error: Cannot read FPS from video.")
        return

    frame_interval = int(round(input_fps / output_fps))
    if frame_interval < 1:
        frame_interval = 1

    frame_count = 0
    saved_frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            height, width = frame.shape[:2]
            if height > max_height:
                scale = max_height / height
                new_width = int(width * scale)
                frame = cv2.resize(frame, (new_width, max_height))

            output_path = os.path.join(output_dir, f"frame_{saved_frame_count:05d}.jpg")
            cv2.imwrite(output_path, frame)
            saved_frame_count += 1

        frame_count += 1

    cap.release()
    print(f"Done: Saved {saved_frame_count} frames to {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: 이 파일에 비디오를 드래그하거나 명령어로 실행하세요.")
        print("예: python video_frame_extractor.py example.mp4 [fps]")
        sys.exit(1)

    video_path = sys.argv[1]
    if not os.path.isfile(video_path):
        print(f"오류: 파일을 찾을 수 없습니다 - {video_path}")
        sys.exit(1)

    # FPS 설정 (기본값 12)
    try:
        output_fps = float(sys.argv[2]) if len(sys.argv) >= 3 else 12.0
    except ValueError:
        print("fps 값은 숫자여야 합니다. 기본값 12를 사용합니다.")
        output_fps = 12.0

    output_dir = os.path.join(os.path.dirname(video_path), "extracted_frames")
    extract_frames_from_video(video_path, output_dir, output_fps=output_fps)
