import cv2
import datetime
import time
import schedule
import signal
import os
import subprocess

def outlined_text(frame, txt, center, scale = 1, outline_color = [0,0,0], color = [255, 255, 255]):
    frame = cv2.putText(img=frame, text=txt, org=center,
        fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=scale, color=outline_color, lineType=cv2.LINE_AA, thickness=round(4 * scale))
    frame = cv2.putText(img=frame, text=txt, org=center,
        fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=scale, color=color, lineType=cv2.LINE_AA, thickness=round(2 * scale))
    return frame

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
    global daily_frames
    if len(daily_frames) == 0:
        return
    try:
        new_vid_path = os.path.join(working_dir, "new_video.mp4")
        new_vid = cv2.VideoWriter(new_vid_path, cv2.VideoWriter_fourcc(*'avc1'), 30, (1920, 1080))

        print(f'---- saving {len(daily_frames)} frames ----')
        for frame in daily_frames:
            new_vid.write(frame)
        new_vid.release()
        daily_frames.clear()

        temp_vid_path = os.path.join(working_dir, "temp_video.mp4")
        popen_args = list(f'ffmpeg -f concat -i {os.path.join(working_dir, "video_list.txt")} -c copy {temp_vid_path} -y'.split(" "))

        subprocess.run(popen_args, stdout=subprocess.DEVNULL)
        os.replace(temp_vid_path, os.path.join(working_dir, 'big_video.mp4'))

        print(f'---- done ----')
    except:
        print('---------------------- COULDNT SAVE VIDEO ------------------------------------------------')

def capture_image(jpg = False):
    now_time = datetime.datetime.now()
    if not (5 <= now_time.hour <= 21):
        return

    ret, frame = cap.read()
    if ret:
        txt = now_time.strftime('%Y/%m/%d - %H:%M')
        frame = outlined_text(frame, txt, (10,30))
        daily_frames.append(frame)
        if jpg:
            cv2.imwrite(os.path.join(image_dir, f"{now_time.strftime('%Y_%m_%d__%H_%M')}.jpg"), frame)
        print(txt)

if __name__ == "__main__":
    schedule.every(3).minutes.do(capture_image)
    schedule.every(1).hours.do(capture_image, jpg=True)
    schedule.every().day.at("23:30").do(save)
    while running:
        schedule.run_pending()
        time.sleep(20)

    cap.release()

