from algorithms.ImageAI.imageai.Classification.Custom import ClassificationModelTrainer

model_trainer = ClassificationModelTrainer()
model_trainer.setModelTypeAsResNet50()
model_trainer.setDataDirectory("dataset/weedcrop")
model_trainer.trainModel(num_objects=2, num_experiments=50, batch_size=64, show_network_summary=True)