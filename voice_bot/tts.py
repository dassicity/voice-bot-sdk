from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from openai import OpenAI


class TTSEngine(Enum):
    OPENAI = "openai"


@dataclass
class TTSConfig:
    engine: TTSEngine
    api_key: str


class BaseTTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        pass


class OpenAITTSProvider(BaseTTSProvider):
    def __init__(self, config: TTSConfig):
        self.client = OpenAI(api_key=config.api_key)

    async def synthesize(self, text: str, output_file: str) -> bool:
        print(f"Inside TTS with text: {text}")
        try:

            # Creating speech from text
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text,
                response_format="wav"
            )

            with open(output_file, 'wb') as f:
                print("Writing")
                f.write(response.content)
            return True
        except Exception as e:
            print(f"Error during TTS synthesis: {e}")
            return False
