from collections.preferences.Item import Item

class ElectricEngine(Item):
    """Type of engine that will be discussed.

    Args:
        Item (unique_id): the id of the created engine
        Item (coeff): the coefficient will be used as a multiplication factor to define value for each criteria. 
                    It has to be between 0 and 1.
    """
    def __init__(self, unique_id, coeff):
        super().__init__(unique_id)
        self.c1 = 10000 + (20000 - 10000) * coeff
        self.c2 = None
        self.c3 = None
        self.c4 = None
        self.c5 = None
        self.c6 = None