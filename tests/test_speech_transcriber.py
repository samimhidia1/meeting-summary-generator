import unittest
from speech_transcriber import transcribe_audio


class TestSpeechTranscriber(unittest.TestCase):
    """
    Test cases for the transcribe_audio function in speech_transcriber.py.
    """

    def test_transcribe_audio(self) -> None:
        """
        Test if the audio is successfully transcribed.
        """
        api_key = "your_openai_api_key"
        audio_path = "inputs/audios/sample_audio.wav"

        transcriptions = transcribe_audio(api_key, audio_path)

        self.assertIsNotNone(transcriptions)
        self.assertTrue(isinstance(transcriptions, list))
        self.assertTrue(len(transcriptions) > 0)


if __name__ == "__main__":
    unittest.main()
