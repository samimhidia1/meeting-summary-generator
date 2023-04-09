# Meeting Summary Generator

The Meeting Summary Generator is a Python-based tool that extracts audio from an MP4 video of a virtual meeting, transcribes the audio using OpenAI's Whisper model, and generates a summary of the meeting using OpenAI's GPT-4 model.

## Features

- Extract audio from video files (MP4 format)
- Transcribe audio using OpenAI's Whisper model
- Summarize transcriptions using OpenAI's GPT-4 model
- Save generated meeting summaries as text files

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/samimhidia1/meeting-summary-generator.git
    ```
2. Change to the project directory:
    
    ```bash
    cd meeting-summary-generator
    ```
3. Install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```


## Usage

Run the `main.py` script with the following command-line arguments:

- `video_path`: The path to the input video file (MP4 format)
- `output_summary_path` (optional): The path to save the summarized meeting notes (text format)
- `audio_output_path` (optional): The path to save the extracted audio (WAV format)

Example usage:

```bash
python main.py --video_path ./input.mp4
```

using the `--output_summary_path` and `--audio_output_path` arguments:

```bash
python main.py --video_path ./input.mp4 --output_summary_path ./output.txt --audio_output_path ./audio.wav
```

## Project Structure

The project is structured as follows:

```
meeting_summary_generator/
│
├── audio_extractor/
│ ├── init.py
│ └── audio_extractor.py
│
├── speech_transcriber/
│ ├── init.py
│ └── speech_transcriber.py
│
├── meeting_summarizer/
│ ├── init.py
│ └── meeting_summarizer.py
│
├── tests/
│ ├── init.py
│ ├── test_audio_extractor.py
│ ├── test_speech_transcriber.py
│ └── test_meeting_summarizer.py
│
├── inputs/
│ └──videos/
│
├── outputs/
│ ├── audios/
│ ├── summaries/
│ └── transcriptions/
│
├── .gitignore
├── README.md
├── requirements.txt
└── main.py
```

## Testing

You can run the unit tests with the following command:

```bash
python -m unittest discover  tests
```


**Note:** Running the tests for `speech_transcriber` and `meeting_summarizer` will consume tokens from your OpenAI API quota, so use it judiciously to avoid running out of your allocated tokens.

## License

This project is distributed under the MIT License.

## Acknowledgements

- [OpenAI](https://openai.com)
- [MoviePy](https://zulko.github.io/moviepy)
- [Pydub](https://github.com/jiaaro/pydub)

## Contact

Sami Mhidia - sami.mhidia@jarvisator.com
