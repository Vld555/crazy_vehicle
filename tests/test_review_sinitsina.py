"""Проверки принятых замечаний Синициной: TC-53–TC-55."""

from tests.constants import Messages
from tests.steps import Steps
from walking_hut import HutOutOfFirewood, WalkingHut


class TestSinitsinaReview(Steps):
    def test_tc53_constructor_stores_integer_arguments_as_float(self):
        """TC-53: целочисленные аргументы хранятся в числовых полях как float."""
        hut = WalkingHut("Избушка", 1000, 2, 50)

        for attribute, expected in (("mass_kg", 1000.0), ("leg_length_m", 2.0),
                                    ("firewood", 50.0), ("position_m", 0.0)):
            with self.subTest(attribute=attribute):
                self.assertIs(type(getattr(hut, attribute)), float)
                self.assertEqual(getattr(hut, attribute), expected)
        self.assertIs(type(hut.healthy_legs), int)

    def test_tc54_run_without_enough_firewood_is_atomic(self):
        """TC-54: неудачный бег сохраняет полный снимок состояния."""
        hut = self.given_hut(firewood=5.0)
        before = hut.get_status().copy()

        self.assert_raises_with(HutOutOfFirewood, Messages.OUT_OF_FIREWOOD,
                                hut.run, 100)

        self.assertEqual(hut.get_status(), before)

    def test_tc55_obstacle_feasibility_does_not_check_firewood(self):
        """TC-55: геометрическая возможность не гарантирует наличие дров."""
        hut = self.given_hut(firewood=0.0)
        before = hut.get_status().copy()

        self.assertIs(hut.can_step_over("fence"), True)
        self.assertEqual(hut.get_status(), before)
        self.assert_raises_with(HutOutOfFirewood, Messages.OUT_OF_FIREWOOD,
                                hut.step_over, "fence")

        self.assertEqual(hut.get_status(), before)
