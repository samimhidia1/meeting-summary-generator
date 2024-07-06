import unittest
import os
from speech_transcriber import transcribe_audio
from openai_api_interaction import OpenAIAudioAPI


class TestSpeechTranscriber(unittest.TestCase):
    """
    Test cases for the transcribe_audio function in speech_transcriber.py.
    """

    def test_transcribe_audio(self) -> None:
        """
        Test if the audio is successfully transcribed.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        base_test_dir = "tests/inputs"
        audio_path = os.path.join(base_test_dir, "sample_audio.wav")
        config = OpenAIAudioAPI(
            api_key=api_key,
            file_path=audio_path,
            model="whisper-1"
        )

        transcriptions = transcribe_audio(config)

        self.assertIsNotNone(transcriptions)
        self.assertTrue(isinstance(transcriptions, str))
        self.assertTrue(len(transcriptions) > 0)


if __name__ == "__main__":
    unittest.main()
