from communication.preferences.Item import Item

class DieselEngine(Item):
    """Type of engine that will be discussed.

    Args:
        Item (unique_id): the id of the created engine
        Item (quality_factor): a coefficient that will be used as a multiplication factor to define value for each criteria. 
            It has to be between 0 and 1.
    """
    
    def __init__(self, unique_id, quality_factor):
        description = "Diesel engine with quality factor {}".format(quality_factor)
        super().__init__(unique_id, description)
        self.PRODUCTION_COST = 10000 + (16000 - 10000) * quality_factor # between 10000 and 16000 € (increase with higher quality)
        self.CONSUMPTION = 8 + (4 - 8) * quality_factor # between 4 and 8 L/100km (decrease with higher quality)
        self.DURABILITY = 2 + (4 - 2) * quality_factor * (-1) # between 2 and 4 (increase with higher quality)
        # * -1 because its the only criteria that we want to maximise 
        self.ENVIRONMENT_IMPACT = 4 + (2 - 4) * quality_factor # between 2 and 4 (decrease with higher quality)
        self.NOISE = 80 + (55 - 80) * quality_factor # between 55 and 80 dB (decrease with higher quality)
        self.COST_PER_KM = 0.12 + (0.08 - 0.12) * quality_factor # between 0.08 and 0.12 €/km (decrease with higher quality)
        