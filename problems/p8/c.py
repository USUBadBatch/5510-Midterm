# https://pytorch.org/hub/ultralytics_yolov5/

import torch
import os
from termcolor import colored



model = torch.hub.load("ultralytics/yolov5", "custom", path="weedcrop-models/yolov5-retrain/weights/best.pt")
images = os.listdir("dataset/test/images")


results = model([f"dataset/test/images/{image}" for image in images])
results.save(save_dir="output/c-yolov5-retrain/best/", exist_ok=True)


model = torch.hub.load("ultralytics/yolov5", "custom", path="weedcrop-models/yolov5-retrain/weights/last.pt")
images = os.listdir("dataset/test/images")


results = model([f"dataset/test/images/{image}" for image in images])
results.save(save_dir="output/c-yolov5-retrain/last/", exist_ok=True)

print(colored("Output Images for the retrained yolov5 model are in ", "green"), end="")
print(colored("output/c-yolov5-retrain/best/", "blue"))