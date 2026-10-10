"""Модульные тесты WalkingHut (SPEC 4.1, TC-01…TC-39), паттерн AAA."""

from tests.constants import (
    STATUS_KEYS,
    Facing,
    Firewood,
    Hut,
    Legs,
    Messages,
    Obstacle,
    Pose,
)
from tests.steps import Steps
from walking_hut import (
    HutCannotStepOver,
    HutCannotWalk,
    HutIsLame,
    HutIsSitting,
    HutOutOfFirewood,
    HutWrongPose,
    WalkingHut,
)


class TestWalkingHutInit(Steps):
    """Конструктор (SPEC 3.2, 3.3)."""

    def test_tc01_init_with_defaults(self):
        """TC-01: параметры по умолчанию и начальное состояние."""
        # Arrange
        self.step("Параметры базовой избушки")

        # Act
        self.step("Создание избушки")
        hut = WalkingHut(Hut.NAME, Hut.MASS_KG, Hut.LEG_LENGTH_M)

        # Assert
        self.step("Проверка атрибутов")
        self.assert_state(hut,
                          name=Hut.NAME,
                          mass_kg=Hut.MASS_KG,
                          leg_length_m=Hut.LEG_LENGTH_M,
                          firewood=Firewood.DEFAULT,
                          position_m=0.0,
                          pose=Pose.STANDING,
                          facing=Facing.FOREST,
                          healthy_legs=Legs.HEALTHY)  # fmt: skip

    def test_tc02_init_with_all_parameters(self):
        """TC-02: все параметры заданы явно."""
        # Arrange
        mass_kg, leg_length_m, firewood = 1500.0, 3.0, 40.0

        # Act
        hut = WalkingHut(Hut.NAME, mass_kg, leg_length_m, firewood)

        # Assert
        self.assert_state(hut, mass_kg=1500.0, leg_length_m=3.0, firewood=40.0)

    def test_tc03_init_lower_boundaries_allowed(self):
        """TC-03: нижние границы диапазонов допустимы."""
        # Arrange
        mass_kg, leg_length_m, firewood = 300.0, 0.5, 0.0

        # Act
        hut = WalkingHut(Hut.NAME, mass_kg, leg_length_m, firewood)

        # Assert
        self.assert_state(hut, mass_kg=300.0, leg_length_m=0.5, firewood=0.0)

    def test_tc04_init_empty_name_raises(self):
        """TC-04: пустое имя."""
        # Arrange
        name = ""

        # Act / Assert
        self.assert_raises_with(ValueError, Messages.EMPTY_NAME,
                                WalkingHut, name, Hut.MASS_KG, Hut.LEG_LENGTH_M)  # fmt: skip

    def test_tc05_init_blank_name_raises(self):
        """TC-05: имя из одних пробелов."""
        # Arrange
        name = "   "

        # Act / Assert
        self.assert_raises_with(ValueError, Messages.EMPTY_NAME,
                                WalkingHut, name, Hut.MASS_KG, Hut.LEG_LENGTH_M)  # fmt: skip

    def test_tc06_init_mass_below_range_raises(self):
        """TC-06: масса меньше 300."""
        # Arrange
        mass_kg = 299.9

        # Act / Assert
        self.assert_raises_with(ValueError, Messages.MASS_RANGE,
                                WalkingHut, Hut.NAME, mass_kg, Hut.LEG_LENGTH_M)  # fmt: skip

    def test_tc07_init_mass_above_range_raises(self):
        """TC-07: масса больше 3000."""
        # Arrange
        mass_kg = 3000.1

        # Act / Assert
        self.assert_raises_with(ValueError, Messages.MASS_RANGE,
                                WalkingHut, Hut.NAME, mass_kg, Hut.LEG_LENGTH_M)  # fmt: skip

    def test_tc08_init_legs_too_short_raises(self):
        """TC-08: длина ног меньше 0.5."""
        # Arrange
        leg_length_m = 0.4

        # Act / Assert
        self.assert_raises_with(ValueError, Messages.LEG_RANGE,
                                WalkingHut, Hut.NAME, Hut.MASS_KG, leg_length_m)  # fmt: skip

    def test_tc09_init_legs_too_long_raises(self):
        """TC-09: длина ног больше 5.0."""
        # Arrange
        leg_length_m = 5.1

        # Act / Assert
        self.assert_raises_with(ValueError, Messages.LEG_RANGE,
                                WalkingHut, Hut.NAME, Hut.MASS_KG, leg_length_m)  # fmt: skip

    def test_tc10_init_firewood_above_range_raises(self):
        """TC-10: запас дров больше 100."""
        # Arrange
        firewood = 100.5

        # Act / Assert
        self.assert_raises_with(ValueError, Messages.FIREWOOD_RANGE,
                                WalkingHut, Hut.NAME, Hut.MASS_KG, Hut.LEG_LENGTH_M, firewood)  # fmt: skip

    def test_tc11_init_mass_wrong_type_raises(self):
        """TC-11: масса передана строкой."""
        # Arrange
        mass_kg = "1000"

        # Act / Assert
        self.assert_raises_with(TypeError, None,
                                WalkingHut, Hut.NAME, mass_kg, Hut.LEG_LENGTH_M)  # fmt: skip


