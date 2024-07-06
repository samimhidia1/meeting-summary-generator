import os
import unittest
from src.audio_extractor.audio_extractor import extract_audio_from_video
from pydub import AudioSegment


class TestAudioExtractor(unittest.TestCase):
    """
    Test cases for the extract_audio_from_video function in audio_extractor.py.
    """

    def test_extract_audio_from_video(self) -> None:
        """
        Test if the audio is successfully extracted from the video.
        """
        input_video = "tests/inputs/sample_video_with_frame.mp4"
        output_audio = "tests/outputs/sample_audio.wav"

        try:
            extract_audio_from_video(input_video, output_audio)
        except KeyError as e:
            self.fail(f"KeyError encountered: {e}")

        self.assertTrue(os.path.exists(output_audio))

        if os.path.exists(output_audio):
            os.remove(output_audio)

    def test_extract_audio_format_and_properties(self) -> None:
        """
        Test if the extracted audio has the correct format and properties.
        """
        input_video = "tests/inputs/sample_video_with_frame.mp4"
        output_audio = "tests/outputs/sample_audio.wav"

        extract_audio_from_video(input_video, output_audio, audio_format="wav")

        self.assertTrue(os.path.exists(output_audio))

        audio = AudioSegment.from_file(output_audio, format="wav")
        self.assertEqual(audio.frame_rate, 44100)  # Check if the frame rate is 44100 Hz
        self.assertGreater(audio.duration_seconds, 0)  # Check if the duration is greater than 0

        if os.path.exists(output_audio):
            os.remove(output_audio)

    def test_extract_audio_from_nonexistent_video(self) -> None:
        """
        Test if the function handles non-existent input video files gracefully.
        """
        input_video = "tests/inputs/nonexistent_video.mp4"
        output_audio = "tests/outputs/sample_audio.wav"

        with self.assertRaises(FileNotFoundError):
            extract_audio_from_video(input_video, output_audio)

    def test_extract_audio_to_restricted_output_path(self) -> None:
        """
        Test the function's behavior when the output path is not writable or has restricted permissions.
        """
        input_video = "tests/inputs/sample_video_with_frame.mp4"
        output_audio = "/restricted_path/sample_audio.wav"

        with self.assertRaises(PermissionError):
            extract_audio_from_video(input_video, output_audio)


if __name__ == "__main__":
    unittest.main()
