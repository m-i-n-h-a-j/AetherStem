from __future__ import annotations

from ai.reconstruction.analysis.profiles import ForensicReport
from ai.reconstruction.core import ReconstructionProfile
from ai.reconstruction.harmonic.engine import HarmonicRegenerationStage
from ai.reconstruction.bandwidth.engine import BandwidthExtensionStage
from ai.reconstruction.mastering.engine import MasteringStage
from ai.reconstruction.orchestration.graph import ReconstructionGraph
from ai.reconstruction.psychoacoustics.engine import PsychoacousticOptimizationStage
from ai.reconstruction.restoration.engine import DeclipStage, DenoiseStage, DynamicRecoveryStage
from ai.reconstruction.spectral.engine import SpectralRepairStage
from ai.reconstruction.stereo.engine import StereoReconstructionStage
from ai.reconstruction.transients.engine import TransientRecoveryStage


class ReconstructionGraphBuilder:
    def build(self, report: ForensicReport, profile: ReconstructionProfile) -> ReconstructionGraph:
        stages = []
        artifacts = report.artifacts
        recommended = set(report.feasibility.recommended_stages)
        if artifacts.clipping_detected or "declip" in recommended:
            stages.append(DeclipStage())
        if artifacts.codec_ringing > 0.2:
            stages.append(DenoiseStage())
        if "spectral_repair" in recommended or profile in {ReconstructionProfile.EXTREME, ReconstructionProfile.ARCHIVAL, ReconstructionProfile.EXPERIMENTAL}:
            stages.append(SpectralRepairStage())
        if "harmonic_regeneration" in recommended or profile in {ReconstructionProfile.EXTREME, ReconstructionProfile.EXPERIMENTAL}:
            stages.append(HarmonicRegenerationStage())
        if "bandwidth_extension" in recommended or profile in {ReconstructionProfile.EXTREME, ReconstructionProfile.ARCHIVAL}:
            stages.append(BandwidthExtensionStage())
        if "transient_recovery" in recommended or profile in {ReconstructionProfile.BALANCED, ReconstructionProfile.EXTREME, ReconstructionProfile.ARCHIVAL}:
            stages.append(TransientRecoveryStage())
        if "stereo_reconstruction" in recommended:
            stages.append(StereoReconstructionStage())
        if profile != ReconstructionProfile.FAST:
            stages.append(DynamicRecoveryStage())
            stages.append(PsychoacousticOptimizationStage())
        stages.append(MasteringStage())
        return ReconstructionGraph(stages=stages)

