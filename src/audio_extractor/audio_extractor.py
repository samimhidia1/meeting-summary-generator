import os
import tempfile
from typing import Optional

from moviepy.editor import VideoFileClip
from pydub import AudioSegment


def extract_audio_from_video(
        video_path: str,
        audio_path: str,
        audio_format: Optional[str] = "mp3",
        start_time: Optional[float] = 0.0,
        end_time: Optional[float] = None,
) -> None:
    """
    Extracts the audio from a video file and saves it in the specified format.

    Parameters
    ----------
    video_path : str
        The path of the input video file.
    audio_path : str
        The path where the extracted audio file will be saved.
    audio_format : str, optional
        The output format of the extracted audio, by default "wav".
    start_time : float, optional
        The starting time (in seconds) from which to extract the audio, by default 0.0.
    end_time : float, optional
        The ending time (in seconds) up to which the audio will be extracted, by default None.

    Returns
    -------
    None
    """
    # Check if the input video file exists
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"The video file {video_path} does not exist.")

    # Load video and extract audio
    video = VideoFileClip(video_path)
    if end_time is None:
        end_time = video.duration
    audio = video.subclip(start_time, end_time).audio

    # Save audio to a unique temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_format}") as temp_audio_file:
        temp_audio_path = temp_audio_file.name
    audio.write_audiofile(temp_audio_path, codec=audio_format)

    # Convert the temporary audio file to the desired format and save it
    try:
        audio_segment = AudioSegment.from_file(temp_audio_path, format=audio_format)
        audio_segment.export(audio_path, format=audio_format)
    except Exception as e:
        raise RuntimeError(f"Error during audio conversion: {e}")

    # Remove the temporary audio file
    os.remove(temp_audio_path)