class TestWalkingHutWalkRun(Steps):
    """Ходьба и бег (SPEC 3.4.1, 3.4.2)."""

    def test_tc12_walk_on_two_legs(self):
        """TC-12: обычный шаг на 100 м."""
        # Arrange
        hut = self.given_hut()

        # Act
        minutes = hut.walk(100)

        # Assert
        self.assertAlmostEqual(minutes, 5.0)
        self.assert_state(hut, position_m=100.0, firewood=98.0)

    def test_tc13_walk_lame_is_slower_and_costlier(self):
        """TC-13: хромая избушка идёт вдвое медленнее и тратит вдвое больше."""
        # Arrange
        hut = self.given_hut(healthy_legs=Legs.LAME)

        # Act
        minutes = hut.walk(100)

        # Assert
        self.assertAlmostEqual(minutes, 10.0)
        self.assert_state(hut, position_m=100.0, firewood=96.0)

    def test_tc14_walk_zero_distance_raises(self):
        """TC-14: нулевое расстояние."""
        # Arrange
        hut = self.given_hut()

        # Act / Assert
        self.assert_raises_with(ValueError, Messages.DISTANCE_POSITIVE, hut.walk, 0)
        self.assert_state(hut, position_m=0.0, firewood=100.0)

    def test_tc15_walk_wrong_type_raises(self):
        """TC-15: расстояние передано строкой."""
        # Arrange
        hut = self.given_hut()

        # Act / Assert
        self.assert_raises_with(TypeError, None, hut.walk, "abc")

    def test_tc16_walk_while_sitting_raises(self):
        """TC-16: ходьба сидя."""
        # Arrange
        hut = self.given_hut(sitting=True)

        # Act / Assert
        self.assert_raises_with(HutIsSitting, Messages.IS_SITTING, hut.walk, 10)
        self.assert_state(hut, position_m=0.0, firewood=100.0)

    def test_tc17_walk_without_firewood_raises(self):
        """TC-17: дров меньше, чем нужно; состояние не меняется."""
        # Arrange
        hut = self.given_hut(firewood=1.0)

        # Act / Assert
        self.assert_raises_with(HutOutOfFirewood, Messages.OUT_OF_FIREWOOD, hut.walk, 100)
        self.assert_state(hut, position_m=0.0, firewood=1.0)

    def test_tc18_walk_with_exact_firewood(self):
        """TC-18: дров ровно впритык — движение выполняется."""
        # Arrange
        hut = self.given_hut(firewood=2.0)

        # Act
        hut.walk(100)

        # Assert
        self.assert_state(hut, position_m=100.0, firewood=0.0)

    def test_tc19_run_on_two_legs(self):
        """TC-19: бег на 100 м."""
        # Arrange
        hut = self.given_hut()

        # Act
        minutes = hut.run(100)

        # Assert
        self.assertAlmostEqual(minutes, 2.5)
        self.assert_state(hut, position_m=100.0, firewood=94.0)

    def test_tc20_run_lame_raises(self):
        """TC-20: бег на одной ноге."""
        # Arrange
        hut = self.given_hut(healthy_legs=Legs.LAME)

        # Act / Assert
        self.assert_raises_with(HutIsLame, Messages.IS_LAME, hut.run, 10)
        self.assert_state(hut, position_m=0.0, firewood=100.0)


