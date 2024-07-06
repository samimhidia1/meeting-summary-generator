import openai
from typing import Optional, List, Dict

from meeting_summarizer.utils import create_messages_from_transcripts
from openai_api_interaction import OpenAICompletionAPI


def summarize_transcription(
        transcriptions: str,
        config: OpenAICompletionAPI,
) -> str:
    """
    Summarizes the meeting transcription using OpenAI's GPT-4o model.

    Parameters
    ----------
    transcriptions : str
        The meeting transcription.
    config : OpenAICompletionAPI
        The configuration for the OpenAI Completion API.

    Returns
    -------
    str
        The generated meeting summary.
    """
    # Set up the OpenAI API client
    client = openai.OpenAI(api_key=config.api_key)

    # Create the messages
    messages = create_messages_from_transcripts(
        transcriptions=transcriptions,
        model=config.model,
        num_token_completion=config.max_tokens
    )

    if len(messages) < 20:
        response = client.chat.completions.create(
            model=config.model,
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            top_p=config.top_p,
            n=config.n,
            presence_penalty=config.presence_penalty,
            frequency_penalty=config.frequency_penalty,
        )
        summary = [choice["message"]["content"].strip()
                   for choice in response.choices]
        summary = "".join(summary)
        return summary

    else:
        responses = []
        for i in range(0, len(messages), 20):
            response = client.chat.completions.create(
                model=config.model,
                messages=messages[i:i + 20],
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                top_p=config.top_p,
                n=config.n,
                stop=config.stop,
                presence_penalty=config.presence_penalty,
                frequency_penalty=config.frequency_penalty,
            )
            summary = [choice["message"]["content"].strip()
                       for choice in response.choices]
            responses += summary
        summary = "".join(responses)
        return summary
