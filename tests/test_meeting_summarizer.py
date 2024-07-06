import unittest
from meeting_summarizer import summarize_transcription
from openai_api_interaction import OpenAICompletionAPI


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
        config = OpenAICompletionAPI(
            api_key=api_key,
            model="gpt-4",
            max_tokens=4000,
            temperature=0.5,
            top_p=1.0,
            n=1,
            presence_penalty=0.0,
            frequency_penalty=0.0
        )

        transcriptions_str = " ".join(transcriptions)
        summary = summarize_transcription(transcriptions_str, config)

        self.assertIsNotNone(summary)
        self.assertTrue(isinstance(summary, str))
        self.assertTrue(len(summary) > 0)


if __name__ == "__main__":
    unittest.main()
