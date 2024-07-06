from audio_extractor import extract_audio_from_video
from generate_meeting_summary import generate_meeting_summary
from meeting_summarizer import summarize_transcription
from openai_api_interaction import OpenAIAudioAPI, OpenAICompletionAPI
from speech_transcriber import transcribe_audio


def save_text(text, output_path):
    with open(output_path, "w", encoding='utf-8') as transcription_file:
        transcription_file.write(text)


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
    video_path = f"projects/{project}/videos/{video_name}"
    audio_output_path = f"projects/{project}/audios/{video_name.split('.')[0]}.wav"
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
    configAudio = OpenAIAudioAPI(api_key=api_key, file_path=audio_path)
    transcription = transcribe_audio(configAudio)
    audio_name = audio_path.split("/")[-1].split(".")[0]
    output_transcription_path = f"projects/{project}/transcriptions/transcription_{audio_name}.txt"
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
    configSummary = OpenAICompletionAPI(api_key=api_key,
                                        max_tokens=777,
                                        temperature=0.5,
                                        presence_penalty=0.7,
                                        frequency_penalty=0.4,
                                        messages=[{"role": "system", "content": "You are a helpful assistant."},
                                                  {"role": "user", "content": transcription}])
    summary = summarize_transcription(transcriptions=transcription,
                                      config=configSummary)
    output_summary_path = f"projects/{project}/summaries/summary_{name}.txt"
    save_text(summary, output_summary_path)
    print("Summary of transcriptions completed.")
    print(f"Transcriptions summary saved to: {output_summary_path}")

    # Step 2: Generate the meeting summary
    with open("generate_meeting_summary/prompts/summary_structure_2.txt", "r", encoding='utf-8') as file:
        prompt_template_meeting_summary = file.read()
    print("Generating the meeting summary...")
    configMeetingSummary = OpenAICompletionAPI(api_key=api_key,
                                               max_tokens=2000,
                                               messages=[{"role": "system", "content": "You are a helpful assistant."},
                                                         {"role": "user", "content": summary}])
    meeting_summary = generate_meeting_summary(summary=summary,
                                               config=configMeetingSummary,
                                               prompt_template=prompt_template_meeting_summary)
    output_meeting_summary_path = f"projects/{project}/summaries/meeting_summary_{name}.txt"
    save_text(meeting_summary, output_meeting_summary_path)
    print("Meeting summary completed.")
    print(f"Meeting summary saved to: {output_meeting_summary_path}")
