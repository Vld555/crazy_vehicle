"""Дополнительные проверки по ревью Уханова: TC-48–TC-52."""

from tests.constants import Messages
from tests.steps import Steps
from walking_hut import HutOutOfFirewood, WalkingHut


class TestUkhanovReview(Steps):
    def test_tc48_stand_up_without_firewood_is_atomic(self):
        """TC-48: неудачный подъём сохраняет полный снимок состояния."""
        hut = self.given_hut(firewood=0.5, sitting=True)
        before = hut.get_status().copy()

        self.assert_raises_with(
            HutOutOfFirewood, Messages.OUT_OF_FIREWOOD, hut.stand_up
        )

        self.assertEqual(hut.get_status(), before)
        self.assertEqual(hut.pose, "sitting")
        self.assertEqual(hut.firewood, 0.5)

    def test_tc49_constructor_rejects_nonfinite_numbers(self):
        """TC-49: каждый числовой параметр отклоняет NaN и бесконечности."""
        for parameter, message in (
            ("mass_kg", Messages.MASS_RANGE),
            ("leg_length_m", Messages.LEG_RANGE),
            ("firewood", Messages.FIREWOOD_RANGE),
        ):
            for value in (float("nan"), float("inf"), -float("inf")):
                with self.subTest(parameter=parameter, value=value):
                    arguments = dict(name="Избушка", mass_kg=1000.0,
                                     leg_length_m=2.0, firewood=100.0)
                    arguments[parameter] = value
                    self.assert_raises_with(ValueError, message,
                                            lambda: WalkingHut(**arguments))

    def test_tc50_movement_rejects_nonfinite_distance_before_pose(self):
        """TC-50: расстояние проверяется до позы, ошибка не меняет состояние."""
        for method in ("walk", "run"):
            for sitting in (False, True):
                for value in (float("nan"), float("inf"), -float("inf")):
                    with self.subTest(method=method, sitting=sitting, value=value):
                        hut = self.given_hut(sitting=sitting)
                        before = hut.get_status().copy()
                        self.assert_raises_with(ValueError, Messages.DISTANCE_POSITIVE,
                                                getattr(hut, method), value)
                        self.assertEqual(hut.get_status(), before)

    def test_tc51_firewood_rejects_nonfinite_amount_before_pose(self):
        """TC-51: количество проверяется до позы, ошибка не меняет состояние."""
        for sitting in (True, False):
            for value in (float("nan"), float("inf"), -float("inf")):
                with self.subTest(sitting=sitting, value=value):
                    hut = self.given_hut(firewood=50.0, sitting=sitting)
                    before = hut.get_status().copy()
                    self.assert_raises_with(ValueError, Messages.AMOUNT_POSITIVE,
                                            hut.add_firewood, value)
                    self.assertEqual(hut.get_status(), before)

    def test_tc52_sitting_and_forced_landing_need_no_firewood(self):
        """TC-52: обычная и принудительная посадки возможны без дров."""
        for forced in (False, True):
            with self.subTest(forced=forced):
                hut = self.given_hut(firewood=0.0)
                if forced:
                    hut.damage_leg()
                    hut.damage_leg()
                else:
                    hut.sit_down()
                self.assertEqual(hut.pose, "sitting")
                self.assertEqual(hut.firewood, 0.0)
                self.assertEqual(hut.position_m, 0.0)
                self.assertEqual(hut.healthy_legs, 0 if forced else 2)
