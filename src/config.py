import os

# Configuration settings for the project

# OpenAI API settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_TOKENS_SUMMARY = 4000
MAX_TOKENS_MEETING_SUMMARY = 2000
TEMPERATURE = 0.5
PRESENCE_PENALTY = 0.7
FREQUENCY_PENALTY = 0.4

# Prompt template file paths
PROMPT_TEMPLATE_SUMMARY = "generate_meeting_summary/prompts/summary_structure_2.txt"

# Batch processing settings
BATCH_SIZE = 20
