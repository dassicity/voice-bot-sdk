from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import time
from openai import OpenAI


class LLMEngine(Enum):
    OPENAI = "openai"


@dataclass
class LLMConfig:
    engine: LLMEngine
    api_key: str
    system_prompt: str


class BaseLLMProvider(ABC):
    @abstractmethod
    async def query(self, text: str) -> tuple[str, float, float]:
        pass


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = OpenAI(api_key=config.api_key)

    async def query(self, text: str) -> tuple[str, float, float]:
        print(f"Inside Query with text: {text}")
        start_time = time.time()

        # Querying GPT for LLM response
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.config.system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "text"
            }
        )

        # print(response.choices[0].message.content.strip())
        llm_response = response.choices[0].message.content.strip()

        first_token_time = 0

        complete_time = time.time() - start_time
        return llm_response, first_token_time, complete_time
