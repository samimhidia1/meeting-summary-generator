import unittest
from meeting_summarizer import summarize_transcription


class TestMeetingSummarizer(unittest.TestCase):
    """
    Test cases for the summarize_transcription function in meeting_summarizer.py.
    """

    def test_summarize_transcription(self) -> None:
        """
        Test if the meeting transcription is successfully summarized.
        """
        api_key = "your_openai_api_key"
        transcriptions = [
            "Alice suggested a new marketing strategy.",
            "Bob proposed to increase the budget for the next quarter.",
            "Carol emphasized the importance of client satisfaction.",
        ]

        summary = summarize_transcription(api_key, transcriptions)

        self.assertIsNotNone(summary)
        self.assertTrue(isinstance(summary, str))
        self.assertTrue(len(summary) > 0)


if __name__ == "__main__":
    unittest.main()
