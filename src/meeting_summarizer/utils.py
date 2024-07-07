from typing import List, Dict, Optional
import tiktoken
from src.openai_api_interaction.openai_api_interaction import OpenAIAudioAPI, OpenAICompletionAPI
from src.config import TEMPERATURE, PRESENCE_PENALTY, FREQUENCY_PENALTY

def count_tokens(text: str, model: str = "gpt-4o") -> int:
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

def construct_path(project: str, folder: str, filename: str) -> str:
    """
    Constructs a file path from the given project, folder, and filename.
    Parameters
    ----------
    project : str
        The project name.
    folder : str
        The folder name.
    filename : str
        The filename.

    Returns
    -------
    str
        The constructed file path.
    """
    return f"projects/{project}/{folder}/{filename}"

def extract_name_from_path(file_path: str) -> str:
    """
    Extracts the name from a given file path.
    Parameters
    ----------
    file_path : str
        The file path.

    Returns
    -------
    str
        The extracted name.
    """
    return file_path.split("/")[-1].split(".")[0]

def create_openai_audio_config(api_key: str, file_path: str) -> OpenAIAudioAPI:
    """
    Creates an OpenAIAudioAPI configuration.
    Parameters
    ----------
    api_key : str
        The OpenAI API key.
    file_path : str
        The file path.

    Returns
    -------
    OpenAIAudioAPI
        The OpenAIAudioAPI configuration.
    """
    return OpenAIAudioAPI(api_key=api_key, file_path=file_path)

def create_openai_completion_config(api_key: str, content: str, max_tokens: int) -> OpenAICompletionAPI:
    """
    Creates an OpenAICompletionAPI configuration.
    Parameters
    ----------
    api_key : str
        The OpenAI API key.
    content : str
        The content for the completion.
    max_tokens : int
        The maximum number of tokens.

    Returns
    -------
    OpenAICompletionAPI
        The OpenAICompletionAPI configuration.
    """
    return OpenAICompletionAPI(
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=TEMPERATURE,
        presence_penalty=PRESENCE_PENALTY,
        frequency_penalty=FREQUENCY_PENALTY,
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": content}]
    )

def save_text(text: str, output_path: str) -> None:
    """
    Saves the given text to the specified output path.
    Parameters
    ----------
    text : str
        The text to save.
    output_path : str
        The output file path.

    Returns
    -------
    None
    """
    with open(output_path, "w", encoding='utf-8') as transcription_file:
        transcription_file.write(text)

def read_prompt_template(file_path: str) -> str:
    """
    Reads the prompt template from the specified file path.
    Parameters
    ----------
    file_path : str
        The file path.

    Returns
    -------
    str
        The prompt template.
    """
    with open(file_path, "r", encoding='utf-8') as file:
        return file.read()
