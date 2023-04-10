from dataclasses import dataclass
from typing import Optional


@dataclass
class OpenAIAudioAPI:
    """
    A dataclass to store the configuration for the OpenAI Audio API.

    Parameters
    ----------
    api_key : str
        The OpenAI API key.
    file_path : str
        The path to the input audio file.
    model : str, optional
        The model to use for transcription, by default "whisper-1"
    file : Optional[str], optional
        The name of the file, by default ""
    prompt : Optional[str], optional
        The prompt to use for transcription, by default None
    response_format : Optional[str], optional
        The format of the response, by default "text"
    temperature : Optional[float], optional
        The temperature to use for transcription, by default 0.0
    language : Optional[str], optional
        The language to use for transcription, by default "en"
    """
    api_key: str
    file_path: str
    model: str = "whisper-1"
    file: Optional[str] = ""
    prompt: Optional[str] = None
    response_format: Optional[str] = "text"
    temperature: Optional[float] = 0.0
    language: Optional[str] = "en"


@dataclass
class OpenAICompletionAPI:
    """
    A dataclass to store the configuration for the OpenAI Completion API.

    Parameters
    ----------
    api_key : str
        The OpenAI API key.
    model : Optional[str], optional
        The model to use for completion, by default "text-davinci-003"
    prompt : Optional[str], optional
        The prompt to use for completion, by default None
    suffix : Optional[str], optional
        The suffix to use for completion, by default None
    max_tokens : Optional[int], optional
        The maximum number of tokens to use for completion, by default 150
    temperature : Optional[float], optional
        The temperature to use for completion, by default 0.7
    top_p : Optional[float], optional
        The top p to use for completion, by default 1.0
    n : Optional[int], optional
        The number of completions to use for completion, by default 1
    stream : Optional[bool], optional
        Whether to stream the completion, by default False
    logprobs : Optional[int], optional
        The logprobs to use for completion, by default None
    echo : Optional[bool], optional
        Whether to echo the completion, by default False
    stop : Optional[str], optional
        The stop to use for completion, by default None
    presence_penalty : Optional[float], optional
        The presence penalty to use for completion, by default 0.0
    frequency_penalty : Optional[float], optional
        The frequency penalty to use for completion, by default 0.0
    best_of : Optional[int], optional
        The best of to use for completion, by default 1

    Returns
    -------
    OpenAICompletionAPI
        The OpenAI Completion API configuration.
    """
    api_key: str
    model: Optional[str] = "text-davinci-003"
    prompt: Optional[str] = None
    suffix: Optional[str] = None
    max_tokens: Optional[int] = 150
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    stream: Optional[bool] = False
    logprobs: Optional[int] = None
    echo: Optional[bool] = False
    stop: Optional[str] = None
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    best_of: Optional[int] = 1
