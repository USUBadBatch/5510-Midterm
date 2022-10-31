import os



data_dir = "dataset/"
otrain_dir = "train/"
oval_dir = "validation/"


crop_files = []
weed_files = []

otrain_files = os.listdir(data_dir + otrain_dir + "images/")
oval_files = os.listdir(data_dir + oval_dir + "images/")

print(f"{len(otrain_files)} train files")
print(f"{len(oval_files)} val files")

for file in otrain_files:
    label_file_data = open(data_dir + otrain_dir + "labels/" + file.replace(".jpeg", ".txt")).readline()
    classid, _, _, _, _ = label_file_data.split(" ")
    classid = int(classid)
    if classid == 0: #crop
        crop_files.append(data_dir + otrain_dir + "images/" + file)
    elif classid == 1: #weed
        weed_files.append(data_dir + otrain_dir + "images/" + file)



for file in oval_files:
    label_file_data = open(data_dir + oval_dir + "labels/" + file.replace(".jpeg", ".txt")).readline()
    classid, _, _, _, _ = label_file_data.split(" ")
    classid = int(classid)

    if classid == 0: #crop
        crop_files.append(data_dir + oval_dir + "images/" + file)
    elif classid == 1: #weed
        weed_files.append(data_dir + oval_dir + "images/" + file)



print(f"{len(crop_files)} crop files")
print(f"{len(weed_files)} weed files")


for crop_file in crop_files:
    os.system(f"cp {crop_file} dataset/weedcrop/train/crop/")



for weed_file in weed_files:
    os.system(f"cp {weed_file} dataset/weedcrop/train/weed/")
