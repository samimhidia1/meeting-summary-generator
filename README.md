# Meeting Summary Generator

The Meeting Summary Generator is a Python-based tool that extracts audio from an MP4 video of a virtual meeting, transcribes the audio using OpenAI's Whisper model, and generates a summary of the meeting using OpenAI's GPT models. You can also start the process from an audio file or a text file.

## Features

- Extract audio from video files (MP4 format)
- Transcribe audio using OpenAI's Whisper model
- Summarize transcriptions using OpenAI's GPT-3.5 text-davinci-003 model
- Save generated meeting summaries as text files

## Requirements

- Python 3.10 or higher
-  [OpenAI](https://openai.com)  API key

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/samimhidia1/meeting-summary-generator.git
    ```
2. Change to the project directory:
    
    ```bash
    cd meeting-summary-generator
    ```
3. Create a virtual environment:
    
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    
    ```bash
    source venv/bin/activate
    ```
5. Install the project dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
   

## Usage

At the line 45 of the `main.py` script, replace the value of the `OPENAI_API_KEY` variable with your OpenAI API key.

Run the `main.py` script in your terminal:

```bash
python main.py
```

The script will prompt you to enter the name of the project you want to generate a summary for. Enter the name of the project and press `Enter`.

The script will then prompt you to choose between the following options:

- `1`: Start from video file
- `2`: Start from an audio file
- `3`: Start from a text file
- `4`: Exit

Choose the option that best suits your needs and press `Enter`.

### Option 1: Start from video file

If you choose option 1, the script will prompt you to enter the name of the video file you want to extract the audio from. Enter the name of the video file with the extension and press `Enter`.

e.g. `meeting.mp4`

### Option 2: Start from an audio file

If you choose option 2, the script will prompt you to enter the name of the audio file you want to transcribe. Enter the name of the audio file with the extension and press `Enter`.

e.g. `meeting.wav`

### Option 3: Start from a text file

If you choose option 3, the script will prompt you to enter the name of the text file you want to summarize. Enter the name of the text file with the extension and press `Enter`.

e.g. `meeting.txt`

### Option 4: Exit

If you choose option 4, the script will exit.

## Project Structure

The project is structured as follows:

```
meeting_summary_generator/
├── audio_extractor
│   └── audio_extractor.py
├── generate_meeting_summary
│   ├── generate_meeting_summary.py
│   └── prompts
│       ├── summary_structure_2.txt
│       └── summary_structure.txt
├── main.py
├── meeting_summarizer
│   ├── meeting_summarizer.py
│   ├── prompts
│   │   └── summarize_transcript.txt
│   └── utils.py
├── openai_api_interaction
│   └── openai_api_interaction.py
├── pipelines.py
├── projects
│   └── CISAM
│       ├── audios
│       ├── summaries
│       ├── transcriptions
│       └── videos
├── README.md
├── requirements.txt
├── speech_transcriber
│   └── speech_transcriber.py
├── temp
└── tests
    ├── test_audio_extractor.py
    ├── test_meeting_summarizer.py
    └── test_speech_transcriber.py
```

## Testing

You can run the unit tests with the following command:

```bash
python -m unittest discover  tests
```


**Note:** Running the tests for `speech_transcriber` and `meeting_summarizer` will consume tokens from your OpenAI API quota, so use it judiciously to avoid running out of your allocated tokens.

## TODO

- [ ] Add support for other video formats
- [ ] Add support for other audio formats
- [ ] Rewrite the tests to use mocks instead of the actual OpenAI API
- [ ] Add support for other Transformers models
- [ ] Add support for other prompts and summary structures
- [ ] Add support for other languages and automatic language detection
- [ ] Make the text in the terminal more user-friendly
- [ ] Test for other operating systems

## Acknowledgements

- [OpenAI](https://openai.com)
- [MoviePy](https://zulko.github.io/moviepy)
- [Pydub](https://github.com/jiaaro/pydub)

## Contact

Sami Mhidia - sami.mhidia@jarvisator.com
