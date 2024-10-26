from dataclasses import dataclass

@dataclass
class PerformanceMetrics:

    # All the metrics I am measuring
    stt_processing_time: float = 0.0
    llm_complete_time: float = 0.0
    total_processing_time: float = 0.0
