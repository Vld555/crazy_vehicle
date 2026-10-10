"""Шаги тестирования «Бабкин Экспресс».

Класс ``Steps`` содержит подготовку (Given / Arrange), создание пилота и проверки (Then / Assert).
Предусловия создаются только через публичный интерфейс ``WalkingHut``.
"""

import unittest

from tests.constants import PLACES, Hut, Legs
from tests.logger import begin_test, end_test, logger, step
from tests.pilot import BabaYaga, Kapkan
from walking_hut import CrazyVehicleError, WalkingHut, WalkingHutError


class Steps(unittest.TestCase):
    """Базовый класс тестов: подготовка, пилот и проверки."""

    def setUp(self):
        """Открывает лог текущего теста с его именем."""
        begin_test(f"{type(self).__name__}.{self._testMethodName}")

    def tearDown(self):
        """Закрывает лог текущего теста."""
        end_test()

    @staticmethod
    def step(text: str) -> None:
        """Записывает в лог шаг теста."""
        step(text)

    # region =====Подготовка=====

    @logger
    def given_hut(
        self,
        name: str = Hut.NAME,
        mass_kg: float = Hut.MASS_KG,
        leg_length_m: float = Hut.LEG_LENGTH_M,
        firewood: float = None,
        sitting: bool = False,
        healthy_legs: int = Legs.HEALTHY,
    ) -> WalkingHut:
        """Создаёт избушку и доводит её до нужного состояния через публичный интерфейс."""
        kwargs = {}
        if firewood is not None:
            kwargs["firewood"] = firewood
        hut = WalkingHut(name=name,
                         mass_kg=mass_kg,
                         leg_length_m=leg_length_m,
                         **kwargs)  # fmt: skip
        for _ in range(Legs.HEALTHY - healthy_legs):
            hut.damage_leg()
        if sitting and hut.pose != "sitting":
            hut.sit_down()
        return hut

    @logger
    def given_pilot(self, **hut_kwargs) -> BabaYaga:
        """Создаёт избушку, пилота «Баба Яга» и капкан."""
        self.hut = self.given_hut(**hut_kwargs)
        self.kapkan = Kapkan()
        return BabaYaga(self.hut)

    # endregion

    # region =====Проверки=====

    def assert_state(self, hut: WalkingHut, **expected) -> None:
        """Сверяет публичные атрибуты избушки; float — с точностью PLACES знаков."""
        for attribute, value in expected.items():
            actual = getattr(hut, attribute)
            if isinstance(value, float):
                self.assertAlmostEqual(actual, value, places=PLACES, msg=attribute)
            else:
                self.assertEqual(actual, value, msg=attribute)

    def assert_status(self, status: dict, **expected) -> None:
        """Сверяет значения словаря get_status(); float — с точностью PLACES знаков."""
        for key, value in expected.items():
            if isinstance(value, float):
                self.assertAlmostEqual(status[key], value, places=PLACES, msg=key)
            else:
                self.assertEqual(status[key], value, msg=key)

    def assert_raises_with(self, exception: type, message, action, *args):
        """Проверяет тип и текст исключения; доменные — ещё и место в иерархии (SPEC 6.1).

        ``message=None`` — текст не проверяется (например, для TypeError).
        """
        with self.assertRaises(exception) as context:
            action(*args)
        error = context.exception
        if message is not None:
            self.assertEqual(str(error), message)
        if not issubclass(exception, (ValueError, TypeError)):
            self.assertIsInstance(error, WalkingHutError)
            self.assertIsInstance(error, CrazyVehicleError)
        return error

    # endregion
