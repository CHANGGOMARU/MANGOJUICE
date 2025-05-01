from flask import Flask, Response
import cv2

app = Flask(__name__)

def generate_video():
    cap = cv2.VideoCapture(0)  # 카메라 열기
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
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
    app.run(debug=True)