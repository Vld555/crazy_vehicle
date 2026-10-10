"""Иерархия исключений «Бабкин Экспресс» (SPEC, раздел 6).

Ошибки параметров описаны стандартными ``TypeError`` / ``ValueError`` и здесь не объявляются.
"""


class CrazyVehicleError(Exception):
    """Корень доменных исключений безумного транспорта."""


class WalkingHutError(CrazyVehicleError):
    """Корень доменных исключений ходячей избушки."""


class HutCannotWalk(WalkingHutError):
    """Нет здоровых ног: ходить, бегать и вставать невозможно."""


class HutIsSitting(WalkingHutError):
    """Действие невозможно, пока избушка сидит."""


class HutIsLame(WalkingHutError):
    """Действие требует двух здоровых ног."""


class HutOutOfFirewood(WalkingHutError):
    """Не хватает дров в печи на действие."""


class HutCannotStepOver(WalkingHutError):
    """Препятствие выше длины ног."""


class HutWrongPose(WalkingHutError):
    """Действие несовместимо с текущей позой избушки."""
