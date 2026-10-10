"""Сценарные (функциональные) тесты (SPEC 4.2, TC-40…TC-47), паттерн GWT.

Все действия выполняются через пилота «Баба Яга» и капкан; итог — через ``осмотреться()``.
"""

from tests.constants import Facing, Legs, Messages, Obstacle, Pose
from tests.steps import Steps
from walking_hut import (
    HutCannotStepOver,
    HutCannotWalk,
    HutIsLame,
    HutIsSitting,
    HutOutOfFirewood,
    HutWrongPose,
)


class TestScenarios(Steps):
    """Сквозные сценарии 40–47."""

    def test_tc40_traveler_at_forest(self):
        """TC-40: Путник у леса."""
        # Given базовая избушка, стоит к лесу
        yaga = self.given_pilot()

        # When Баба Яга идёт 300 м
        minutes = yaga.пройти(300)
        # Then время 15 мин, пройдено 300 м, дров 94
        self.assertAlmostEqual(minutes, 15.0)
        self.assert_state(self.hut, position_m=300.0, firewood=94.0)

        # When «стань ко мне передом»
        yaga.стань_ко_мне_передом()
        # Then к путнику, дров 93.5
        self.assert_state(self.hut, facing=Facing.TRAVELER, firewood=93.5)

        # When присесть и подкинуть 20 дров
        yaga.присесть()
        yaga.подкинуть_дров(20)

        # Then дров не больше максимума; итоговое состояние
        self.assert_status(yaga.осмотреться(),
                           position_m=300.0,
                           firewood=100.0,
                           pose=Pose.SITTING,
                           facing=Facing.TRAVELER,
                           healthy_legs=Legs.HEALTHY)  # fmt: skip

    def test_tc41_obstacle_course(self):
        """TC-41: Полоса препятствий."""
        # Given базовая избушка
        yaga = self.given_pilot()

        # When перешагнуть бревно
        yaga.перешагнуть(Obstacle.LOG)
        # Then дров 97
        self.assert_state(self.hut, firewood=97.0)

        # When можно ли перешагнуть валун
        # Then нельзя, дрова не тратятся
        self.assertIs(yaga.можно_перешагнуть(Obstacle.BOULDER), False)
        self.assert_state(self.hut, firewood=97.0)

        # When пройти 50 м
        yaga.пройти(50)
        # Then пройдено 50, дров 96
        self.assert_state(self.hut, position_m=50.0, firewood=96.0)

        # When перешагнуть забор
        yaga.перешагнуть(Obstacle.FENCE)
        # Then дров 93
        self.assert_state(self.hut, firewood=93.0)

        # When перешагнуть стену
        # Then HutCannotStepOver, дрова не тратятся
        self.assert_raises_with(HutCannotStepOver, Messages.CANNOT_STEP_OVER,
                                yaga.перешагнуть, Obstacle.WALL)  # fmt: skip

        # Then итоговое состояние
        self.assert_status(yaga.осмотреться(),
                           position_m=50.0,
                           firewood=93.0,
                           pose=Pose.STANDING)  # fmt: skip

    def test_tc42_trap_in_thicket(self):
        """TC-42: Капкан в чаще."""
        # Given базовая избушка
        yaga = self.given_pilot()

        # When пройти 100 м
        yaga.пройти(100)
        # Then пройдено 100, дров 98
        self.assert_state(self.hut, position_m=100.0, firewood=98.0)

        # When срабатывает капкан
        self.kapkan.защемить(self.hut)
        # Then одна здоровая нога, стоит
        self.assert_state(self.hut, healthy_legs=Legs.LAME, pose=Pose.STANDING)

        # When пройти ещё 100 м
        minutes = yaga.пройти(100)
        # Then вдвое медленнее и вдвое дороже
        self.assertAlmostEqual(minutes, 10.0)
        self.assert_state(self.hut, position_m=200.0, firewood=94.0)

        # When пробежать 10 м
        # Then HutIsLame
        self.assert_raises_with(HutIsLame, Messages.IS_LAME, yaga.пробежать, 10)

        # When перешагнуть бревно
        # Then HutIsLame
        self.assert_raises_with(HutIsLame, Messages.IS_LAME, yaga.перешагнуть, Obstacle.LOG)

        # Then итоговое состояние
        self.assert_status(yaga.осмотреться(),
                           position_m=200.0,
                           firewood=94.0,
                           healthy_legs=Legs.LAME,
                           pose=Pose.STANDING)  # fmt: skip

    def test_tc43_out_of_firewood_on_the_road(self):
        """TC-43: Дрова кончились в пути."""
        # Given избушка с 10 дровами
        yaga = self.given_pilot(firewood=10.0)

        # When пробежать 100 м
        minutes = yaga.пробежать(100)
        # Then 2.5 мин, пройдено 100, дров 4
        self.assertAlmostEqual(minutes, 2.5)
        self.assert_state(self.hut, position_m=100.0, firewood=4.0)

        # When пройти 300 м (нужно 6)
        # Then HutOutOfFirewood, состояние не изменилось
        self.assert_raises_with(HutOutOfFirewood, Messages.OUT_OF_FIREWOOD, yaga.пройти, 300)
        self.assert_state(self.hut, position_m=100.0, firewood=4.0)

        # When присесть и подкинуть 50 дров
        yaga.присесть()
        yaga.подкинуть_дров(50)
        # Then дров 54
        self.assert_state(self.hut, firewood=54.0)

        # When встать
        yaga.встать()
        # Then дров 53
        self.assert_state(self.hut, firewood=53.0)

        # When пройти 300 м
        yaga.пройти(300)

        # Then итоговое состояние
        self.assert_status(yaga.осмотреться(),
                           position_m=400.0,
                           firewood=47.0,
                           pose=Pose.STANDING)  # fmt: skip

    def test_tc44_double_trap(self):
        """TC-44: Двойной капкан."""
        # Given базовая избушка
        yaga = self.given_pilot()

        # When срабатывает капкан
        self.kapkan.защемить(self.hut)
        # Then одна нога, стоит
        self.assert_state(self.hut, healthy_legs=Legs.LAME, pose=Pose.STANDING)

        # When срабатывает второй капкан
        self.kapkan.защемить(self.hut)
        # Then ног нет, избушка садится
        self.assert_state(self.hut, healthy_legs=Legs.BROKEN, pose=Pose.SITTING)

        # When встать
        # Then HutCannotWalk
        self.assert_raises_with(HutCannotWalk, Messages.CANNOT_WALK, yaga.встать)

        # When пройти 10 м
        # Then HutCannotWalk
        self.assert_raises_with(HutCannotWalk, Messages.CANNOT_WALK, yaga.пройти, 10)

        # When срабатывает третий капкан
        # Then HutCannotWalk «Обе ноги уже сломаны.»
        self.assert_raises_with(HutCannotWalk, Messages.LEGS_ALREADY_BROKEN,
                                self.kapkan.защемить, self.hut)  # fmt: skip

        # Then итоговое состояние
        self.assert_status(yaga.осмотреться(),
                           position_m=0.0,
                           firewood=100.0,
                           pose=Pose.SITTING,
                           healthy_legs=Legs.BROKEN)  # fmt: skip

    def test_tc45_sitting_strike(self):
        """TC-45: Сидячая забастовка."""
        # Given базовая избушка
        yaga = self.given_pilot()

        # When присесть
        yaga.присесть()
        # Then сидит
        self.assert_state(self.hut, pose=Pose.SITTING)

        # When пройти 10 м
        # Then HutIsSitting
        self.assert_raises_with(HutIsSitting, Messages.IS_SITTING, yaga.пройти, 10)

        # When «стань ко мне передом»
        # Then HutIsSitting
        self.assert_raises_with(HutIsSitting, Messages.IS_SITTING, yaga.стань_ко_мне_передом)

        # When снова присесть
        # Then HutWrongPose «Избушка уже сидит.»
        self.assert_raises_with(HutWrongPose, Messages.ALREADY_SITTING, yaga.присесть)

        # When встать
        yaga.встать()
        # Then дров 99
        self.assert_state(self.hut, firewood=99.0)

        # When подкинуть 1 полено стоя
        # Then HutWrongPose
        self.assert_raises_with(HutWrongPose, Messages.FIREWOOD_ONLY_SITTING,
                                yaga.подкинуть_дров, 1)  # fmt: skip

        # Then итоговое состояние
        self.assert_status(yaga.осмотреться(),
                           position_m=0.0,
                           firewood=99.0,
                           pose=Pose.STANDING,
                           facing=Facing.FOREST)  # fmt: skip

    def test_tc46_long_legged_giant(self):
        """TC-46: Великан на длинных ногах."""
        # Given избушка 2500 кг, ноги 5.0 м, дров 100
        yaga = self.given_pilot(mass_kg=2500.0, leg_length_m=5.0)

        # When перешагнуть стену
        yaga.перешагнуть(Obstacle.WALL)
        # Then дров 97
        self.assert_state(self.hut, firewood=97.0)

        # When пробежать 200 м
        minutes = yaga.пробежать(200)
        # Then 2 мин, пройдено 200, дров 67
        self.assertAlmostEqual(minutes, 2.0)
        self.assert_state(self.hut, position_m=200.0, firewood=67.0)

        # When пройти 500 м
        minutes = yaga.пройти(500)
        # Then 10 мин, пройдено 700, дров 42
        self.assertAlmostEqual(minutes, 10.0)
        self.assert_state(self.hut, position_m=700.0, firewood=42.0)

        # When дважды «стань ко мне передом»
        yaga.стань_ко_мне_передом()
        yaga.стань_ко_мне_передом()

        # Then снова к лесу; итоговое состояние
        self.assert_status(yaga.осмотреться(),
                           position_m=700.0,
                           firewood=41.0,
                           facing=Facing.FOREST)  # fmt: skip

    def test_tc47_thrifty_little_hut(self):
        """TC-47: Экономная малышка."""
        # Given избушка 300 кг, ноги 0.5 м, дров 3
        yaga = self.given_pilot(mass_kg=300.0, leg_length_m=0.5, firewood=3.0)

        # When можно ли перешагнуть бревно
        # Then можно — длина ног ровно равна высоте
        self.assertIs(yaga.можно_перешагнуть(Obstacle.LOG), True)

        # When перешагнуть бревно
        yaga.перешагнуть(Obstacle.LOG)
        # Then дров 0
        self.assert_state(self.hut, firewood=0.0)

        # When пройти 1 м
        # Then HutOutOfFirewood
        self.assert_raises_with(HutOutOfFirewood, Messages.OUT_OF_FIREWOOD, yaga.пройти, 1)

        # When присесть, подкинуть 100 дров и встать
        yaga.присесть()
        yaga.подкинуть_дров(100)
        yaga.встать()
        # Then дров 99
        self.assert_state(self.hut, firewood=99.0)

        # When пройти 100 м
        minutes = yaga.пройти(100)

        # Then 20 мин; итоговое состояние
        self.assertAlmostEqual(minutes, 20.0)
        self.assert_status(yaga.осмотреться(),
                           position_m=100.0,
                           firewood=98.4)  # fmt: skip
