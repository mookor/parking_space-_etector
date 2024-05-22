import cv2
import os
from datetime import datetime
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--is_test', type=bool, default=False)
parser.add_argument('--time', type=int, default=15, help='how many minutes to take a photo')
parser.add_argument('--night-scale', type=float, default=4.0)
parser.add_argument('--show_frame', type=bool, default=False)
args = parser.parse_args()

data_dir = 'data'
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

data_image_dir = os.path.join(data_dir, 'images')
if not os.path.exists(data_image_dir):
    os.mkdir(data_image_dir)

dataset_full_path = os.path.join(data_image_dir, 'test' if args.is_test else 'train')
if not os.path.exists(dataset_full_path):
    os.mkdir(dataset_full_path)


cap = cv2.VideoCapture(0)
last_photo_time = datetime.now()
print("launching camera... at", last_photo_time.strftime("%H:%M:%S"))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if args.show_frame:
        cv2.imshow('frame', cv2.resize(frame, (640*2, 480*2)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if last_photo_time.hour >= 22 or last_photo_time.hour < 4:
        photo_uptime = args.time * args.night_scale * 60 
    else:
        photo_uptime = args.time * 60
    
    current_time = datetime.now()
    img_name = f'{datetime.now():%Y_%m_%d_%H_%M_%S}.jpg'
    img_path = os.path.join(dataset_full_path, img_name)
    time_delta = current_time - last_photo_time

    if time_delta.seconds >= args.time * 60:
        cv2.imwrite(img_path, frame)
        print("saved photo at", current_time.strftime("%H:%M:%S"))
        last_photo_time = current_time
        

    