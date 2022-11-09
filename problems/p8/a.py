import os
from algorithms.ImageAI.imageai.Classification.Custom import CustomImageClassification

execution_path = os.getcwd()

model = CustomImageClassification()
model.setModelTypeAsInceptionV3()
model.setModelPath(os.path.join(execution_path, "dataset/weedcrop/models/IV3/model_ex-017_acc-0.974545.h5"))
model.setJsonPath(os.path.join(execution_path, "dataset/weedcrop/json/model_class.json"))
model.loadModel(num_objects=2)

test_images = []
for image in os.listdir("dataset/test/images"):
    predictions, probabilities = model.classifyImage(f"dataset/test/images/{image}", result_count=2)

    print(f"\n\n-------------{image:^10}---------------")
    for i in range(len(predictions)):
        print(f"|{predictions[i]: <8}|{probabilities[i]:>9.6}|")

    print(f"--------------------------------------\n\n")