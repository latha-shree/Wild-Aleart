import cv2
import torch
import time
import requests
from flask import Flask, render_template, Response

# === Telegram Bot Config ===
BOT_TOKEN = ''
CHAT_ID = ''

# Load YOLOv5 model from PyTorch hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# All animals YOLOv5s (COCO) supports (lion not included)
animal_classes = [
    'bird', 'cat', 'dog', 'horse', 'sheep',
    'cow', 'elephant', 'bear', 'zebra', 'giraffe'
]

# Initialize Flask app
app = Flask(__name__)
video_capture = cv2.VideoCapture(0)

# Track last sent time to avoid spamming
last_sent_time = 0
cooldown = 10  # seconds

def send_image_to_telegram(image_path, label):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    files = {'photo': open(image_path, 'rb')}
    data = {'chat_id': CHAT_ID, 'caption': f'🚨 Detected: {label}'}
    response = requests.post(url, files=files, data=data)
    if response.ok:
        print("✅ Image sent to Telegram!")
    else:
        print("❌ Failed to send image:", response.text)

def gen_frames():
    global last_sent_time

    while True:
        success, frame = video_capture.read()
        if not success:
            break

        # Inference
        results = model(frame)

        # Parse detections
        for *box, conf, cls in results.xyxy[0]:
            label = model.names[int(cls)]
            if label in animal_classes and conf > 0.6:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

                # Check cooldown before sending image
                current_time = time.time()
                if current_time - last_sent_time > cooldown:
                    img_path = f"detected_{label}.jpg"
                    cv2.imwrite(img_path, frame)
                    send_image_to_telegram(img_path, label)
                    last_sent_time = current_time

        # Encode image
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
