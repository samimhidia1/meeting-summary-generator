import os
import logging
from typing import Optional

from pipelines import video_to_summary, audio_to_summary, text_to_summary


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

configure_logging()


def create_project_folders(project_name: str) -> None:
    """
    Creates the necessary project folders and subfolders.

    Parameters
    ----------
    project_name : str
        The name of the project.
    """
    project_path = f"projects/{project_name}"
    subfolders = ["audios", "summaries", "transcriptions", "videos"]

    try:
        if not os.path.exists(project_path):
            os.makedirs(project_path)
            for subfolder in subfolders:
                os.makedirs(f"{project_path}/{subfolder}")
            logging.info(f"Created the project folder: {project_path}")
            logging.info(f"Created the subfolders: {', '.join(subfolders)}")
            logging.info("Please copy your video, audio, or text file to the project's folders.")
            logging.info("Then run the program again.")
            exit(0)
        else:
            logging.info("_____________________________________________________________")
    except OSError as e:
        logging.error(f"Error creating project folders: {e}")
        exit(1)


def get_user_input(prompt: str) -> str:
    """
    Gets user input with the given prompt.

    Parameters
    ----------
    prompt : str
        The prompt to display to the user.

    Returns
    -------
    str
        The user's input.
    """
    return input(prompt)


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
    try:
        if option == 1:
            video_to_summary(project=project, video_name=video_name, api_key=api_key)
        elif option == 2:
            audio_to_summary(project, audio_path=audio_path, api_key=api_key)
        elif option == 3:
            if not os.path.exists(transcription_path):
                raise FileNotFoundError(f"Transcription file not found: {transcription_path}")
            transcription = open(transcription_path, "r", encoding='utf-8').read()
            name = transcription_path.split("/")[-1].split(".")[0]
            text_to_summary(project, transcription=transcription, name=name, api_key=api_key)
        else:
            raise ValueError("Invalid option selected. Please choose a valid option.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise EnvironmentError("The OPENAI_API_KEY environment variable is not set. Please set it before running the script.")

    logging.info("Welcome to the meeting summarizer!")
    logging.info("This program will summarize a meeting from a video, audio file, or text file.")
    logging.info("It will first extract the audio from the video, then transcribe the audio, "
          "and finally summarize the meeting notes to a text file.")
    logging.info("You can also choose to start from an audio file or a text file directly.")
    logging.info("To begin with, enter a name for your project.")

    project_name = get_user_input("Enter the name of the project: ")
    logging.info(f"You chose the name: {project_name}")

    create_project_folders(project_name)

    logging.info("Choose an option to start from:")
    logging.info("1. Start from a video")
    logging.info("2. Start from an audio file")
    logging.info("3. Start from a text file")
    logging.info("4. Exit")

    chosen_option = get_user_input("Enter your choice: ")

    if chosen_option == "1":
        logging.info("You chose to start from a video")
        video_name = get_user_input("Enter the name of the video file: ")
        main(project=project_name, video_name=video_name, api_key=OPENAI_API_KEY, option=int(chosen_option))
    elif chosen_option == "2":
        logging.info("You chose to start from an audio file")
        audio_name = get_user_input("Enter the name of the audio file: ")
        audio_path = f"projects/{project_name}/audios/{audio_name}"
        main(project=project_name, audio_path=audio_path, api_key=OPENAI_API_KEY, option=int(chosen_option))
        logging.info("_____________________________________________________________")
    elif chosen_option == "3":
        logging.info("You chose to start from a text file")
        transcription_name = get_user_input("Enter the name of the text file: ")
        transcription_path = f"projects/{project_name}/transcriptions/{transcription_name}"
        main(project=project_name, transcription_path=transcription_path, api_key=OPENAI_API_KEY, option=int(chosen_option))
        logging.info("_____________________________________________________________")
    elif chosen_option == "4":
        logging.info("Goodbye!")
        exit()
