# https://pytorch.org/hub/ultralytics_yolov5/

import torch
import os
from termcolor import colored


model = torch.hub.load("ultralytics/yolov5", "custom", path="weedcrop-models/yolov5-fresh/weights/best.pt")
images = os.listdir("dataset/test/images")


results = model([f"dataset/test/images/{image}" for image in images])
results.save(save_dir="output/b-yolov5-fresh/best/", exist_ok=True)

model = torch.hub.load("ultralytics/yolov5", "custom", path="weedcrop-models/yolov5-fresh/weights/last.pt")
images = os.listdir("dataset/test/images")


results = model([f"dataset/test/images/{image}" for image in images])
results.save(save_dir="output/b-yolov5-fresh/last/", exist_ok=True)

print(colored("Output Images for the fresh trained yolov5 model are in ", "green"), end="")
print(colored("output/b-yolov5-fresh/best/", "blue"))
print("The differences between the InceptionV3 model and the yolov5 model are:")
print("The InceptionV3 model classifies whole images, whereas the yolov5 model can extract and classify objects from within an image")
print("The yolov5 model weights are substantially smaller than the inceptionv3 weights, ~15mb vs ~100mb")

