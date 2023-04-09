import openai
from typing import List, Optional


def summarize_transcription(
        api_key: str,
        transcriptions: List[str],
        model: Optional[str] = "text-davinci-002",
        prompt_template: Optional[str] = "Please summarize the following meeting points:\n{points}\n",
        max_tokens: Optional[int] = 150,
) -> str:
    """
    Summarizes the meeting transcription using OpenAI's GPT-4 model.

    Parameters
    ----------
    api_key : str
        The OpenAI API key.
    transcriptions : List[str]
        A list of transcribed sentences.
    model : str, optional
        The OpenAI model to use for summarization, by default "text-davinci-002".
    prompt_template : str, optional
        The template for creating the GPT-4 prompt, by default
                    "Please summarize the following meeting points:\n{points}\n".
    max_tokens : int, optional
        The maximum number of tokens to generate in the summary, by default 150.

    Returns
    -------
    str
        The generated meeting summary.
    """
    # Set up the OpenAI API client
    openai.api_key = api_key

    # Format the transcription for the prompt
    transcription_text = "\n".join(f"- {point}" for point in transcriptions)
    prompt = prompt_template.format(points=transcription_text)

    # Generate the summary
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )

    summary = response.choices[0].text.strip()

    return summary
