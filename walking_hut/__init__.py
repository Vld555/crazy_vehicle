"""Пакет «Бабкин Экспресс»: ходячая избушка и доменные ошибки (SPEC, разделы 3, 6)."""

from .errors import (
    CrazyVehicleError,
    HutCannotStepOver,
    HutCannotWalk,
    HutIsLame,
    HutIsSitting,
    HutOutOfFirewood,
    HutWrongPose,
    WalkingHutError,
)
from .walking_hut import WalkingHut

__all__ = [
    "WalkingHut",
    "CrazyVehicleError",
    "WalkingHutError",
    "HutCannotWalk",
    "HutIsSitting",
    "HutIsLame",
    "HutOutOfFirewood",
    "HutCannotStepOver",
    "HutWrongPose",
]
