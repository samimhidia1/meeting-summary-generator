import openai

from meeting_summarizer.utils import add_chunks_of_transcripts_to_prompt
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

    # Create the prompts
    prompts = add_chunks_of_transcripts_to_prompt(
        transcriptions=summary,
        model=config.model,
        prompt_template=prompt_template,
        num_token_completion=config.max_tokens
    )

    if len(prompts) == 1:
        response = openai.Completion.create(
            model=config.model,
            prompt=prompts[0],
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            top_p=config.top_p,
            n=config.n,
            echo=config.echo,
            stop=config.stop,
            presence_penalty=config.presence_penalty,
            frequency_penalty=config.frequency_penalty,
        )
        summary = response.choices[0]["text"].strip()
        return summary

    elif len(prompts) < 20:
        response = openai.Completion.create(
            model=config.model,
            prompt=prompts,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            top_p=config.top_p,
            n=config.n,
            echo=config.echo,
            stop=config.stop,
            presence_penalty=config.presence_penalty,
            frequency_penalty=config.frequency_penalty,
        )
        summary = [choice["text"].strip() for choice in response.choices]
        summary = merge_summaries(summary)
        return summary

    else:
        responses = []
        for i in range(0, len(prompts), 20):
            response = openai.Completion.create(
                model=config.model,
                prompt=prompts[i:i + 20],
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                top_p=config.top_p,
                n=config.n,
                stream=config.stream,
                echo=config.echo,
                stop=config.stop,
                presence_penalty=config.presence_penalty,
                frequency_penalty=config.frequency_penalty,
                best_of=config.best_of,
            )
            summary = [choice["text"].strip() for choice in response.choices]
            responses += summary
        summary = merge_summaries(responses)
        return summary


def merge_summaries(summaries: list) -> str:
    """
    Merges a list of summaries into a single summary.
    Parameters
    ----------
    summaries : list
        A list of summaries.

    Returns
    -------
    str
        The merged summary.
    """
    prompt_merging = open("prompts/merge_summaries.txt", "r", encoding='utf-8').read()
    summaries_to_merge = ""
    for i, summary in enumerate(summaries):
        summaries_to_merge += "MEETING SUMMARY {} :".format(str(i+1)) + "\n" + summary + "\n"
    prompt = prompt_merging.replace("<<<MEETING SUMMARY>>>", summaries_to_merge)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        temperature=0.7,
        top_p=1,
        n=1,
        presence_penalty=0.6,
        frequency_penalty=0.3,
        best_of=3,
    )
    merged_summary = response.choices[0]["text"].strip()
    return merged_summary

