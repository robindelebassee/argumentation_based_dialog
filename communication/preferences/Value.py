#!/usr/bin/env python3

from enum import Enum


class Value(Enum):
    """Value enum class.
    Enumeration containing the possible Value.
    """
    VERY_BAD = 0, 'VERY BAD'
    BAD = 1, 'BAD'
    GOOD = 2, 'GOOD'
    VERY_GOOD = 3, 'VERY GOOD'
    
    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        return member
