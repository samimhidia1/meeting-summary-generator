import openai
from typing import List, Optional


def transcribe_audio(
        api_key: str,
        audio_path: str,
        model: Optional[str] = "whisper",
        temperature: Optional[float] = 0.0,
) -> List[str]:
    """
    Transcribes the audio using OpenAI's Whisper model.

    Parameters
    ----------
    api_key : str
        The OpenAI API key.
    audio_path : str
        The path of the input audio file.
    model : str, optional
        The OpenAI model to use for transcription, by default "whisper".
    temperature : float, optional
        The temperature to use for transcription, by default 0.0.

    Returns
    -------
    List[str]
        A list of transcribed sentences.
    """
    # Set up the OpenAI API client
    openai.api_key = api_key

    # Transcribe the audio
    with open(audio_path, "rb") as audio_file:
        response = openai.Audio.transcribe(
            file=audio_file,
            model=model,
            temperature=temperature,
        )

    # Process the transcription and create a list of sentences
    transcriptions = response["choices"][0]["text"].strip().split("\n")

    return transcriptions
