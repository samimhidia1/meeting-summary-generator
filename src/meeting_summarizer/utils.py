from typing import List, Dict

import tiktoken


def count_tokens(text: str,
                 model: str = "gpt-4o") -> int:
    """
    Counts the number of tokens in the text.
    Parameters
    ----------
    text : str
        The text to count the tokens of.
    model : str, optional
        The model to use, by default "gpt-4o".

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


def create_messages_from_transcripts(
        transcriptions: str,
        model: str,
        num_token_completion: int
) -> List[Dict[str, str]]:
    """
    Adds chunks of the meeting transcription to the GPT-4 messages.
    Parameters
    ----------
    transcriptions : str
        The meeting transcription.
    model : str
        The model from OpenAI to use.
    num_token_completion : int
        The number of tokens to use for the completion.

    Returns
    -------
    List[Dict[str, str]]
        The GPT-4 messages.
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
                             "gpt-4o": 128000,
                             }

    token_limit = token_limit_per_model[model]
    num_tokens_in_transcriptions = count_tokens(
        text=transcriptions, model=model)
    num_tokens_without_transcription = num_token_completion
    num_token_left = token_limit - num_tokens_without_transcription
    number_of_chunks = num_tokens_in_transcriptions // num_token_left + 1

    list_of_messages = [
        {"role": "system", "content": "You are a helpful assistant. Please summarize the following meeting points:"}]

    for i in range(number_of_chunks):
        start = i * num_token_left
        end = (i + 1) * num_token_left
        chunk = transcriptions[start:end]
        message = {"role": "user", "content": chunk}
        list_of_messages.append(message)

    return list_of_messages
