from pathlib import Path
from typing import Optional
from .stages.inspect import InspectStage
from .stages.preprocess import PreprocessStage
from .stages.analyze import AnalyzeStage
from .stages.export import ExportStage
from models.pipeline_result import PipelineResult
from utils.logger import logger
from utils.config_loader import config

class PipelineRunner:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(config.paths.output_dir)
        self.inspect_stage = InspectStage()
        self.preprocess_stage = PreprocessStage()
        self.analyze_stage = AnalyzeStage()
        self.export_stage = ExportStage()

    def run(self, input_path: Path) -> PipelineResult:
        logger.info(f"Starting pipeline for: {input_path}")
        
        try:
            # 1. Inspect
            metadata = self.inspect_stage.execute(input_path)
            
            # 2. Preprocess (Load)
            signal, sr = self.preprocess_stage.execute(input_path)
            
            # 3. Analyze
            analysis, quality = self.analyze_stage.execute(signal, sr)
            
            # Construct initial result
            result = PipelineResult(
                metadata=metadata,
                analysis=analysis,
                quality=quality,
                success=True
            )
            
            # 4. Export
            result = self.export_stage.execute(result, signal, sr, self.output_dir)
            
            logger.info(f"Pipeline completed successfully for: {input_path}")
            return result

        except Exception as e:
            logger.error(f"Pipeline failed for {input_path}: {e}")
            # Try to return a failure result with metadata if possible
            try:
                metadata = self.inspect_stage.execute(input_path)
                return PipelineResult(
                    metadata=metadata,
                    success=False,
                    error=str(e)
                )
            except:
                raise e
