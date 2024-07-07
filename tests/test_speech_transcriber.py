import unittest
import os
from src.speech_transcriber.speech_transcriber import transcribe_audio
from src.openai_api_interaction import OpenAIAudioAPI


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

    def test_transcribe_audio_different_format(self) -> None:
        """
        Test if the audio in a different format is successfully transcribed.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        base_test_dir = "tests/inputs"
        audio_path = os.path.join(base_test_dir, "sample_audio.mp3")
        config = OpenAIAudioAPI(
            api_key=api_key,
            file_path=audio_path,
            model="whisper-1"
        )

        transcriptions = transcribe_audio(config)

        self.assertIsNotNone(transcriptions)
        self.assertTrue(isinstance(transcriptions, str))
        self.assertTrue(len(transcriptions) > 0)

    def test_transcribe_invalid_audio(self) -> None:
        """
        Test if the function handles invalid or corrupted audio files gracefully.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        base_test_dir = "tests/inputs"
        audio_path = os.path.join(base_test_dir, "invalid_audio.wav")
        config = OpenAIAudioAPI(
            api_key=api_key,
            file_path=audio_path,
            model="whisper-1"
        )

        with self.assertRaises(Exception):
            transcribe_audio(config)

    def test_transcribe_audio_with_whisper_model(self) -> None:
        """
        Test if the audio is successfully transcribed using the whisper-1 model.
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

    def test_transcribe_audio_no_api_key(self) -> None:
        """
        Test if the function handles cases where the OpenAI API key is not set.
        """
        base_test_dir = "tests/inputs"
        audio_path = os.path.join(base_test_dir, "sample_audio.wav")
        config = OpenAIAudioAPI(
            api_key=None,
            file_path=audio_path,
            model="whisper-1"
        )

        with self.assertRaises(ValueError):
            transcribe_audio(config)

    def test_transcribe_audio_service_unavailable(self) -> None:
        """
        Test if the function handles cases where the OpenAI service is unavailable or returns an error.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        base_test_dir = "tests/inputs"
        audio_path = os.path.join(base_test_dir, "sample_audio.wav")
        config = OpenAIAudioAPI(
            api_key=api_key,
            file_path=audio_path,
            model="whisper-1"
        )

        # Simulate service unavailability by providing an invalid API key
        config.api_key = "invalid_api_key"

        with self.assertRaises(Exception):
            transcribe_audio(config)


if __name__ == "__main__":
    unittest.main()
