"""Ходячая избушка «Бабкин Экспресс» по публичному контракту SPEC 0.2."""

import math

from .errors import (
    HutCannotStepOver, HutCannotWalk, HutIsLame, HutIsSitting,
    HutOutOfFirewood, HutWrongPose,
)

_OBSTACLES = {"log": 0.5, "fence": 1.5, "boulder": 2.5, "wall": 4.0}
_DISTANCE_ERROR = "Расстояние должно быть больше 0."
_CANNOT_WALK = "Избушка не может идти: обе ноги сломаны."
_IS_SITTING = "Избушка сидит. Сначала встаньте."
_IS_LAME = "Избушка хромает: действие требует двух здоровых ног."


def _check_number_type(value: float, parameter: str) -> None:
    """Разрешить int/float, исключив bool до любых проверок значений."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{parameter} должен быть int или float, кроме bool.")


def _number(value: float, message: str, minimum: float = 0.0,
            maximum: float | None = None, *, positive: bool = False) -> float:
    """Проверить конечность и диапазон до изменения состояния."""
    try:
        result = float(value)
    except OverflowError:
        raise ValueError(message) from None
    if (not math.isfinite(result) or result < minimum
            or (positive and result <= 0)
            or (maximum is not None and result > maximum)):
        raise ValueError(message)
    return result


def _obstacle_height(obstacle: str) -> float:
    """Проверить тип и название препятствия."""
    if not isinstance(obstacle, str):
        raise TypeError("obstacle должен быть строкой.")
    if obstacle not in _OBSTACLES:
        raise ValueError("Неизвестное препятствие.")
    return _OBSTACLES[obstacle]


class WalkingHut:
    """Избушка с печью и двумя ногами; публичные атрибуты только для чтения."""

    def __init__(self, name: str, mass_kg: float, leg_length_m: float,
                 firewood: float = 100.0) -> None:
        """Проверить сначала все типы, затем значения в порядке SPEC 3.2."""
        if not isinstance(name, str):
            raise TypeError("name должен быть строкой.")
        for parameter, value in (("mass_kg", mass_kg),
                                 ("leg_length_m", leg_length_m),
                                 ("firewood", firewood)):
            _check_number_type(value, parameter)
        if not name.strip():
            raise ValueError("Имя не может быть пустым.")
        mass = _number(mass_kg, "Масса должна быть в диапазоне 300…3000 кг.",
                       300.0, 3000.0)
        length = _number(leg_length_m,
                         "Длина ног должна быть в диапазоне 0.5…5.0 м.", 0.5, 5.0)
        wood = _number(firewood, "Запас дров должен быть в диапазоне 0…100.",
                       0.0, 100.0)
        self._name = name
        self._mass_kg = mass
        self._leg_length_m = length
        self._firewood = wood
        self._position_m = 0.0
        self._pose = "standing"
        self._facing = "forest"
        self._healthy_legs = 2

    @property
    def name(self) -> str:
        """Имя избушки."""
        return self._name

    @property
    def mass_kg(self) -> float:
        """Масса в килограммах."""
        return self._mass_kg

    @property
    def leg_length_m(self) -> float:
        """Длина ног в метрах."""
        return self._leg_length_m

    @property
    def firewood(self) -> float:
        """Остаток дров в печи."""
        return self._firewood

    @property
    def position_m(self) -> float:
        """Суммарное пройденное расстояние в метрах."""
        return self._position_m

    @property
    def pose(self) -> str:
        """Текущая поза: standing или sitting."""
        return self._pose

    @property
    def facing(self) -> str:
        """Направление: forest или traveler."""
        return self._facing

    @property
    def healthy_legs(self) -> int:
        """Число здоровых ног."""
        return self._healthy_legs

    def _require_standing(self) -> None:
        if self._pose == "sitting":
            raise HutIsSitting(_IS_SITTING)

    def _require_firewood(self, cost: float) -> None:
        if self._firewood < cost:
            raise HutOutOfFirewood("Не хватает дров в печи.")

    def _move(self, distance_m: float, *, running: bool) -> float:
        _check_number_type(distance_m, "distance_m")
        distance = _number(distance_m, _DISTANCE_ERROR, positive=True)
        if self._healthy_legs == 0:
            raise HutCannotWalk(_CANNOT_WALK)
        self._require_standing()
        if running and self._healthy_legs == 1:
            raise HutIsLame(_IS_LAME)
        speed = self._leg_length_m * 10
        cost = distance * (self._mass_kg / 50000)
        if running:
            speed *= 2
            cost *= 3
        elif self._healthy_legs == 1:
            speed *= 0.5
            cost *= 2
        self._require_firewood(cost)
        minutes = distance / speed
        position = self._position_m + distance
        self._position_m = position
        self._firewood -= cost
        return minutes

    def walk(self, distance_m: float) -> float:
        """Пройти расстояние; вернуть время в минутах, при хромоте идти медленнее."""
        return self._move(distance_m, running=False)

    def run(self, distance_m: float) -> float:
        """Пробежать на двух здоровых ногах; вернуть время в минутах."""
        return self._move(distance_m, running=True)

    def sit_down(self) -> None:
        """Сесть без расхода дров."""
        if self._pose == "sitting":
            raise HutWrongPose("Избушка уже сидит.")
        self._pose = "sitting"

    def stand_up(self) -> None:
        """Встать на одной или двух здоровых ногах, потратив единицу дров."""
        if self._pose == "standing":
            raise HutWrongPose("Избушка уже стоит.")
        if self._healthy_legs == 0:
            raise HutCannotWalk(_CANNOT_WALK)
        self._require_firewood(1.0)
        self._pose = "standing"
        self._firewood -= 1.0

    def turn_around(self) -> None:
        """Развернуться стоя за 0.5 единицы дров, сохранив позицию."""
        self._require_standing()
        self._require_firewood(0.5)
        self._facing = "traveler" if self._facing == "forest" else "forest"
        self._firewood -= 0.5

    def can_step_over(self, obstacle: str) -> bool:
        """Проверить позу, ноги и высоту; наличие дров не учитывать."""
        height = _obstacle_height(obstacle)
        return (self._pose == "standing" and self._healthy_legs == 2
                and self._leg_length_m >= height)

    def step_over(self, obstacle: str) -> None:
        """Перешагнуть допустимое препятствие за 3 единицы дров."""
        height = _obstacle_height(obstacle)
        self._require_standing()
        if self._healthy_legs == 1:
            raise HutIsLame(_IS_LAME)
        if self._leg_length_m < height:
            raise HutCannotStepOver("Ноги слишком короткие для этого препятствия.")
        self._require_firewood(3.0)
        self._firewood -= 3.0

    def add_firewood(self, amount: float) -> None:
        """Пополнить печь сидя, ограничив запас сотней единиц."""
        _check_number_type(amount, "amount")
        wood = _number(amount, "Количество дров должно быть больше 0.", positive=True)
        if self._pose == "standing":
            raise HutWrongPose("Подбросить дров можно только когда избушка сидит.")
        self._firewood = min(100.0, self._firewood + wood)

    def damage_leg(self) -> None:
        """Повредить ногу; при потере второй ноги бесплатно сесть."""
        if self._healthy_legs == 0:
            raise HutCannotWalk("Обе ноги уже сломаны.")
        self._healthy_legs -= 1
        if self._healthy_legs == 0:
            self._pose = "sitting"

    def get_status(self) -> dict:
        """Вернуть независимый снимок с шестью ключами по SPEC 3.4.10."""
        return {
            "name": self._name,
            "position_m": self._position_m,
            "firewood": self._firewood,
            "pose": self._pose,
            "facing": self._facing,
            "healthy_legs": self._healthy_legs,
        }
