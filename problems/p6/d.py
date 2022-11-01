import cv2
import fer
from fer import utils
import os
from utils import process_video
ESC = 27






selection = input("Enter the number for your selection.\n1) Analyze live webcam feed\n2) Analyze pre recorded video\n3) Record and analyze a custom video\n:>")
if selection == "1":
        
    webcam = cv2.VideoCapture(0)
    detector = fer.FER()
    if not webcam.isOpened():
        raise IOError("Cant open webcam")


    while True:
        frame_status, frame = webcam.read()
        faces = detector.detect_emotions(frame)
        frame = utils.draw_annotations(frame, faces, boxes=True, scores=True)

        cv2.imshow("Webcam Feed(Press ESC to stop)", frame)

        key = cv2.waitKey(1)
        if key == ESC:
            break

    webcam.release()
    cv2.destroyAllWindows()
elif selection == "2":
    print("Enter the path to the video")
    path = input(os.getcwd() + "/")
    process_video(path)
elif selection == "3":

    width = 1920
    height = 1080
    channel = 3
    
    fps = 30
    sec = int(input("How many seconds long\n:>"))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('custom.mp4', fourcc, float(fps), (width, height))
    webcam = cv2.VideoCapture(0)
    
    if not webcam.isOpened():
        raise IOError("Cant open webcam")

    for frame_count in range(fps*sec):
        frame_status, frame = webcam.read()
        cv2.imshow("Webcam Feed(Press ESC to stop)", frame)
        frame = cv2.resize(frame, (width, height))
        video.write(frame)

        key = cv2.waitKey(1)
        if key == ESC:
            break

    video.release()
    webcam.release()
    cv2.destroyAllWindows()

    process_video("custom.mp4")
else:
    print("Unknown Option")
    exit()