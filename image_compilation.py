import cv2
import datetime
import time
import os

def outlined_text(frame, txt, center, scale = 1, outline_color = [0,0,0], color = [255, 255, 255]):
    frame = cv2.putText(img=frame, text=txt, org=center,
        fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=scale, color=outline_color, lineType=cv2.LINE_AA, thickness=round(4 * scale))
    frame = cv2.putText(img=frame, text=txt, org=center,
        fontFace=cv2.FONT_HERSHEY_COMPLEX , fontScale=scale, color=color, lineType=cv2.LINE_AA, thickness=round(2 * scale))
    return frame

working_dir = os.path.dirname(os.path.abspath(__file__))

old_vid_path = os.path.join(working_dir, "video.mp4")
new_vid_path = os.path.join(working_dir, "new_video.mp4")
new_vid = cv2.VideoWriter(new_vid_path, cv2.VideoWriter_fourcc(*'avc1'), 30, (1920, 1080))

img_paths = os.listdir(os.path.join(working_dir, 'images'))

#f"ffmpeg -framerate 30 -pattern_type glob -i '{os.path.join(working_dir, 'images' , '*.jpg')}' -c:v libx264 -pix_fmt yuv420p out.mp4"

for img_path in sorted(img_paths):
    dt = datetime.datetime.fromtimestamp(int(img_path.replace('.jpg','')))
    txt = dt.strftime('%Y/%m/%d - %H:%M')
    frame = cv2.imread(os.path.join('images', img_path))
    frame = outlined_text(frame, txt, (10,30))
    new_vid.write(frame)

new_vid.release()
os.replace(new_vid_path, old_vid_path)
