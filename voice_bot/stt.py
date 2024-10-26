from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import time
from pathlib import Path
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import httpx

class STTEngine(Enum):
    DEEPGRAM = "deepgram"


@dataclass
class STTConfig:
    engine: STTEngine
    api_key: str


class BaseSTTProvider(ABC):
    @abstractmethod
    async def transcribe(self, audio_file_path: Path) -> tuple[str, float]:
        pass


class DeepgramProvider(BaseSTTProvider):
    def __init__(self, config: STTConfig):
        self.client = DeepgramClient(config.api_key)

    async def transcribe(self, audio_file_path: Path) -> tuple[str, float]:
        try:
            start_time = time.time()

            # Reading audio file
            with open(audio_file_path, "rb") as file:
                buffer_data = file.read()

            payload: FileSource = {
                "buffer": buffer_data,
            }

            # Deepgram options
            options = PrerecordedOptions(
                model="nova-2",
                language="en-US",
                punctuate=True,
                utterances=True,
            )

            # Sending audio for transcription
            response = self.client.listen.rest.v("1").transcribe_file(
                payload, options, timeout=httpx.Timeout(300.0, connect=10.0)
            )

            # Extracting transcript from response
            transcript = response.results.channels[0].alternatives[0].transcript
            processing_time = time.time() - start_time

            return transcript.strip(), processing_time

        except Exception as e:
            print(f"Error in Deepgram transcription: {str(e)}")
            raise
