#!/usr/bin/env python3
import random as rd

# from communication.preferences.CriterionName import CriterionName
# from communication.preferences.CriterionValue import CriterionValue
# from communication.preferences.Item import Item
# from communication.preferences.Value import Value

from CriterionName import CriterionName
from CriterionValue import CriterionValue
from Item import Item
from Value import Value
from EnginesCorpus import EnginesCorpus


class Preferences:
    """Preferences class.
    This class implements the preferences of an agent.

    attr:
        criterion_name_list: the list of criterion name (ordered by importance)
        criterion_value_list: the list of criterion value
    """
    # à supprimer après
    # criterion_category_range = {
    #     'PRODUCTION_COST': [(17000,19000), (14000,16000), (11000,13000)],
    #     'CONSUMPTION': [(6,8), (3,5), (0.1,2)],
    #     'DURABILITY': [(1.6,2), (2.3,2.7), (3.0,3.4)],
    #     'ENVIRONMENT_IMPACT': [(3.4,3.0), (2.7, 2.3), (2.0, 1.6)],
    #     'NOISE': [(68,72), (58,62), (48,52)],
    #     'COST_PER_KM': [(0.1, 0.08), (0.06,0.05), (0.02,0.03)],
    # }

    def __init__(self, item_list=None):
        """Creates a new Preferences object.
        Pass an item_list parameter which contains the Engine corpus that will be discussed by the agents.
        """
        
        self.__item_list = item_list
        
        criterion_name_list = [
            CriterionName.PRODUCTION_COST, 
            CriterionName.CONSUMPTION,
            CriterionName.DURABILITY,
            CriterionName.ENVIRONMENT_IMPACT,
            CriterionName.NOISE,
            CriterionName.COST_PER_KM
        ]
        rd.shuffle(criterion_name_list)
        self.__criterion_name_list = criterion_name_list
        
        # expliquer comment on définit nos ranges
        self.__criterion_category = {
            'PRODUCTION_COST': [rd.randrange(17000,19000), rd.randrange(14000,16000), rd.randrange(11000,13000)],
            'CONSUMPTION': [rd.randrange(60,80)/10, rd.randrange(30,50)/10, rd.randrange(1,20)/10],
            'DURABILITY': [rd.randrange(-20,-16)/10, rd.randrange(-27,-23)/10, rd.randrange(-34,-30)/10], # ce critère est négatif 
            'ENVIRONMENT_IMPACT': [rd.randrange(30,34)/10, rd.randrange(23, 27)/10, rd.randrange(16, 20)/10],
            'NOISE': [rd.randrange(68,72), rd.randrange(58,62), rd.randrange(48,52)],
            'COST_PER_KM': [rd.randrange(80, 100)/1000, rd.randrange(50,60)/1000, rd.randrange(20,30)/1000],
        }
        
        self.__criterion_value_list = self.evaluate_items(item_list) if item_list else [] # ordre pas important
        
    
    def evaluate_items(self, item_list):
        """Evaluate each item of the list"""
        criterion_value_list = []        
        for item in item_list:
            evaluation = self.evaluate_item(item)
            for criterion, value in evaluation.items():
                criterion_value_list.append(CriterionValue(item, criterion, value))
        # for criterion_value in criterion_value_list:
        #     self.add_criterion_value(criterion_value)
        return criterion_value_list
    
    def evaluate_item(self, item):
        """Attribute a category for each criterion given the preferences of the agent to the item.
        """
        
        dict_item = vars(item)
        evaluation = {
            'PRODUCTION_COST': 0,
            'CONSUMPTION': 0,
            'DURABILITY': 0,
            'ENVIRONMENT_IMPACT': 0,
            'NOISE': 0,
            'COST_PER_KM': 0,
        }
        for criterion in self.__criterion_name_list:
            if dict_item[criterion.name] > self.__criterion_category[criterion.name][0]:
                evaluation[criterion.name] = Value.VERY_BAD
            elif dict_item[criterion.name] > self.__criterion_category[criterion.name][1]:
                evaluation[criterion.name] = Value.BAD
            elif dict_item[criterion.name] > self.__criterion_category[criterion.name][2]:
                evaluation[criterion.name] = Value.GOOD
            else:
                evaluation[criterion.name] = Value.VERY_GOOD
        
        return evaluation        

    def get_criterion_name_list(self):
        """Returns the list of criterion name.
        """
        return self.__criterion_name_list

    def get_criterion_value_list(self):
        """Returns the list of criterion value.
        """
        return self.__criterion_value_list

    def set_criterion_name_list(self, criterion_name_list):
        """Sets the list of criterion name.
        """
        self.__criterion_name_list = criterion_name_list

    def add_criterion_value(self, criterion_value):
        """Adds a criterion value in the list.
        """
        self.__criterion_value_list.append(criterion_value)

    def get_value(self, item, criterion_name):
        """Gets the value for a given item and a given criterion name.
        """
        for value in self.__criterion_value_list:
            if value.get_item() == item and value.get_criterion_name() == criterion_name.name:
                return value.get_value()
        return None

    def is_preferred_criterion(self, criterion_name_1, criterion_name_2):
        """Returns if a criterion 1 is preferred to the criterion 2.
        """
        for criterion_name in self.__criterion_name_list:
            if criterion_name == criterion_name_1:
                return True
            if criterion_name == criterion_name_2:
                return False

    def is_preferred_item(self, item_1, item_2):
        """Returns if the item 1 is preferred to the item 2.
        """
        return item_1.get_score(self) > item_2.get_score(self)

    def most_preferred(self, item_list=None, evaluation_needed=True):
        """Returns the most preferred item from a list.
        """
        # To be completed
        if item_list:
            if evaluation_needed:
                self.__criterion_value_list = self.evaluate_items(item_list)
            self.__item_list = item_list
            self.__item_scores = [item.get_score(self) for item in self.__item_list]
        score_max = max(self.__item_scores)
        return self.__item_list[self.__item_scores.index(score_max)]

    def is_item_among_top_10_percent(self, item, item_list=None, evaluation_needed=True):
        """
        Return whether a given item is among the top 10 percent of the preferred items.

        :return: a boolean, True means that the item is among the favourite ones
        """
        # To be completed
        if item_list:
            if evaluation_needed:
                self.__criterion_value_list = self.evaluate_items(item_list)
            self.__item_list = item_list
            self.__item_scores = [item.get_score(self) for item in self.__item_list]
            self.__item_ordered_list = [item for _,item in sorted(zip(self.__item_scores,self.__item_list))]
        is_top_item = self.__item_ordered_list.index(item) < int(0.1 * len(self.__item_ordered_list)) + 1
        return is_top_item


