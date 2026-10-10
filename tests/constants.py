"""Константы и тестовые данные «Бабкин Экспресс» (SPEC.md)."""

PLACES = 6


class Hut:
    NAME = "Избушка"
    MASS_KG = 1000.0
    LEG_LENGTH_M = 2.0


class Firewood:
    MIN = 0.0
    MAX = 100.0
    DEFAULT = 100.0
    STAND_UP = 1.0
    TURN_AROUND = 0.5
    STEP_OVER = 3.0


class Pose:
    STANDING = "standing"
    SITTING = "sitting"


class Facing:
    FOREST = "forest"
    TRAVELER = "traveler"


class Legs:
    HEALTHY = 2
    LAME = 1
    BROKEN = 0


class Obstacle:
    LOG = "log"
    FENCE = "fence"
    BOULDER = "boulder"
    WALL = "wall"
    UNKNOWN = "river"


STATUS_KEYS = {"name", "position_m", "firewood", "pose", "facing", "healthy_legs"}


class Messages:
    EMPTY_NAME = "Имя не может быть пустым."
    MASS_RANGE = "Масса должна быть в диапазоне 300…3000 кг."
    LEG_RANGE = "Длина ног должна быть в диапазоне 0.5…5.0 м."
    FIREWOOD_RANGE = "Запас дров должен быть в диапазоне 0…100."
    DISTANCE_POSITIVE = "Расстояние должно быть больше 0."
    AMOUNT_POSITIVE = "Количество дров должно быть больше 0."
    UNKNOWN_OBSTACLE = "Неизвестное препятствие."
    CANNOT_WALK = "Избушка не может идти: обе ноги сломаны."
    LEGS_ALREADY_BROKEN = "Обе ноги уже сломаны."
    IS_SITTING = "Избушка сидит. Сначала встаньте."
    IS_LAME = "Избушка хромает: действие требует двух здоровых ног."
    OUT_OF_FIREWOOD = "Не хватает дров в печи."
    CANNOT_STEP_OVER = "Ноги слишком короткие для этого препятствия."
    ALREADY_SITTING = "Избушка уже сидит."
    ALREADY_STANDING = "Избушка уже стоит."
    FIREWOOD_ONLY_SITTING = "Подбросить дров можно только когда избушка сидит."
