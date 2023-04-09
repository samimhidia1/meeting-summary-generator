import argparse
from typing import Optional

from audio_extractor import extract_audio_from_video
from speech_transcriber import transcribe_audio
from meeting_summarizer import summarize_transcription


def main(
        video_path: str,
        api_key: str,
        output_summary_path: Optional[str] = None,
        audio_output_path: Optional[str] = None,
) -> None:
    """
    Extracts audio from a video, transcribes the audio, and summarizes the meeting.

    Parameters
    ----------
    video_path : str
        The path to the input video file.
    api_key : str
        The OpenAI API key.
    output_summary_path : str, optional
        The path to save the summarized meeting notes.
    audio_output_path : str, optional
        The path to save the extracted audio, by default None.
    """
    # Step 1: Extract audio from the video
    if audio_output_path is None:
        audio_output_path = "outputs/audios/extracted_audio_{}.wav".format(video_path.split("/")[-1].split(".")[0])

    if output_summary_path is None:
        output_summary_path = "outputs/summaries/summary_{}.txt".format(video_path.split("/")[-1].split(".")[0])

    extract_audio_from_video(video_path, audio_output_path)

    # Step 2: Transcribe the audio
    transcriptions = transcribe_audio(api_key, audio_output_path)

    # Step 3: Summarize the meeting transcription
    summary = summarize_transcription(api_key, transcriptions)

    # Save the summary to a file
    with open(output_summary_path, "w") as summary_file:
        summary_file.write(summary)

    print(f"Meeting summary saved to: {output_summary_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a meeting summary from a video")
    parser.add_argument("--video_path", type=str, required=True,
                        help="The path to the input video file (MP4 format)")
    parser.add_argument("--output_summary_path", type=str,
                        help="The path to save the summarized meeting notes (text format)")
    parser.add_argument("--audio_output_path", type=str,
                        help="The path to save the extracted audio (WAV format)")

    args = parser.parse_args()

    OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    main(video_path=args.video_path,
         api_key=OPENAI_API_KEY,
         output_summary_path=args.output_summary_path,
         audio_output_path=args.audio_output_path)
