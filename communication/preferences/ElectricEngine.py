from communication.preferences.Item import Item


class ElectricEngine(Item):
    """Type of engine that will be discussed.

    Args:
        Item (unique_id): the id of the created engine
        Item (quality_factor): a coefficient that will be used as a multiplication factor to define value for each criteria. 
            It has to be between 0 and 1.
    """
    
    def __init__(self, unique_id, quality_factor):
        description = "Electric engine with quality factor {}".format(quality_factor)
        super().__init__(unique_id, description)
        self.PRODUCTION_COST = 14000 + (20000 - 14000) * quality_factor # between 14000 and 20000 (increase with higher quality)
        self.CONSUMPTION = 0 # always at zero because electric engines don't consume gas
        self.DURABILITY = 1 + (3 - 1) * quality_factor * (-1) # between 1 and 3 (increase with higher quality)
        # * -1 because its the only criteria that we want to maximise 
        self.ENVIRONMENT_IMPACT = 3 + (1 - 3) * quality_factor # between 1 and 3 (decrease with higher quality)
        self.NOISE = 60 + (40 - 60) * quality_factor # between 40 and 60 (decrease with higher quality)
        self.COST_PER_KM = 0.05 + (0.02 - 0.05) * quality_factor # between 0.02 and 0.05 (decrease with higher quality)
        