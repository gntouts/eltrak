from EltrakLib.BaseClasses import TrackingResult, TrackingCheckpoint
from dataclasses import dataclass
from typing import List


@dataclass
class DeprecatedTrackingResult:
    courier: str
    tracking: str
    updates: List[TrackingCheckpoint]

    @classmethod
    def from_result(cls, tracking_result: TrackingResult):
        deprecated = cls(tracking_result.courier,
                         tracking_result.tracking_number, tracking_result.updates)
        return deprecated
