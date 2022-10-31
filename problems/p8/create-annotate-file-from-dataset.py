import os


classes = {
    0: "crop",
    1: "weed"
}


data_path = "dataset/"

validation_dir = "validation/"
train_dir = "train/"


out_file = open("annotate.txt",encoding="utf-8", mode="w+")

train_files = os.listdir(data_path + train_dir + "images/")
validation_files = os.listdir(data_path + validation_dir + "images")

for file in train_files:
    label_file = open(data_path + train_dir + "labels/" + file.replace(".jpeg", ".txt"))
    for line in label_file:
        classnum, x_center, y_center, width, height = line.split(" ")
        xmin = float(x_center)-(float(width)/2)
        xmax = float(x_center)+(float(width)/2)
        ymin = float(y_center)-(float(height)/2)
        ymax = float(y_center)+(float(height)/2)
        classname = classes[int(classnum)]
        filepath  = data_path + train_dir + 'images/' + file
        out_file.write(f"{filepath},{xmin},{ymin},{xmax},{ymax},{classname}\n")

for file in validation_files:
    label_file = open(data_path + validation_dir + "labels/" + file.replace(".jpeg", ".txt"))
    for line in label_file:
        classnum, x_center, y_center, width, height = line.split(" ")
        xmin = float(x_center)-(float(width)/2)
        xmax = float(x_center)+(float(width)/2)
        ymin = float(y_center)-(float(height)/2)
        ymax = float(y_center)+(float(height)/2)
        classname = classes[int(classnum)]
        filepath  = data_path + validation_dir + 'images/' + file
        out_file.write(f"{filepath},{xmin},{ymin},{xmax},{ymax},{classname}\n")