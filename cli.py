import asyncio
import os
from dotenv import load_dotenv
from voice_bot import (
    VoiceBot,
    STTConfig,
    TTSConfig,
    LLMConfig,
    STTEngine,
    TTSEngine,
    LLMEngine
)

def load_env_variables():
    load_dotenv()

    required_vars = {
        'DEEPGRAM_API_KEY': os.getenv('DEEPGRAM_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    }

    missing_vars = [var for var, value in required_vars.items() if not value]

    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            "Please ensure these are set in your .env file"
        )

    return required_vars

async def main():
    try:
        env_vars = load_env_variables()

        bot = VoiceBot()

        stt_config = STTConfig(
            engine=STTEngine.DEEPGRAM,
            api_key=env_vars['DEEPGRAM_API_KEY']
        )

        tts_config = TTSConfig(
            engine=TTSEngine.OPENAI,
            api_key=env_vars['OPENAI_API_KEY']
        )

        llm_config = LLMConfig(
            engine=LLMEngine.OPENAI,
            api_key=env_vars['OPENAI_API_KEY'],
            system_prompt="You are a helpful voice assistant. Keep your responses concise and natural."
        )

        bot.setup(stt_config, tts_config, llm_config)

        print("Voice Bot initialized successfully!")
        print("Listening... (Press Ctrl+C to exit)")

        metrics = await bot.stream_conversation()

        print("\nPerformance Metrics:")
        print(f"STT Processing Time: {metrics.stt_processing_time:.2f}s")
        print(f"LLM Complete Time: {metrics.llm_complete_time:.2f}s")
        print(f"Total Processing Time: {metrics.total_processing_time:.2f}s")

    except ValueError as e:
        print(f"Configuration Error: {str(e)}")
    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
