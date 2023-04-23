#!/usr/bin/env python3

from enum import Enum


class CriterionName(Enum):
    """CriterionName enum class.
    Enumeration containing the possible CriterionName.
    """
    PRODUCTION_COST = 0, 'PRODUCTION_COST'
    CONSUMPTION = 1, 'CONSUMPTION'
    DURABILITY = 2, 'DURABILITY'
    ENVIRONMENT_IMPACT = 3, 'ENVIRONMENT_IMPACT'
    NOISE = 4, 'NOISE'
    COST_PER_KM = 5, 'COST_PER_KM'
    
    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        return member


criterionName_classdict = {
    'PRODUCTION_COST': CriterionName.PRODUCTION_COST,
    'CONSUMPTION': CriterionName.CONSUMPTION,
    'DURABILITY': CriterionName.DURABILITY,
    'ENVIRONMENT_IMPACT': CriterionName.ENVIRONMENT_IMPACT,
    'NOISE': CriterionName.NOISE,
    'COST_PER_KM': CriterionName.COST_PER_KM,
}
