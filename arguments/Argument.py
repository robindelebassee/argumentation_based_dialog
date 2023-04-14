#!/ usr/bin /env python3

from arguments.Comparison import Comparison
from arguments.CoupleValue import CoupleValue


class Argument :
    """ Argument class.
    This class implements an argument used during the interaction.

    attr:
        decision:
        item:
        comparison_list:
        couple_values_list:
    """

    def __init__ (self, boolean_decision, item_name):
        """ Creates a new Argument.
        :param boolean_decision: True if the argument is positive for the given item, False if not.
        """
        self.boolean_decision = boolean_decision
        self.item_name = item_name
        self.comparison_list = []
        self.couple_values_list = []

    def add_premiss_comparison (self, criterion_name_1, criterion_name_2):
        """ Adds a premiss comparison in the comparison list. 
        
        Criterion 1 has to be better ranked in the preferences system of the agent than Criterion 2.
        """
        self.comparison_list.append(Comparison(criterion_name_1, criterion_name_2))

    def add_premiss_couple_values (self, criterion_name, value):
        """ Add a premiss couple values in the couple values list.
        
        Value has to stand for the CriterionValue object instead of an instance of the Value object.
        """
        self.couple_values_list.append(CoupleValue(criterion_name, value))
    
    def List_supporting_proposal (self, item_name, preferences):
        """ Generate a list of premisses which can be used to support an item
            : param item : Item - name of the item
            : return : list of all premisses PRO an item ( sorted by order of importance
            based on agent ’s preferences )
        """
        # Add criterion/value premisses
        # Search for all the criterion values in the preferences for given item having a good or very good review
        # get list of criterion ordered by preference for the agent
        ordered_criterion = preferences._Preferences__criterion_name_list
        # get the full item object corresponding to the name
        working_item = None
        for item in preferences._Preferences__item_list:
            if item._Item__name == item_name:
                working_item = item
                break
        assert working_item, 'Given item {} not found in preferences item list.'.format(item_name)
        # Retrieving item evaluation
        item_evaluation = {}
        for criterion in ordered_criterion:
            item_evaluation[criterion] = preferences.get_value(working_item, criterion)
        # Searching for good and very good values in evaluation
        supporting_proposal = []
        for criterion, value in item_evaluation.items():
            if value.value >= 2:
                self.add_premiss_couple_values(criterion, value)
        
        # Add criterion/criterion premisses:
        for best_index in range(len(ordered_criterion)-1):
            for worst_index in range(best_index+1, len(ordered_criterion)):
                self.add_premiss_comparison(ordered_criterion[best_index], ordered_criterion[worst_index])

    
    def List_attacking_proposal (self, item_name, preferences):
        """ Generate a list of premisses which can be used to attack an item
            : param item : Item - name of the item
            : return : list of all premisses CON an item ( sorted by order of importance
            based on preferences )
        """
        # Search for all the criterion values in the preferences for given item having a good or very good review
        # get list of criterion ordered by preference for the agent
        ordered_criterion = preferences._Preferences__criterion_name_list
        # get the full item object corresponding to the name
        working_item = None
        for item in preferences._Preferences__item_list:
            if item._Item__name == item_name:
                working_item = item
                break
        assert working_item, 'Given item {} not found in preferences item list.'.format(item_name)
        # Retrieving item evaluation
        item_evaluation = {}
        for criterion in ordered_criterion:
            item_evaluation[criterion] = preferences.get_value(working_item, criterion)
        # Searching for good and very good values in evaluation
        supporting_proposal = []
        for criterion, value in item_evaluation.items():
            if value < 2:
                self.add_premiss_couple_values(criterion, value)
        
        # Add criterion/criterion premisses:
        for best_index in range(len(ordered_criterion)-1):
            for worst_index in range(best_index+1, len(ordered_criterion)):
                self.add_premiss_comparison(ordered_criterion[best_index], ordered_criterion[worst_index])