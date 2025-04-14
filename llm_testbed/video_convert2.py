import cv2
import os
import sys
from tqdm import tqdm

def resize_frame_if_needed(frame, max_width=360, max_height=420):
    height, width = frame.shape[:2]
    if width <= max_width and height <= max_height:
        return frame

    width_scale = max_width / width
    height_scale = max_height / height
    scale = min(width_scale, height_scale)

    new_width = int(width * scale)
    new_height = int(height * scale)

    return cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

def convert_video(video_path, output_fps=6.0, max_width=360, max_height=420):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    input_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if input_fps == 0 or total_frames == 0:
        print("Error: Cannot read FPS or frame count from video.")
        return

    frame_interval = int(round(input_fps / output_fps))
    if frame_interval < 1:
        frame_interval = 1

    # 첫 프레임에서 크기를 결정
    ret, frame = cap.read()
    if not ret:
        print("Error: Cannot read frame from video.")
        return

    resized_frame = resize_frame_if_needed(frame, max_width, max_height)
    height, width = resized_frame.shape[:2]

    output_path = os.path.splitext(video_path)[0] + ".converted.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, output_fps, (width, height))

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    total_written = 0

    with tqdm(total=total_frames, desc="🎞 변환 중", unit="frame") as pbar:
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                resized_frame = resize_frame_if_needed(frame, max_width, max_height)
                resized_h, resized_w = resized_frame.shape[:2]
                if (resized_w, resized_h) != (width, height):
                    resized_frame = cv2.resize(resized_frame, (width, height))

                out.write(resized_frame)
                total_written += 1

            frame_count += 1
            pbar.update(1)

    cap.release()
    out.release()
    print(f"✅ 변환 완료: {output_path} ({total_written} frames at {output_fps} fps)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: 이 파일에 비디오를 드래그하거나 명령어로 실행하세요.")
        print("예: python video_convert.py example.mp4 [fps]")
        sys.exit(1)

    video_path = sys.argv[1]
    if not os.path.isfile(video_path):
        print(f"오류: 파일을 찾을 수 없습니다 - {video_path}")
        sys.exit(1)

    try:
        output_fps = float(sys.argv[2]) if len(sys.argv) >= 3 else 6.0
        if output_fps > 6.0:
            print("FPS는 최대 6으로 제한됩니다.")
            output_fps = 6.0
    except ValueError:
        print("fps 값은 숫자여야 합니다. 기본값 6을 사용합니다.")
        output_fps = 6.0

    convert_video(video_path, output_fps=output_fps)
