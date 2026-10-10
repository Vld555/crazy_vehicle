"""Тестовые обёртки сценариев (SPEC 4.2): пилот «Баба Яга» и объект среды «Капкан».

Не входят в продукт: только делегируют вызовы публичному интерфейсу ``WalkingHut``
на доменном языке.
"""

from tests.logger import logger


class BabaYaga:
    """Пилот избушки. Управляет ею на доменном языке."""

    def __init__(self, hut) -> None:
        self._hut = hut

    @logger
    def пройти(self, distance_m: float) -> float:
        return self._hut.walk(distance_m)

    @logger
    def пробежать(self, distance_m: float) -> float:
        return self._hut.run(distance_m)

    @logger
    def присесть(self) -> None:
        self._hut.sit_down()

    @logger
    def встать(self) -> None:
        self._hut.stand_up()

    @logger
    def стань_ко_мне_передом(self) -> None:
        self._hut.turn_around()

    @logger
    def можно_перешагнуть(self, obstacle: str) -> bool:
        return self._hut.can_step_over(obstacle)

    @logger
    def перешагнуть(self, obstacle: str) -> None:
        self._hut.step_over(obstacle)

    @logger
    def подкинуть_дров(self, amount: float) -> None:
        self._hut.add_firewood(amount)

    @logger
    def осмотреться(self) -> dict:
        return self._hut.get_status()


class Kapkan:
    """Капкан в лесу: защемляет одну ногу избушки."""

    @logger
    def защемить(self, hut) -> None:
        hut.damage_leg()
