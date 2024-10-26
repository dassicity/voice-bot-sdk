import os
import time
from typing import Optional
from pathlib import Path
import pyaudio
import wave
from .stt import BaseSTTProvider, DeepgramProvider, STTConfig, STTEngine
from .llm import BaseLLMProvider, OpenAIProvider, LLMConfig, LLMEngine
from .tts import BaseTTSProvider, OpenAITTSProvider, TTSConfig, TTSEngine
from .metrics import PerformanceMetrics


class VoiceBot:
    def __init__(self):
        self.stt_provider: Optional[BaseSTTProvider] = None
        self.llm_provider: Optional[BaseLLMProvider] = None
        self.tts_provider: Optional[BaseTTSProvider] = None
        self.metrics = PerformanceMetrics()

    def setup(self, stt_config: STTConfig, tts_config: TTSConfig, llm_config: LLMConfig):
        if stt_config.engine == STTEngine.DEEPGRAM:
            self.stt_provider = DeepgramProvider(stt_config)

        if tts_config.engine == TTSEngine.OPENAI:
            self.tts_provider = OpenAITTSProvider(tts_config)

        if llm_config.engine == LLMEngine.OPENAI:
            self.llm_provider = OpenAIProvider(llm_config)

    async def stream_conversation(self) -> PerformanceMetrics:
        try:
            start_time = time.time()

            # Recording audio
            audio_file_path = self.record_audio(duration=5)

            # Processing through STT
            transcript, stt_time = await self.stt_provider.transcribe(audio_file_path)
            # Deleting the file
            os.remove(audio_file_path)
            self.metrics.stt_processing_time = stt_time

            if transcript.strip():
                print(f"Transcribed text: {transcript}")

                # Getting LLM response
                llm_response, first_token_time, complete_time = await self.llm_provider.query(transcript)
                print(f"LLM response: {llm_response}")
                self.metrics.llm_first_token_time = first_token_time
                self.metrics.llm_complete_time = complete_time

                # Converting to speech and saving to output.wav
                output_file_path = Path('output.wav')
                success = await self.tts_provider.synthesize(llm_response, str(output_file_path))

                self.metrics.total_processing_time = time.time() - start_time

                # Playing the synthesized speech
                if success:
                    self.play_audio_file("output.wav")
                else:
                    print("No response audio generated.")

                return self.metrics

            else:
                print("No transcript available.")
                self.metrics.total_processing_time = time.time() - start_time
                return self.metrics

        except Exception as e:
            print(f"Error in stream_conversation: {str(e)}")
            self.metrics.total_processing_time = time.time() - start_time
            return self.metrics

    def record_audio(self, duration=5, sample_rate=16000, channels=1) -> Path:
        chunk_size = 1024
        format = pyaudio.paInt16

        p = pyaudio.PyAudio()

        # Opening the stream
        stream = p.open(format=format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

        print("Recording...")

        frames = []

        for _ in range(0, int(sample_rate / chunk_size * duration)):
            data = stream.read(chunk_size, exception_on_overflow=False)
            frames.append(data)

        print("Recording finished.")

        # Stopping and closing the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Saving the recorded data as WAV file
        audio_file_path = Path('recording.wav')
        with wave.open(str(audio_file_path), 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

        return audio_file_path

    def play_audio_file(self, file_path: str):
        # Opening the WAV file
        with wave.open(file_path, 'rb') as wf:
            p = pyaudio.PyAudio()

            # Opening a stream
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            chunk_size = 1024
            data = wf.readframes(chunk_size)

            # Playing the audio
            print("Playing audio...")
            while data:
                stream.write(data)
                data = wf.readframes(chunk_size)

            # Deleting the file
            os.remove(file_path)
            stream.stop_stream()
            stream.close()
            p.terminate()

        print("Playback finished.")
