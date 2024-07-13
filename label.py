import os
import cv2
import sys
from parser1 import parser
from utils_for_imgLabel import save_info, load_info, go2frame, show_image

args = parser.parse_args()
video_path = args.label_video_path
if not os.path.isfile(video_path) or not video_path.endswith('.mp4'):
    print("Not a valid video path! Please modify path in parser.py --label_video_path")
    sys.exit(1)

csv_path = os.path.splitext(video_path)[0] + '_ball'+ '.csv'
if not os.path.isfile(csv_path):
    print("Not a valid csv file! Please ensure the corresponding csv file exists at:", csv_path)
    sys.exit(1)

cap = cv2.VideoCapture(video_path)
fps = int(cap.get(cv2.CAP_PROP_FPS))

frame_list = []
success, frame = cap.read()
while success:
    frame_list.append(frame)
    success, frame = cap.read()
cap.release()

n_frames = len(frame_list)

info = load_info(csv_path)
if len(info) != n_frames:
    print("Number of frames in video and dictionary are not the same!")
    print("Fail to load, create new dictionary instead.")
    info = {
        idx: {
            'Frame': idx,
            'Visibility': 0,
            'X': 0,
            'Y': 0
        } for idx in range(n_frames)
    }
else:
    print("Load labeled dictionary successfully.")

modified_frames = set()

def ball_label(event, x, y, flags, param):
    global frame_no, info, image, modified_frames
    if event == cv2.EVENT_LBUTTONDOWN:
        info[frame_no]['X'] = x
        info[frame_no]['Y'] = y
        info[frame_no]['Visibility'] = 1
        modified_frames.add(frame_no)

    elif event == cv2.EVENT_MBUTTONDOWN:
        info[frame_no]['X'] = 0
        info[frame_no]['Y'] = 0
        info[frame_no]['Visibility'] = 0
        modified_frames.add(frame_no)

saved_success = False
frame_no = 0
image = frame_list[0].copy()
show_image(image, 0, info[0]['Visibility'], info[0]['X'], info[0]['Y'])
while True:
    leave = 'y'
    cv2.imshow('imgLabel', image)
    cv2.setMouseCallback('imgLabel', ball_label)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('e'):
        if not saved_success:
            print("You forget to save file!")
            while True:
                leave = str(input("Really want to leave without saving? [Y/N]"))
                leave = leave.lower()
                if leave != 'y' and leave != 'n':
                    print("Please type 'y/Y' or 'n/N'")
                    continue
                elif leave == 'y':
                    cv2.destroyAllWindows()
                    print("Exit label program")
                    sys.exit(1)
                elif leave == 'n':
                    break

        if leave == 'y':
            cv2.destroyAllWindows()
            print("Exit label program")
            sys.exit(1)

    elif key == ord('s'):
        save_info(info, csv_path)
        saved_success = True

    elif key == ord('n'):
        if frame_no >= n_frames - 1:
            print("This is the last frame")
            continue
        frame_no += 1
        image = go2frame(frame_list, frame_no, info)
        print("Frame No.{}".format(frame_no))

    elif key == ord('b'):
        if frame_no == 0:
            print("This is the first frame")
            continue
        frame_no -= 1
        image = go2frame(frame_list, frame_no, info)
        print("Frame No.{}".format(frame_no))

    elif key == ord('f'):
        if frame_no == 0:
            print("This is the first frame")
            continue
        frame_no = 0
        image = go2frame(frame_list, frame_no, info) 
        print("Frame No.{}".format(frame_no))

    elif key == ord('l'):
        if frame_no == n_frames - 1:
            print("This is the last frame")
            continue
        frame_no = n_frames - 1
        image = go2frame(frame_list, frame_no, info)
        print("Frame No.{}".format(frame_no))

    elif key == ord('d'):
        if frame_no + 36 >= n_frames - 1:
            print("Reach last frame")
            frame_no = n_frames - 1
        else:
            frame_no += 36
        image = go2frame(frame_list, frame_no, info)
        print("Frame No.{}".format(frame_no))

    elif key == ord('a'):
        if frame_no - 36 <= 0:
            print("Reach first frame")
            frame_no = 0
        else:
            frame_no -= 36
        image = go2frame(frame_list, frame_no, info)
        print("Frame No.{}".format(frame_no))

    elif key == ord(' '):  
        info[frame_no]['X'] = 0
        info[frame_no]['Y'] = 0
        info[frame_no]['Visibility'] = 0
        modified_frames.add(frame_no)
        print(f"Cleared point at frame {frame_no}")
        if frame_no >= n_frames - 1:
            print("This is the last frame")
            continue
        frame_no += 1
        image = go2frame(frame_list, frame_no, info)
        print(f"Frame No.{frame_no}")

    else:
        image = go2frame(frame_list, frame_no, info)


