"""Класс WalkingHut — публичный интерфейс (SPEC, раздел 3).

описаны только сигнатуры. Реализацию пишет разработчик.
"""


class WalkingHut:
    """Избушка на курьих ножках «Бабкин Экспресс»."""

    def __init__(
        self,
        name: str,
        mass_kg: float,
        leg_length_m: float,
        firewood: float = 100.0,
    ) -> None:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def mass_kg(self) -> float:
        raise NotImplementedError

    @property
    def leg_length_m(self) -> float:
        raise NotImplementedError

    @property
    def firewood(self) -> float:
        raise NotImplementedError

    @property
    def position_m(self) -> float:
        raise NotImplementedError

    @property
    def pose(self) -> str:
        raise NotImplementedError

    @property
    def facing(self) -> str:
        raise NotImplementedError

    @property
    def healthy_legs(self) -> int:
        raise NotImplementedError

    def walk(self, distance_m: float) -> float:
        raise NotImplementedError

    def run(self, distance_m: float) -> float:
        raise NotImplementedError

    def sit_down(self) -> None:
        raise NotImplementedError

    def stand_up(self) -> None:
        raise NotImplementedError

    def turn_around(self) -> None:
        raise NotImplementedError

    def can_step_over(self, obstacle: str) -> bool:
        raise NotImplementedError

    def step_over(self, obstacle: str) -> None:
        raise NotImplementedError

    def add_firewood(self, amount: float) -> None:
        raise NotImplementedError

    def damage_leg(self) -> None:
        raise NotImplementedError

    def get_status(self) -> dict:
        raise NotImplementedError
