from ai.reconstruction.core import ReconstructionProfile

PROFILE_DESCRIPTIONS = {
    ReconstructionProfile.FAST: "Minimal deterministic restoration pass.",
    ReconstructionProfile.BALANCED: "Balanced restoration, transient, psychoacoustic, and mastering stages.",
    ReconstructionProfile.EXTREME: "Aggressive multi-stage offline reconstruction.",
    ReconstructionProfile.ARCHIVAL: "Conservative archival restoration and high-resolution rendering.",
    ReconstructionProfile.EXPERIMENTAL: "Maximum experimental reconstruction stages.",
}

