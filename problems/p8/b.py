# https://pytorch.org/hub/ultralytics_yolov5/

import torch
import os



model = torch.hub.load("ultralytics/yolov5", "custom", path="data/runs/yolov5/weights/best.pt")
images = os.listdir("data/test")

results = model("D:\\Documents\\code\\school\\cs5510\\5510-Midterm\\problems\\p8\\data\\test\\images\\crop_1.jpeg")

results.save()