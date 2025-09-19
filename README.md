🐾 WildAlert

WildAlert is a real-time animal detection and alert system powered by YOLOv5, OpenCV, and Flask.
It monitors live video, detects specific animals, streams the annotated feed in a web browser, and sends instant alerts (with images) to Telegram.

📖 Features

✅ Real-time detection using YOLOv5 (PyTorch)

✅ Detects only selected animals (cat, dog, cow, elephant, giraffe, etc.)

✅ Draws bounding boxes with confidence scores on detected animals

✅ Sends captured image + alert to Telegram bot

✅ Cooldown system (10s) to prevent spam alerts

✅ Flask-based web interface for live video streaming

🛠️ Tech Stack

Python 3

YOLOv5 (PyTorch) – Object detection

OpenCV – Video capture & annotations

Flask – Web application (live streaming)

Telegram Bot API – Instant animal alerts

▶️ How It Works

The webcam (cv2.VideoCapture(0)) captures live video.

YOLOv5 detects objects in each frame.

If a detected object is in the animal list and confidence > 0.6:

Bounding box + label drawn on frame

Frame saved locally (detected_<animal>.jpg)

Image + alert sent to Telegram

The annotated video feed is streamed on:

http://127.0.0.1:5000/ → index page

http://127.0.0.1:5000/video_feed → live MJPEG video

📊 Supported Animals

By default, WildAlert detects these animals (from COCO dataset):

🐦 Bird

🐱 Cat

🐶 Dog

🐴 Horse

🐑 Sheep

🐄 Cow

🐘 Elephant

🐻 Bear

🦓 Zebra

🦒 Giraffe

📌 Setup & Installation

Clone Repository

git clone https://github.com/your-username/WildAlert.git
cd WildAlert


Install Dependencies

pip install flask torch torchvision opencv-python requests


Configure Telegram Bot

Create a bot via @BotFather
 on Telegram

Get your BOT_TOKEN

Get your CHAT_ID (using @userinfobot or via API)

Replace them in the script:

BOT_TOKEN = 'your_bot_token_here'
CHAT_ID = 'your_chat_id_here'


Run the App

python app.py


Access the Live Feed

Open browser → http://127.0.0.1:5000/

📊 Output Example

Browser shows live video with bounding boxes

Telegram receives an alert like:

🚨 Detected: Cow


with the detected frame as an image

✨ Future Improvements

Add more animal species (custom-trained YOLO model)

Cloud storage for detected images

Email/SMS alerts in addition to Telegram

Deploy on Raspberry Pi for farm monitoring

![detect_realtime]()
![horse]()
![bear]()
![bird]()
![cat]()
![cow]()
![dog]()
![ele]()
![gir]()
![sheep]()
![zebra]()
![detect_real1]()
![detect_real2]()
