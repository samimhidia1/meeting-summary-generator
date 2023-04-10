import os
from typing import Optional

from pipelines import video_to_summary, audio_to_summary, text_to_summary


def main(
        project: str,
        api_key: str,
        option: int,
        video_name: Optional[str] = None,
        transcription_path: Optional[str] = None,
        audio_path: Optional[str] = None,
) -> None:
    """
    Extracts audio from a video, transcribes the audio, and summarizes the meeting.

    Parameters
    ----------
    project : str
        The name of the project.
    api_key : str
        The OpenAI API key.
    option : int
        The option to choose the input type.
    video_name : str, optional
        The name of the input video file.
    transcription_path : str, optional
        The path to the input transcription file, by default None.
    audio_path : str, optional
        The path to save the extracted audio, by default None.
    """
    if option == 1:
        video_to_summary(project=project, video_name=video_name, api_key=api_key)
    elif option == 2:
        audio_to_summary(project, audio_path=audio_path, api_key=api_key)
    elif option == 3:
        transcription = open(transcription_path, "r", encoding='utf-8').read()
        name = transcription_path.split("/")[-1].split(".")[0]
        text_to_summary(project, transcription=transcription, name=name, api_key=api_key)


if __name__ == "__main__":
    # OPENAI_API_KEY = open("openai_apikey.txt", "r").read().strip()
    OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    print("Welcome to the meeting summarizer!")
    print("This program will summarize a meeting from a video, audio file, or text file.")
    print("Il will first extract the audio from the video, then transcribe the audio, "
          "and finally summarize the meeting notes to a text file.")
    print("You can also choose to start from an audio file or a text file directly.")
    print("To begin with Enter a name for your project.")
    project_name = input("Enter the name of the project: ")
    print("You chose the name: {}".format(project_name))
    if not os.path.exists("projects"):
        os.makedirs("projects")
    if not os.path.exists("projects/{}".format(project_name)):
        os.makedirs("projects/{}".format(project_name))
        os.makedirs("projects/{}/audios".format(project_name))
        os.makedirs("projects/{}/summaries".format(project_name))
        os.makedirs("projects/{}/transcriptions".format(project_name))
        os.makedirs("projects/{}/videos".format(project_name))
        print("Created the project folder: projects/{}".format(project_name))
        print("Created the subfolders: audios, summaries, transcriptions, videos")
        print("please copy your video, audio or text file to the project's folders.")
        print("Then run the program again.")
        exit(0)
    else:
        print("_____________________________________________________________")

    print("Choose an option to start from:")
    print("1. Start from a video")
    print("2. Start from an audio file")
    print("3. Start from a text file")
    print("4. Exit")
    chosen_option = input("Enter your choice: ")
    if chosen_option == "1":
        print("You chose to start from a video")
        videoName = input("Enter the name of the video file: ")
        main(project=project_name,
             video_name=videoName,
             api_key=OPENAI_API_KEY,
             option=int(chosen_option)
             )

    elif chosen_option == "2":
        print("You chose to start from an audio file")
        audioName = input("Enter the name to the audio file: ")
        audioPath = "projects/{}/audios/{}".format(project_name, audioName)
        main(project=project_name,
             audio_path=audioPath,
             api_key=OPENAI_API_KEY,
             option=int(chosen_option)
             )
        print("_____________________________________________________________")

    elif chosen_option == "3":
        print("You chose to start from a text file")
        transcriptionName = input("Enter the name to the text file: ")
        transcriptionPath = "projects/{}/transcriptions/{}".format(project_name, transcriptionName)
        main(project=project_name,
             transcription_path=transcriptionPath,
             api_key=OPENAI_API_KEY,
             option=int(chosen_option)
             )
        print("_____________________________________________________________")

    elif chosen_option == "4":
        print("Goodbye!")
        exit()
