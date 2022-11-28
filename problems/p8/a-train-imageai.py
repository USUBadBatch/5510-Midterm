from algorithms.ImageAI.imageai.Classification.Custom import ClassificationModelTrainer

model_trainer = ClassificationModelTrainer()
model_trainer.setModelTypeAsInceptionV3()
model_trainer.setDataDirectory("dataset/weedcrop", models_subdirectory="models/IV3")
model_trainer.trainModel(num_objects=2, num_experiments=20, batch_size=64, enhance_data=True, show_network_summary=True)