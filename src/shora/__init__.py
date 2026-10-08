"""Shora (Ṣọ́ra) — multilingual Nigerian scam shield."""
from .analyze import analyze, local_pass
from .rules import find_red_flags, heuristic_score
from .taxonomy import LANGUAGES, LEGIT_TYPES, SCAM_TYPES

__version__ = "0.1.0"
__all__ = ["analyze", "local_pass", "find_red_flags", "heuristic_score", "LANGUAGES", "SCAM_TYPES", "LEGIT_TYPES"]
