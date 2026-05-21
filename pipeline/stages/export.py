from pathlib import Path
import json
from models.pipeline_result import PipelineResult
from dsp.visualizer import generate_spectrogram, generate_waveform, generate_vectorscope, generate_phase_correlation_graph
import numpy as np

class ExportStage:
    def execute(self, result: PipelineResult, signal: np.ndarray, sample_rate: int, output_dir: Path) -> PipelineResult:
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate Visualizations
        spec_path = output_dir / f"{result.metadata.filename}_spectrogram.png"
        wave_path = output_dir / f"{result.metadata.filename}_waveform.png"
        vector_path = output_dir / f"{result.metadata.filename}_vectorscope.png"
        phase_path = output_dir / f"{result.metadata.filename}_phase.png"
        
        generate_spectrogram(signal, sample_rate, spec_path)
        generate_waveform(signal, sample_rate, wave_path)
        if result.metadata.channels == 2:
            generate_vectorscope(signal, vector_path)
            generate_phase_correlation_graph(signal, sample_rate, phase_path)
            result.artifacts["vectorscope"] = str(vector_path)
            result.artifacts["phase_correlation_graph"] = str(phase_path)

        result.artifacts["spectrogram"] = str(spec_path)
        result.artifacts["waveform"] = str(wave_path)
        
        # Save JSON Report
        reports_dir = Path("reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_path = reports_dir / f"{result.metadata.filename}_report.json"
        with open(report_path, "w") as f:
            f.write(result.model_dump_json(indent=2))
        
        result.artifacts["report"] = str(report_path)
        
        return result