class TestWalkingHutPose(Steps):
    """Поза и разворот (SPEC 3.4.3–3.4.5)."""

    def test_tc21_sit_down(self):
        """TC-21: присесть."""
        # Arrange
        hut = self.given_hut()

        # Act
        hut.sit_down()

        # Assert
        self.assert_state(hut, pose=Pose.SITTING, firewood=100.0)

    def test_tc22_stand_up_costs_firewood(self):
        """TC-22: встать стоит 1.0 дров."""
        # Arrange
        hut = self.given_hut(sitting=True)

        # Act
        hut.stand_up()

        # Assert
        self.assert_state(hut, pose=Pose.STANDING, firewood=100.0 - Firewood.STAND_UP)

    def test_tc23_stand_up_when_standing_raises(self):
        """TC-23: встать, когда уже стоит."""
        # Arrange
        hut = self.given_hut()

        # Act / Assert
        self.assert_raises_with(HutWrongPose, Messages.ALREADY_STANDING, hut.stand_up)
        self.assert_state(hut, firewood=100.0)

    def test_tc24_stand_up_without_legs_raises(self):
        """TC-24: встать без здоровых ног."""
        # Arrange
        hut = self.given_hut(healthy_legs=Legs.BROKEN)

        # Act / Assert
        self.assert_raises_with(HutCannotWalk, Messages.CANNOT_WALK, hut.stand_up)
        self.assert_state(hut, pose=Pose.SITTING, firewood=100.0)

    def test_tc25_turn_around(self):
        """TC-25: «стань ко мне передом, к лесу задом»."""
        # Arrange
        hut = self.given_hut()

        # Act
        hut.turn_around()

        # Assert
        self.assert_state(hut,
                          facing=Facing.TRAVELER,
                          firewood=100.0 - Firewood.TURN_AROUND,
                          position_m=0.0)  # fmt: skip

    def test_tc26_turn_around_while_sitting_raises(self):
        """TC-26: разворот сидя."""
        # Arrange
        hut = self.given_hut(sitting=True)

        # Act / Assert
        self.assert_raises_with(HutIsSitting, Messages.IS_SITTING, hut.turn_around)
        self.assert_state(hut, facing=Facing.FOREST, firewood=100.0)


class TestWalkingHutObstacles(Steps):
    """Препятствия (SPEC 3.4.6, 3.4.7)."""

    def test_tc27_can_step_over_fence(self):
        """TC-27: забор 1.5 м ниже ног 2.0 м."""
        # Arrange
        hut = self.given_hut()

        # Act
        result = hut.can_step_over(Obstacle.FENCE)

        # Assert
        self.assertIs(result, True)
        self.assert_state(hut, firewood=100.0)

    def test_tc28_cannot_step_over_boulder(self):
        """TC-28: валун 2.5 м выше ног 2.0 м; проверка не тратит дрова."""
        # Arrange
        hut = self.given_hut()

        # Act
        result = hut.can_step_over(Obstacle.BOULDER)

        # Assert
        self.assertIs(result, False)
        self.assert_state(hut, firewood=100.0)

    def test_tc29_step_over_fence(self):
        """TC-29: перешагнуть забор."""
        # Arrange
        hut = self.given_hut()

        # Act
        hut.step_over(Obstacle.FENCE)

        # Assert
        self.assert_state(hut, firewood=100.0 - Firewood.STEP_OVER, position_m=0.0)

    def test_tc30_step_over_too_high_raises(self):
        """TC-30: стена 4.0 м выше ног."""
        # Arrange
        hut = self.given_hut()

        # Act / Assert
        self.assert_raises_with(HutCannotStepOver, Messages.CANNOT_STEP_OVER,
                                hut.step_over, Obstacle.WALL)  # fmt: skip
        self.assert_state(hut, firewood=100.0)

    def test_tc31_step_over_unknown_obstacle_raises(self):
        """TC-31: неизвестное препятствие."""
        # Arrange
        hut = self.given_hut()

        # Act / Assert
        self.assert_raises_with(ValueError, Messages.UNKNOWN_OBSTACLE,
                                hut.step_over, Obstacle.UNKNOWN)  # fmt: skip
        self.assert_state(hut, firewood=100.0)


