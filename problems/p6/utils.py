import fer
import matplotlib.pyplot as plt

def process_video(filepath):
    face_detector = fer.FER()
    video = fer.Video(filepath)

    video_data = video.analyze(face_detector, display=False)

    video_data_dataframe = video.to_pandas(video_data)
    video_data_dataframe = video.get_first_face(video_data_dataframe)
    video_data_dataframe = video.get_emotions(video_data_dataframe)

    emotions_plot = video_data_dataframe.plot(figsize=(20, 8), fontsize=16, title=filepath) #type: ignore
    plt.show()

    emotions = {
        "Angry" : sum(video_data_dataframe.angry), #type: ignore
        "Disgust" : sum(video_data_dataframe.disgust), #type: ignore
        "Fear" : sum(video_data_dataframe.fear), #type: ignore
        "Happy" : sum(video_data_dataframe.happy), #type: ignore
        "Sad" : sum(video_data_dataframe.sad), #type: ignore
        "Surprise" : sum(video_data_dataframe.surprise), #type: ignore
        "Neutral" : sum(video_data_dataframe.neutral) #type: ignore
    }

    for emotion in emotions:
        print(f"|{emotion:<10}|{emotions[emotion]:>7.3f}|")
