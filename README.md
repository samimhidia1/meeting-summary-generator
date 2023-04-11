# Meeting Summary Generator

The Meeting Summary Generator is a Python-based tool that extracts audio from an MP4 video of a virtual meeting, transcribes the audio using OpenAI's Whisper model, and generates a summary of the meeting using OpenAI's GPT models. You can also start the process from an audio file or a text file.

## Features

- Extract audio from video files (MP4 format)
- Transcribe audio using OpenAI's Whisper model
- Summarize transcriptions using OpenAI's GPT-3.5 text-davinci-003 model
- Save generated meeting summaries as text files

## Requirements

- [Download Python](https://www.python.org/downloads/) 3.10 or higher 
- Get an [OpenAI](https://openai.com)  API key

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
    python3 -m venv venv
    ```
4. Activate the virtual environment:
   * if you are using Windows:

    ```bash
    venv\Scripts\activate
    ```
    * if you are using Linux or macOS:
    
     ```bash
    source venv/bin/activate
    ```

5. Install the project dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
   

## Usage

### Setting up the OpenAI API key in the script

At the line 45 of the `main.py` script, replace the value of the `OPENAI_API_KEY` variable with your OpenAI API key.

### Running the script for the first time

Run the `main.py` script in your terminal:

```bash
python main.py
```

The script will prompt you to enter the name of the project you want to generate a summary for. Enter the name of the project and press `Enter`.

e.g. `Project MK-Ultra`

If the project does not exist, the script will create a new project directory with the name you entered. The project directory will be created in the `projects` directory. 

### Adding a video file to an existing project

Place the video file you want to process in the `videos` directory of the project directory. 

The script will extract the audio from the video file and save it in the `audios` directory of the project directory, and then it will transcribe the audio and save the transcription in the `transcriptions` directory of the project directory. Finally, it will generate a summary of the transcription and save it in the `summaries` directory of the project directory.

### Adding an audio file to an existing project

If you want to start the process from an audio file you will need to place the audio file in the `audios` directory of the project directory.

The script will transcribe the audio and save the transcription in the `transcriptions` directory of the project directory. Finally, it will generate a summary of the transcription and a structured meeting summary from it and save both text files in the `summaries` directory of the project directory.

### Adding a text file to an existing project

If you want to start the process from a text file you will need to place the text file in the `transcriptions` directory of the project directory.

The script will generate a summary of the transcription and a structured meeting summary from it and save both text files in the `summaries` directory of the project directory.

### Running the script for an existing project after adding a video file, audio file, or text file

Once you have placed the video file, audio file, or text file in the appropriate directory, re-run the `main.py` script in your terminal:

```bash
python main.py
```

Select the name of the project you want to generate a summary for and press `Enter`.

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

## Structure of the generated summary

The generated summary is structured as follows:

```
STRUCTURE:
1. Meeting Objectives:
    a. Objective 1: [Brief description]
    b. Objective 2:
    .
    .
    .
    c. Objective n:
2. Key Discussion Points:
    a. Topic 1: [Brief summary of discussion]
        Main point 1
        Main point 2
        ...
        Main point n
    b. Topic 2:
        Main point 1
        Main point 2
        ...
        Main point n
    .
    .
    .
    n. Topic n:
        Main point 1
        Main point 2
        ...
        Main point n
3. Important Decisions:
    a. Decision 1: [Decision made and rationale]
    b. Decision 2:
    .
    .
    .
    n. Decision n:
4. Action Items:
    a. Action Item 1: [Task description] - [Deadline]
    b. Action Item 2:
    .
    .
    .
    n. Action Item n:
5. Meeting Outcomes:
    a. Objective 1: [Status - Achieved/Partially Achieved/Not Achieved]
        [Key takeaways, insights, or progress made]
    b. Objective 2:
    .
    .
    .
    n. Objective n:
6. Next Steps:
    a. Next Meeting Date: [Next Meeting Date]
    b. Agenda Items for Next Meeting: [List of Agenda Items]
    c. Additional Follow-up: [Any other relevant information or follow-up tasks]
```

You can change the structure of the summary by editing the `summary_structure.txt` file in the `generate_meeting_summary/prompts` directory and the line 111 of the pipelines.py script.

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
│   └── MK-Monarch
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

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact

Sami Mhidia - sami.mhidia@jarvisator.com
