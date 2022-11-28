import os
import sys


curr_data_files = os.listdir("train/images")


for i in range(len(curr_data_files) // 2):
    print(f"{i}/{len(curr_data_files) // 2}")
    jpeg_file = curr_data_files[i]
    txt_file = jpeg_file.replace(".jpeg", ".txt")
    os.system(f"mv train/images/{jpeg_file} validation/images/")
    os.system(f"mv train/labels/{txt_file} validation/labels/")