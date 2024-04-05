import cv2
import datetime
import time
import schedule
import signal
import os

working_dir = os.path.dirname(os.path.abspath(__file__))

image_dir = os.path.join(working_dir, 'images')
if not os.path.exists(image_dir):
    os.mkdir(image_dir)

running = True
daily_frames = []

def processkill(signum = None, frame = None):
    global running
    running = False

signal.signal(signal.SIGTERM, processkill)

cap = cv2.VideoCapture(0)
width = 1920
height = 1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

if not cap.isOpened():
    print("Cant open camera")
    exit(1)

def save():
    old_vid_path = os.path.join(working_dir, "video.mp4")
    new_vid_path = os.path.join(working_dir, "new_video.mp4")
    old_vid = cv2.VideoCapture(old_vid_path)
    new_vid = cv2.VideoCapture(new_vid_path)
    new_vid.set(cv2.CAP_PROP_FPS, 15)

    if old_vid.isOpened():
        while True:
            ret, frame = old_vid.read()
            new_vid.write(frame)

            if not ret or frame is None:
                break
        for frame in daily_frames:
            new_vid.write(frame)
        new_vid.release()

    os.replace(new_vid_path, old_vid_path)




def capture_image():
    now_time = datetime.datetime.now()
    if not (5 <= now_time.hour <= 20):
        return

    ret, frame = cap.read()
    if ret:
        daily_frames.append(frame)
        timestamp = int(time.time())
        print(f'Saving image {timestamp}.jpg')
        cv2.imwrite(os.path.join(image_dir, f'{timestamp}.jpg'), frame)

if __name__ == "__main__":
    schedule.every(1).minutes.do(capture_image)

    while running:
        schedule.run_pending()
        time.sleep(20)

    cap.release()

