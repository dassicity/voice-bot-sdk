
# VoiceBot SDK Documentation

## Introduction

The **VoiceBot SDK** is a Python library that provides an interface for building voice-based conversational applications. It integrates:

- **Speech-to-Text (STT)** using Deepgram
- **Language Model (LLM)** using OpenAI's GPT-3.5-turbo
- **Text-to-Speech (TTS)** using OpenAI

This SDK allows developers to focus on creating applications without worrying about the underlying implementations of audio recording, transcription, language processing, and speech synthesis.

---

## Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Install Dependencies](#install-dependencies)
- [Setting Up Environment Variables](#setting-up-environment-variables)
- [Usage Instructions](#usage-instructions)
  - [Importing the SDK](#importing-the-sdk)
  - [Setting Up Configurations](#setting-up-configurations)
  - [Initializing the VoiceBot](#initializing-the-voicebot)
  - [Starting the Conversation](#starting-the-conversation)
- [Assumptions](#assumptions)
- [Example Application](#example-application)
- [Additional Notes](#additional-notes)


---

## Installation

### Prerequisites

- **Python 3.7** or higher
- **Internet Connection** for API calls
- **API Keys** for Deepgram and OpenAI
- **PortAudio** library installed on your system (required for PyAudio)

### Install Dependencies

1. **Clone or Download the Repository**

   If you have the repository, navigate to its directory:

   ```bash
   git clone
   cd voice-bot-sdk
   ```

2. **Create a Virtual Environment** (Recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**

   Install dependencies using `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

   **Note**: If you face issues installing `pyaudio`, refer to the troubleshooting section below.

4. **Install PortAudio (Required for PyAudio)**

   - **macOS:**

     ```bash
     brew install portaudio
     ```

   - **Ubuntu/Linux:**

     ```bash
     sudo apt-get install portaudio19-dev
     ```

   - **Windows:**

     Download the appropriate PyAudio wheel from [PyAudio Windows Wheels](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it:

     ```bash
     pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl
     ```

     Replace the wheel file name with the one that matches your Python version and system architecture.

---

## Setting Up Environment Variables

The SDK requires API keys for Deepgram and OpenAI. To securely provide these keys, create a `.env` file in your project directory.

1. **Create a `.env` File**

   In the root directory of your project, create a file named `.env` with the following content:

   ```bash
   DEEPGRAM_API_KEY=your_deepgram_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

   Replace `your_deepgram_api_key` and `your_openai_api_key` with your actual API keys.

2. **Obtain API Keys**

   - **Deepgram API Key**: Sign up at [Deepgram](https://console.deepgram.com/signup) to obtain an API key.
   - **OpenAI API Key**: Sign up at [OpenAI](https://platform.openai.com/signup) and generate an API key.

---

## Usage Instructions

### Importing the SDK

```python
from voice_bot import VoiceBot, STTConfig, TTSConfig, LLMConfig, STTEngine, TTSEngine, LLMEngine
```

### Setting Up Configurations

```python
import os
from dotenv import load_dotenv

load_dotenv()

stt_config = STTConfig(
    engine=STTEngine.DEEPGRAM,
    api_key=os.getenv('DEEPGRAM_API_KEY')
)

tts_config = TTSConfig(
    engine=TTSEngine.OPENAI,
    api_key=os.getenv('OPENAI_API_KEY')
)

llm_config = LLMConfig(
    engine=LLMEngine.OPENAI,
    api_key=os.getenv('OPENAI_API_KEY'),
    system_prompt="You are a helpful voice assistant. Keep your responses concise and natural."
)
```

### Initializing the VoiceBot

```python
bot = VoiceBot()
bot.setup(stt_config, tts_config, llm_config)
```

### Starting the Conversation

```python
import asyncio

async def main():
    metrics = await bot.stream_conversation()
    print("\nPerformance Metrics:")
    print(f"STT Processing Time: {metrics.stt_processing_time:.2f}s")
    print(f"LLM Complete Time: {metrics.llm_complete_time:.2f}s")
    print(f"Total Processing Time: {metrics.total_processing_time:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
```

This script will:

- Record audio from your microphone.
- Transcribe the audio using Deepgram's STT service.
- Generate a response using OpenAI's GPT-3.5-turbo model.
- Synthesize speech from the generated text using OpenAI's TTS service.
- Play back the synthesized speech.
- Display performance metrics.

---

## Assumptions

- **API Rate Limits**: Be aware of any rate limits or usage policies associated with the Deepgram and OpenAI APIs.

- **Audio Compatibility**: The recording, STT, TTS, and playback all use compatible audio formats (e.g., sample rate, channels, bit depth).

- **Temporary File Handling**: The SDK creates temporary audio files (`recording.wav` and `output.wav`) during processing and deletes them after use.

- **Error Handling**: Basic error handling is implemented. For production applications, consider adding more robust error checking and exception management.

- **Dependencies Installation**: Some dependencies, like `pyaudio`, may require system-level libraries (e.g., PortAudio) to be installed.

---

## Example Application

The `cli.py` file is an example application demonstrating how to use the VoiceBot SDK. It performs the following:

- **Loads Environment Variables**: Uses `python-dotenv` to load API keys from the `.env` file.
- **Sets Up Configurations**: Initializes the STT, TTS, and LLM configurations with the appropriate API keys.
- **Initializes the VoiceBot**: Creates an instance of `VoiceBot` and sets it up with the configurations.
- **Starts the Conversation**: Calls `stream_conversation()` to begin processing audio input and output.
- **Displays Performance Metrics**: Prints out the processing times for STT, LLM, and total processing.

### Running the Example Application

```bash
python cli.py
```

---

## Additional Notes

- **Temporary File Deletion**:

  - The SDK deletes temporary files (`recording.wav`, `output.wav`) after processing.
  - This ensures that temporary files do not accumulate over time.

- **Asynchronous Programming**:

  - The SDK uses `asyncio` for asynchronous operations.
  - Ensure that your application supports asynchronous execution.

- **Audio Quality**:

  - The sample rate and audio format are set to be compatible with Deepgram and OpenAI services.
  - Adjust these settings if necessary for your specific use case.

---