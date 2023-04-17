#!/ usr/bin /env python3

from arguments.Comparison import Comparison
from arguments.CoupleValue import CoupleValue


class Argument:
    """ Argument class.
    This class implements an argument used during the interaction.

    attr:
        decision:
        item:
        comparison_list:
        couple_values_list:
    """

    def __init__(self, boolean_decision, item_name):
        """ Creates a new Argument.
        :param boolean_decision: True if the argument is positive for the given item, False if not.
        """
        self.boolean_decision = boolean_decision
        self.item_name = item_name
        self.comparison_list = []
        self.couple_values_list = []
        self.ordered_criterion = []

    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """ Add a premiss comparison in the comparison list. 
        
        Criterion 1 has to be better ranked in the preferences system of the agent than Criterion 2.
        """
        self.comparison_list.append(Comparison(criterion_name_1, criterion_name_2))

    def add_premiss_couple_values(self, criterion_name, value):
        """ Add a premiss couple values in the couple values list.
        
        Value has to stand for the CriterionValue object instead of an instance of the Value object.
        """
        self.couple_values_list.append(CoupleValue(criterion_name, value))
    
    def clear_existing_premisses(self):
        """Clear premisses storage lists. 
        
        It will be called before new premisses generation to insure there are no remaining premisses
        that support the opposite opinion about the considered item.
        """
        self.comparison_list = []
        self.couple_values_list = []
    
    def List_supporting_proposal(self, item_name, preferences):
        """ Generate a list of premisses which can be used to support an item
            : param item : Item - name of the item
            : return : list of all premisses PRO an item ( sorted by order of importance
            based on agent ’s preferences )
        """
        
        # Clear premisses storage lists
        if item_name == self.item_name:
            self.clear_existing_premisses()
        
        premisses_couple_values = []
        premisses_comparison = []
        
        # get the full item object corresponding to the name
        working_item = None
        for item in preferences._Preferences__item_list:
            if item._Item__name == item_name:
                working_item = item
                break
        assert working_item, 'Given item {} not found in preferences item list.'.format(item_name)
        
        # Add criterion/value premisses
        # Search for all the criterion values in the preferences for given item having a good or very good review
        # get list of criterion ordered by preference for the agent
        ordered_criterion = preferences._Preferences__criterion_name_list
        # Retrieving item evaluation
        item_evaluation = {}
        for criterion in ordered_criterion:
            item_evaluation[criterion] = preferences.get_value(working_item, criterion)
        # Searching for good and very good values in evaluation
        for criterion, value in item_evaluation.items():
            if value.value >= 2:
                if item_name == self.item_name:
                    self.add_premiss_couple_values(criterion, value)
                else: 
                    premisses_couple_values.append(CoupleValue(criterion, value))
        
        # Add criterion/criterion premisses:
        for best_index in range(len(ordered_criterion)-1):
            for worst_index in range(best_index+1, len(ordered_criterion)):
                if item_name == self.item_name:
                    self.add_premiss_comparison(ordered_criterion[best_index], ordered_criterion[worst_index])
                else:
                    premisses_comparison.append(Comparison(ordered_criterion[best_index], ordered_criterion[worst_index]))
        
        self.ordered_criterion = ordered_criterion
        
        return premisses_comparison, premisses_couple_values
    
    
    def List_attacking_proposal(self, item_name, preferences):
        """ Generate a list of premisses which can be used to attack an item
            : param item : Item - name of the item
            : return : list of all premisses CON an item ( sorted by order of importance
            based on preferences )
        """
        # Clear premisses storage lists
        if item_name == self.item_name:
            self.clear_existing_premisses()
        
        premisses_couple_values = []
        premisses_comparison = []        
        
        # get the full item object corresponding to the name
        working_item = None
        for item in preferences._Preferences__item_list:
            if item._Item__name == item_name:
                working_item = item
                break
        assert working_item, 'Given item {} not found in preferences item list.'.format(item_name)
        
        # Add criterion/value premisses
        # Search for all the criterion values in the preferences for given item having a good or very good review
        # get list of criterion ordered by preference for the agent
        ordered_criterion = preferences._Preferences__criterion_name_list
        # Retrieving item evaluation
        item_evaluation = {}
        for criterion in ordered_criterion:
            item_evaluation[criterion] = preferences.get_value(working_item, criterion)
        # Searching for good and very good values in evaluation
        for criterion, value in item_evaluation.items():
            if value < 2:
                if item_name == self.item_name:
                    self.add_premiss_couple_values(criterion, value)
                else: 
                    premisses_couple_values.append(CoupleValue(criterion, value))
        
        # Add criterion/criterion premisses:
        for best_index in range(len(ordered_criterion)-1):
            for worst_index in range(best_index+1, len(ordered_criterion)):
                if item_name == self.item_name:
                    self.add_premiss_comparison(ordered_criterion[best_index], ordered_criterion[worst_index])
                else:
                    premisses_comparison.append(Comparison(ordered_criterion[best_index], ordered_criterion[worst_index]))
        
        self.ordered_criterion = ordered_criterion
        
        return (premisses_comparison, premisses_couple_values)
    
    
    def select_best_premiss(self, argumentation_policy='best_criterion', last_opponent_crit=None):
        """Select the best premiss to build an argument according to the chosen policy.
        
        Possible argumentation policy:
            best_criterion: we choose the premiss relative to the most important available criterion in the agent order
            
        To implement if we have time:
            worst_criterion: we choose the premiss relative to the least important available criterion in the agent order
            random_criterion: we choose a random premiss
            adaptative_counter: we choose the first better available criterion according to the last argument of the opponent
        """
        chosen_comparison = None
        chosen_couple_value = None
        
        # Check if there is at least 1 remaining argument
        if not(self.couple_values_list):
            return None

        if argumentation_policy == 'best_criterion':
            
            # case 1 : first message after ask_why --> no existing counter argument
            if not last_opponent_crit:
                # simply choose the couple_values premiss for best available criterion
                for criterion in self.ordered_criterion:
                    for couple_value in self.couple_values_list:
                        if couple_value.criterion_name == criterion:
                            chosen_couple_value = couple_value
                            
            # case 2 : some previous argument exist
            else:
                # find the couple_value premiss to determine best available criterion
                for criterion in self.ordered_criterion:
                    if criterion == last_opponent_crit:
                        return None
                    for couple_value in self.couple_values_list:
                        if couple_value.criterion_name == criterion:
                            chosen_couple_value = couple_value
                            break
                # find the premiss for criterion order
                for comparison in self.comparison_list:
                    if comparison.best_criterion_name == chosen_couple_value.criterion_name and comparison.worst_criterion_name == last_opponent_crit:
                        chosen_comparison = comparison
                        break
            
            return (chosen_comparison, chosen_couple_value)