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
        The output format of the extracted audio, by default "mp3".
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
    try:
        audio.write_audiofile(temp_audio_path, codec=audio_format)
    except Exception as e:
        raise RuntimeError(f"Error during audio extraction: {e}")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)

    # Convert the temporary audio file to the desired format and save it
    try:
        audio_segment = AudioSegment.from_file(temp_audio_path, format=audio_format)
        audio_segment.export(audio_path, format=audio_format)
    except Exception as e:
        # Capture stderr output from ffmpeg for detailed error logging
        stderr_output = e.stderr.decode(errors='ignore') if hasattr(e, 'stderr') else str(e)
        raise RuntimeError(f"Error during audio conversion: {stderr_output}")

    # Remove the temporary audio file
    try:
        os.remove(temp_audio_path)
    except Exception as e:
        print(f"Warning: Failed to remove temporary file {temp_audio_path}: {e}")

    # Proper resource cleanup for VideoFileClip object
    video.close()
