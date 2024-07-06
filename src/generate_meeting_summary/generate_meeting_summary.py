import openai

from meeting_summarizer.utils import create_messages_from_transcripts
from openai_api_interaction import OpenAICompletionAPI


def generate_meeting_summary(
        summary: str,
        config: OpenAICompletionAPI,
        prompt_template: str,
) -> str:
    """
    Generates a meeting summary using OpenAI's Completion API.
    Parameters
    ----------
    summary : str
        The meeting summary.
    config : OpenAICompletionAPI
        The configuration for the OpenAI Completion API.
    prompt_template : str
        The template for creating the summary prompt.

    Returns
    -------
    str
        The generated meeting summary.
    """
    openai.api_key = config.api_key

    # Create the messages
    messages = create_messages_from_transcripts(
        transcriptions=summary,
        model=config.model,
        num_token_completion=config.max_tokens
    )

    if len(messages) == 1:
        response = openai.ChatCompletion.create(
            model=config.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": messages[0]["content"]}
            ],
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            top_p=config.top_p,
            n=config.n,
            presence_penalty=config.presence_penalty,
            frequency_penalty=config.frequency_penalty,
        )
        summary = response.choices[0]["message"]["content"].strip()
        return summary

    elif len(messages) < 20:
        response = openai.ChatCompletion.create(
            model=config.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "\n".join(
                    [msg["content"] for msg in messages])}
            ],
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            top_p=config.top_p,
            n=config.n,
            presence_penalty=config.presence_penalty,
            frequency_penalty=config.frequency_penalty,
        )
        summary = [choice["message"]["content"].strip()
                   for choice in response.choices]
        summary = merge_summaries(summary, config)
        return summary

    else:
        responses = []
        for i in range(0, len(messages), 20):
            response = openai.ChatCompletion.create(
                model=config.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "\n".join(
                        [msg["content"] for msg in messages[i:i + 20]])}
                ],
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                top_p=config.top_p,
                n=config.n,
                stream=config.stream,
                presence_penalty=config.presence_penalty,
                frequency_penalty=config.frequency_penalty,
            )
            summary = [choice["message"]["content"].strip()
                       for choice in response.choices]
            responses += summary
        summary = merge_summaries(responses, config)
        return summary


def merge_summaries(summaries: list, config: OpenAICompletionAPI) -> str:
    """
    Merges a list of summaries into a single summary.
    Parameters
    ----------
    summaries : list
        A list of summaries.
    config : OpenAICompletionAPI
        The configuration for the OpenAI Completion API.

    Returns
    -------
    str
        The merged summary.
    """
    prompt_merging = open("prompts/merge_summaries.txt",
                          "r", encoding='utf-8').read()
    summaries_to_merge = ""
    for i, summary in enumerate(summaries):
        summaries_to_merge += "MEETING SUMMARY {} :".format(
            str(i+1)) + "\n" + summary + "\n"
    prompt = prompt_merging.replace(
        "<<<MEETING SUMMARY>>>", summaries_to_merge)
    response = openai.ChatCompletion.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=config.max_tokens,
        temperature=config.temperature,
        top_p=config.top_p,
        n=config.n,
        presence_penalty=config.presence_penalty,
        frequency_penalty=config.frequency_penalty,
    )
    merged_summary = response.choices[0]["message"]["content"].strip()
    return merged_summary
