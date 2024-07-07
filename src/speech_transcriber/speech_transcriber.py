import os
import requests
from typing import List
from src.openai_api_interaction.openai_api_interaction import OpenAIAudioAPI
from pydub import AudioSegment

def split_audio_file(audio_path: str, chunk_duration: int = 100000) -> List[str]:
    """
    Splits the audio file into chunks of 24MB or less.

    Parameters
    ----------
    audio_path : str
        The path to the audio file.
    chunk_duration : int, optional
        The duration of each audio chunk in milliseconds, by default 30000 (30 seconds).

    Returns
    -------
    List[str]
        A list of file paths for the generated audio chunks.
    """
    # load the audio file
    audio = AudioSegment.from_file(audio_path)
    audio_chunks = []

    # create a temp folder to store the audio chunks
    if not os.path.exists("temp"):
        os.makedirs("temp")

    for i, chunk in enumerate(audio[::chunk_duration]):
        chunk_path = f"temp/temp_audio_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        audio_chunks.append(chunk_path)

    return audio_chunks

def transcribe_audio(
        config: OpenAIAudioAPI,
) -> str:
    """
    Transcribes the audio using OpenAI's Whisper model.

    Parameters
    ----------
    config : OpenAIAudioAPI
        The configuration for the OpenAI Audio API.
    Returns
    -------
    str
        The transcription of the audio.
    """
    # if the file is larger than 25MB, split it into chunks
    audio_size = os.path.getsize(config.file_path)
    max_size = 25 * 1024 * 1024

    if audio_size > max_size:
        # split the audio file into chunks
        audio_chunks = split_audio_file(config.file_path)
    else:
        audio_chunks = [config.file_path]

    # Generate the transcription
    transcriptions = []

    i = 0
    for chunk_path in audio_chunks:
        with open(chunk_path, "rb") as audio_file:
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={
                    "Authorization": f"Bearer {config.api_key}"
                },
                files={
                    "file": audio_file
                },
                data={
                    "model": config.model,
                    "prompt": config.prompt,
                    "response_format": "json",  # Ensure response format is JSON
                    "temperature": config.temperature,
                    "language": config.language
                }
            )
            try:
                response.raise_for_status()
                transcription = response.json().get("text", "")
                if not transcription:
                    raise ValueError(f"Unexpected response format: {response.text}")
            except requests.exceptions.HTTPError as e:
                raise ValueError(f"HTTP error occurred: {e.response.text}") from e
            except (KeyError, ValueError) as e:
                raise ValueError(f"Unexpected response format: {response.text}") from e
            transcriptions.append(transcription)

        print("progress:", i / len(audio_chunks))
        i += 1

        if audio_size > max_size:
            os.remove(chunk_path)

    transcriptions = "\n".join(transcriptions)

    return transcriptions
