"""
tracked_object.py

Defines a tracked object produced by the tracker.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class TrackedObject:
    """
    Represents one tracked object.
    """

    track_id: int
    class_id: int
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]