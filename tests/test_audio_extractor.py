import os
import unittest
from src.audio_extractor.audio_extractor import extract_audio_from_video


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


if __name__ == "__main__":
    unittest.main()
