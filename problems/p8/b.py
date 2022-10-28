# https://pytorch.org/hub/ultralytics_yolov5/

import torch
import os



model = torch.hub.load("ultralytics/yolov5", "custom", path="weedcrop-models/yolov5/weights/best.pt")
images = os.listdir("dataset/test/images")


results = model([f"dataset/test/images/{image}" for image in images])
results.save(save_dir="output/b-yolov5/", exist_ok=True)