class TestWalkingHutFirewood(Steps):
    """Печь (SPEC 3.4.8)."""

    def test_tc32_add_firewood(self):
        """TC-32: подбросить 30 дров сидя."""
        # Arrange
        hut = self.given_hut(firewood=50.0, sitting=True)

        # Act
        hut.add_firewood(30)

        # Assert
        self.assert_state(hut, firewood=80.0)

    def test_tc33_add_firewood_caps_at_max(self):
        """TC-33: печь не переполняется выше 100."""
        # Arrange
        hut = self.given_hut(firewood=50.0, sitting=True)

        # Act
        hut.add_firewood(1000)

        # Assert
        self.assert_state(hut, firewood=Firewood.MAX)

    def test_tc34_add_firewood_standing_raises(self):
        """TC-34: подбросить дров стоя."""
        # Arrange
        hut = self.given_hut(firewood=50.0)

        # Act / Assert
        self.assert_raises_with(HutWrongPose, Messages.FIREWOOD_ONLY_SITTING,
                                hut.add_firewood, 10)  # fmt: skip
        self.assert_state(hut, firewood=50.0)

    def test_tc35_add_zero_firewood_raises(self):
        """TC-35: подбросить 0 дров."""
        # Arrange
        hut = self.given_hut(sitting=True)

        # Act / Assert
        self.assert_raises_with(ValueError, Messages.AMOUNT_POSITIVE, hut.add_firewood, 0)
        self.assert_state(hut, firewood=100.0)


class TestWalkingHutLegsAndStatus(Steps):
    """Ноги и снимок состояния (SPEC 3.4.9, 3.4.10)."""

    def test_tc36_damage_one_leg(self):
        """TC-36: одна нога повреждена — избушка стоит."""
        # Arrange
        hut = self.given_hut()

        # Act
        hut.damage_leg()

        # Assert
        self.assert_state(hut, healthy_legs=Legs.LAME, pose=Pose.STANDING)

    def test_tc37_damage_both_legs_sits_down(self):
        """TC-37: обе ноги повреждены — избушка садится."""
        # Arrange
        hut = self.given_hut()

        # Act
        hut.damage_leg()
        hut.damage_leg()

        # Assert
        self.assert_state(hut, healthy_legs=Legs.BROKEN, pose=Pose.SITTING)

    def test_tc38_damage_leg_when_both_broken_raises(self):
        """TC-38: повредить ногу, когда обе уже сломаны."""
        # Arrange
        hut = self.given_hut(healthy_legs=Legs.BROKEN)

        # Act / Assert
        self.assert_raises_with(HutCannotWalk, Messages.LEGS_ALREADY_BROKEN, hut.damage_leg)
        self.assert_state(hut, healthy_legs=Legs.BROKEN)

    def test_tc39_get_status(self):
        """TC-39: снимок состояния содержит ровно нужные ключи и значения."""
        # Arrange
        hut = self.given_hut()

        # Act
        status = hut.get_status()

        # Assert
        self.assertEqual(set(status), STATUS_KEYS)
        self.assert_status(status,
                           name=Hut.NAME,
                           position_m=0.0,
                           firewood=100.0,
                           pose=Pose.STANDING,
                           facing=Facing.FOREST,
                           healthy_legs=Legs.HEALTHY)  # fmt: skip
