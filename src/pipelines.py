from audio_extractor import extract_audio_from_video
from generate_meeting_summary import generate_meeting_summary
from meeting_summarizer import summarize_transcription
from openai_api_interaction import OpenAIAudioAPI, OpenAICompletionAPI
from speech_transcriber import transcribe_audio
import config


def save_text(text, output_path):
    with open(output_path, "w", encoding='utf-8') as transcription_file:
        transcription_file.write(text)


def read_prompt_template(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        return file.read()


def construct_path(project, folder, filename):
    return f"projects/{project}/{folder}/{filename}"


def extract_name_from_path(file_path):
    return file_path.split("/")[-1].split(".")[0]


def create_openai_audio_config(api_key, file_path):
    return OpenAIAudioAPI(api_key=api_key, file_path=file_path)


def create_openai_completion_config(api_key, content, max_tokens):
    return OpenAICompletionAPI(
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=config.TEMPERATURE,
        presence_penalty=config.PRESENCE_PENALTY,
        frequency_penalty=config.FREQUENCY_PENALTY,
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": content}]
    )


def video_to_summary(
        project: str,
        video_name: str,
        api_key: str,
) -> None:
    """
    Extracts audio from a video, transcribes the audio, and summarizes the meeting.

    Parameters
    ----------
    project : str
        The name of the project.
    video_name : str
        The name of the input video file.
    api_key : str
        The OpenAI API key.
    """
    # Step 1: Extract audio from the video
    print(f"Extracting audio from: {video_name} ...")
    video_path = construct_path(project, "videos", video_name)
    audio_output_path = construct_path(project, "audios", f"{extract_name_from_path(video_name)}.wav")
    extract_audio_from_video(video_path, audio_output_path)
    print(f"Audio extracted and saved to: {audio_output_path}")

    # Step 2: Transcribe the audio and summarize the meeting
    audio_to_summary(project, audio_output_path, api_key)


def audio_to_summary(
        project: str,
        audio_path: str,
        api_key: str,
) -> None:
    """
    Transcribes the audio and summarizes the meeting.

    Parameters
    ----------
    project : str
        The name of the project.
    audio_path : str
        The path to the input audio file.
    api_key : str
        The OpenAI API key.
    """
    # Step 1: Transcribe the audio
    print("Transcribing the audio file...")
    config_audio = create_openai_audio_config(api_key, audio_path)
    transcription = transcribe_audio(config_audio)
    audio_name = extract_name_from_path(audio_path)
    output_transcription_path = construct_path(project, "transcriptions", f"transcription_{audio_name}.txt")
    save_text(transcription, output_transcription_path)
    print("Transcription from the audio completed.")

    # Step 2: Summarize the meeting transcription
    text_to_summary(project, transcription, audio_name, api_key)


def text_to_summary(
        project: str,
        transcription: str,
        name: str,
        api_key: str,
) -> None:
    """
    Summarizes the meeting transcription.

    Parameters
    ----------
    project : str
        The name of the project.
    transcription : str
        The transcription of the meeting.
    name : str
        The name of the input text file.
    api_key : str
        The OpenAI API key.
    """
    # Step 1: Summarize the meeting transcription
    print("Summarizing the meeting transcription...")
    config_summary = create_openai_completion_config(api_key, transcription, config.MAX_TOKENS_SUMMARY)
    summary = summarize_transcription(transcriptions=transcription, config=config_summary)
    output_summary_path = construct_path(project, "summaries", f"summary_{name}.txt")
    save_text(summary, output_summary_path)
    print("Summary of transcriptions completed.")
    print(f"Transcriptions summary saved to: {output_summary_path}")

    # Step 2: Generate the meeting summary
    prompt_template_meeting_summary = read_prompt_template(config.PROMPT_TEMPLATE_SUMMARY)
    print("Generating the meeting summary...")
    config_meeting_summary = create_openai_completion_config(api_key, summary, config.MAX_TOKENS_MEETING_SUMMARY)
    meeting_summary = generate_meeting_summary(summary=summary, config=config_meeting_summary, prompt_template=prompt_template_meeting_summary)
    output_meeting_summary_path = construct_path(project, "summaries", f"meeting_summary_{name}.txt")
    save_text(meeting_summary, output_meeting_summary_path)
    print("Meeting summary completed.")
    print(f"Meeting summary saved to: {output_meeting_summary_path}")
