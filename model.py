from enum import Enum


class UserLevel(Enum):
    none = ''
    junior = 'Новичок (Junior)'
    paid_middle = 'Средний уровень (Middle)'
    unpaid_middle = 'Средний уровень (Middle) 🔒'
    paid_senior = 'Продвинутый уровень (Senior)'
    unpaid_senior = 'Продвинутый уровень (Senior) 🔒'
