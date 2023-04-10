from typing import List

import tiktoken


def count_tokens(text: str,
                 model: str = "text-davinci-003") -> int:
    """
    Counts the number of tokens in the text.
    Parameters
    ----------
    text : str
        The text to count the tokens of.
    model : str, optional
        The model to use, by default "text-davinci-003".

    Returns
    -------
    int
        The number of tokens.
    """
    # Load an encoder for the model
    encoding = tiktoken.encoding_for_model(model)

    # turn the text into a list of tokens
    tokens = encoding.encode(text)
    num_tokens = len(tokens)

    return num_tokens


def add_chunks_of_transcripts_to_prompt(
        transcriptions: str,
        model: str,
        prompt_template: str,
        num_token_completion: int
) -> List[str]:
    """
    Adds chunks of the meeting transcription to the GPT-4 prompt.
    Parameters
    ----------
    transcriptions : str
        The meeting transcription.
    model : str
        The model from OpenAI to use.
    prompt_template : str, optional
        The template for creating the GPT-4 prompt, by default
                    "Please summarize the following meeting points:\n{points}\n".
    num_token_completion : int
        The number of tokens to use for the completion.

    Returns
    -------
    List[str]
        The GPT-4 prompt.
    """
    token_limit_per_model = {"text-davinci-003": 4000,
                             "text-davinci-002": 4000,
                             "davinci": 2000,
                             "text-curie-001": 2000,
                             "curie": 2000,
                             "text-babbage-001": 2000,
                             "babbage": 2000,
                             "text-ada-001": 2000,
                             "ada": 2000,
                             }

    token_limit = token_limit_per_model[model]
    num_tokens_in_prompt_template = count_tokens(text=prompt_template)
    num_tokens_in_transcriptions = count_tokens(text=transcriptions)
    num_tokens_without_transcription = num_tokens_in_prompt_template + num_token_completion
    num_token_left = token_limit - num_tokens_without_transcription
    number_of_chunks = num_tokens_in_transcriptions // num_token_left + 1

    list_of_prompts = list()

    for i in range(number_of_chunks):
        start = i * num_token_left
        end = (i + 1) * num_token_left
        chunk = transcriptions[start:end]
        prompt = prompt_template.replace("<<<CHUNK>>>", chunk)
        list_of_prompts.append(prompt)

    return list_of_prompts