if __name__ == '__main__':
    """Testing the Preferences class.
    """
    
    engines = EnginesCorpus(10)
    engines_list = engines.electrics + engines.diesels
    
    agent_pref = Preferences(engines_list)
    # agent_pref.set_criterion_name_list([CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
    #                                     CriterionName.CONSUMPTION, CriterionName.DURABILITY,
    #                                     CriterionName.NOISE, CriterionName.COST_PER_KM])

    # diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
    # agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.PRODUCTION_COST,
    #                                               Value.VERY_GOOD))
    # agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.CONSUMPTION,
    #                                               Value.GOOD))
    # agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.DURABILITY,
    #                                               Value.VERY_GOOD))
    # agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.ENVIRONMENT_IMPACT,
    #                                               Value.VERY_BAD))
    # agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.NOISE,
    #                                               Value.VERY_BAD))

    # electric_engine = Item("Electric Engine", "A very quiet engine")
    # agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.PRODUCTION_COST,
    #                                               Value.BAD))
    # agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.CONSUMPTION,
    #                                               Value.VERY_BAD))
    # agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.DURABILITY,
    #                                               Value.GOOD))
    # agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.ENVIRONMENT_IMPACT,
    #                                               Value.VERY_GOOD))
    # agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.NOISE,
    #                                               Value.VERY_GOOD))
    
    diesel_engine = engines.diesels[0]
    electric_engine = engines.electrics[0]
    
    print(agent_pref.get_criterion_value_list())

    """test list of preferences"""
    print(diesel_engine)
    print(electric_engine)
    print(diesel_engine.get_value(agent_pref, CriterionName.PRODUCTION_COST))
    print(agent_pref.is_preferred_criterion(CriterionName.CONSUMPTION, CriterionName.NOISE))
    print('Electric Engine > Diesel Engine : {}'.format(agent_pref.is_preferred_item(electric_engine, diesel_engine)))
    print('Diesel Engine > Electric Engine : {}'.format(agent_pref.is_preferred_item(diesel_engine, electric_engine)))
    print('Electric Engine (for agent 1) = {}'.format(electric_engine.get_score(agent_pref)))
    print('Diesel Engine (for agent 1) = {}'.format(diesel_engine.get_score(agent_pref)))
    print('Most preferred item is : {}'.format(agent_pref.most_preferred([diesel_engine, electric_engine], evaluation_needed=False).get_name()))
