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

    if len(prompts) < 20:
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
        summary = "\n ________________\n".join(summary)
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
        summary = "\n ________________\n".join(responses)
        return summary
