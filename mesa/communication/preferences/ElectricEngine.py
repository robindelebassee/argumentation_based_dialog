from communication.preferences.Item import Item

class ElectricEngine(Item):
    """Type of engine that will be discussed.

    Args:
        Item (unique_id): the id of the created engine
        Item (quality_factor): a coefficient that will be used as a multiplication factor to define value for each criteria. 
            It has to be between 0 and 1.
    """
    
    def __init__(self, unique_id, quality_factor):
        super().__init__(unique_id)
        self.production_cost = 14000 + (20000 - 14000) * quality_factor # between 14000 and 20000 (increase with higher quality)
        self.consumption = 0 # always at zero because electric engines don't consume gas
        self.durability = 1 + (3 - 1) * quality_factor # between 1 and 3 (increase with higher quality)
        self.environment_impact = 3 + (1 - 3) * quality_factor # between 1 and 3 (decrease with higher quality)
        self.noise = 60 + (40 - 60) * quality_factor # between 40 and 60 (decrease with higher quality)
        self.cost_per_km = 0.05 + (0.02 - 0.05) * quality_factor # between 0.02 and 0.05 (decrease with higher quality)
        