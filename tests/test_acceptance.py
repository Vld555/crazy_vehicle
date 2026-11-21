"""Проверки по итогам приёмки, TC-56–TC-58."""

from tests.constants import Messages
from tests.steps import Steps
from walking_hut import HutOutOfFirewood, WalkingHut


class TestAcceptance(Steps):
    def test_tc56_move_with_exact_fractional_firewood(self):
        """TC-56: ходьба и бег работают с дробным запасом впритык."""
        for method, firewood, speed in (("walk", 0.0014, 20), ("run", 0.0042, 40)):
            with self.subTest(method=method):
                hut = self.given_hut(firewood=firewood)

                minutes = getattr(hut, method)(0.07)

                self.assertAlmostEqual(minutes, 0.07 / speed)
                self.assertEqual(hut.position_m, 0.07)
                self.assertEqual(hut.firewood, 0.0)

    def test_tc57_rounding_does_not_cover_a_real_shortage(self):
        """TC-57: нехватка сверх допуска и пустая печь дают отказ."""
        for distance, firewood in ((0.07, 0.001399999999), (1e-15, 0.0)):
            with self.subTest(distance=distance, firewood=firewood):
                hut = self.given_hut(firewood=firewood)
                before = hut.get_status().copy()

                self.assert_raises_with(
                    HutOutOfFirewood, Messages.OUT_OF_FIREWOOD, hut.walk, distance
                )

                self.assertEqual(hut.get_status(), before)

    def test_tc58_integer_outside_float_range_is_rejected(self):
        """TC-58: целое вне диапазона float вызывает ValueError."""
        too_large = 10**1000
        for parameter, message in (
            ("mass_kg", Messages.MASS_RANGE),
            ("leg_length_m", Messages.LEG_RANGE),
            ("firewood", Messages.FIREWOOD_RANGE),
        ):
            with self.subTest(parameter=parameter):
                args = dict(name="Избушка", mass_kg=1000, leg_length_m=2, firewood=50)
                args[parameter] = too_large
                self.assert_raises_with(ValueError, message, lambda: WalkingHut(**args))

        hut = self.given_hut()
        for action, message in (
            (hut.walk, Messages.DISTANCE_POSITIVE),
            (hut.run, Messages.DISTANCE_POSITIVE),
            (hut.add_firewood, Messages.AMOUNT_POSITIVE),
        ):
            with self.subTest(action=action.__name__):
                before = hut.get_status().copy()
                self.assert_raises_with(ValueError, message, action, too_large)
                self.assertEqual(hut.get_status(), before)
