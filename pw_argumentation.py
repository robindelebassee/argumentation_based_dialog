import sys
import time as t

from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.EnginesCorpus import EnginesCorpus
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.preferences.CriterionName import criterionName_classdict
from communication.preferences.Value import value_classdict
from arguments.Argument import Argument
from arguments.CoupleValue import CoupleValue
from arguments.Comparison import Comparison


class ArgumentAgent(CommunicatingAgent):
    """ ArgumentAgent which inherit from CommunicatingAgent.
    """
    def __init__ (self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.preferences = None
        self.list_items = None
        self.interlocutor = None
        self.proposition_made = False
        self.has_proposed_best = False # Different than previous line, used for when we have to relaunch negociation after fail of the first proposed
        self.has_committed = False
        self.return_commit_received = False
        self.current_argument = None
        self.argumentation = []
        self.agreed_item = None
        
    def step(self):
        super().step()
        # check mailbox for message
        new_messages = self.get_new_messages() # it is supposed to be a singleton
        if new_messages:
            [new_message] = new_messages
            if new_message._Message__message_performative == MessagePerformative.PROPOSE:
                self.proposition_made = True
                item_concerned = self.find_item_from_name(new_message.get_content())
                if self.preferences.is_item_among_top_10_percent(item_concerned, evaluation_needed=False):
                    self.accept_item(item_concerned)
                else:
                    self.ask_why_item(item_concerned)
            elif new_message._Message__message_performative == MessagePerformative.ACCEPT:
                item_concerned = self.find_item_from_name(new_message.get_content())
                self.commit_item(item_concerned)
            elif new_message._Message__message_performative == MessagePerformative.COMMIT:
                self.return_commit_received = True
                if self.has_committed:
                    self.is_done()
                else:
                    item_concerned = self.find_item_from_name(new_message.get_content())
                    self.commit_item(item_concerned)
            elif new_message._Message__message_performative == MessagePerformative.ASK_WHY:
                item_concerned = self.find_item_from_name(new_message.get_content())
                self.support_proposal(item_concerned)
            elif new_message._Message__message_performative == MessagePerformative.ARGUE:
                content = new_message.get_content()
                sender = new_message.get_exp()
                self.argumentation.append({'sender': sender, 'content': content})
                self.counter_argue(content)
            elif new_message._Message__message_performative == MessagePerformative.STAND_BY and not self.has_proposed_best:
                proposed_item = self.preferences.most_preferred()
                self.propose_item(proposed_item)
        elif not self.proposition_made:
            proposed_item = self.preferences.most_preferred()
            self.propose_item(proposed_item)
        elif self.has_committed and self.return_commit_received:
            self.is_done()
        else:
            self.stand_by()

    def get_preference(self):
        return self.preferences

    def generate_preferences(self, List_items):
        self.list_items = List_items
        self.preferences = Preferences(List_items)
    
    def set_interlocutor(self, other_agent):
        self.interlocutor = other_agent.get_name()
    
    def propose_item(self, item):
        message = Message(self.get_name(), self.interlocutor, MessagePerformative.PROPOSE, item._Item__name)
        self.send_message(message)
        self.proposition_made = True
        self.has_proposed_best = True
        print(self.get_name(), ' - ', message._Message__message_performative, '(', item._Item__name, ')')
    
    def accept_item(self, item):
        message = Message(self.get_name(), self.interlocutor, MessagePerformative.ACCEPT, item._Item__name)
        self.send_message(message)
        print(self.get_name(), ' - ', message._Message__message_performative, '(', item._Item__name, ')')
    
    def ask_why_item(self, item):
        message = Message(self.get_name(), self.interlocutor, MessagePerformative.ASK_WHY, item._Item__name)
        self.send_message(message)
        print(self.get_name(), ' - ', message._Message__message_performative, '(', item._Item__name, ')')
        
    def commit_item(self, item):
        message = Message(self.get_name(), self.interlocutor, MessagePerformative.COMMIT, item._Item__name)
        self.send_message(message)
        self.has_committed = True
        self.agreed_item = item
        print(self.get_name(), ' - ', message._Message__message_performative, '(', item._Item__name, ')')
        
    def support_proposal(self, item):
        """Send first argument after receiving ASK_WHY message."""
        
        self.current_argument = Argument(True, item._Item__name)
        self.current_argument.List_supporting_proposal(item._Item__name, self.preferences)
        _, couple_value = self.current_argument.select_best_premiss()
        arg_content = f'{"NOT " if not(self.current_argument.boolean_decision) else ""}{item._Item__name}, {str(couple_value)}'
        
        message = Message(self.get_name(), self.interlocutor, MessagePerformative.ARGUE, arg_content)
        self.send_message(message)
        print(self.get_name(), ' - ', message._Message__message_performative, '(', arg_content, ')')
    
    def process_couple_value(self, str_couple_value):
        """Accept a str like CRITERION = VALUE and transform it to CoupleValue object."""
        [criterion, value] = str_couple_value.split(' = ')
        return CoupleValue(criterionName_classdict[criterion], value_classdict[value])
    
    def process_comparison(self, str_comparison):
        """Accept a str like CRITERION1 > CRITERION2 and transform it to Comparison object."""
        [criterion1, criterion2] = str_comparison.split(' > ')
        return Comparison(criterionName_classdict[criterion1], criterionName_classdict[criterion2])
    
    def argument_parsing(self, argument_content):
        """Return the premisses and the conclusion of the given argument message content.
        
        Argument content has format : CONCLUSION, PREMISS1 [and PREMISS2 ... and PREMISS_N]
        
        2 possibles types of arguments:
        ITEM, C = VALUE
        ITEM, C = VALUE and C > C0
        
        3 possible types of counter for argument ITEM1, C1 = VALUE1:
        NOT ITEM1, C2 > C1 and C2 = BAD_VALUE
        NOT ITEM1, C1 = BAD_VALUE
        ITEM2, C1 = VALUE2 (avec VALUE2 > VALUE1)
        the last type is only for counter argumentation, it says that given item perform better than argued item on criterion C
        
        2 possible types of counter for argument ITEM1, C1 = VALUE1 AND C1 > C0:
        ITEM2, C1 = VALUE2 (avec VALUE2 > VALUE1)
        NOT ITEM1, CO = BAD_VALUE and C0 > C1
        
        comparative symbols between values are here to inverse if the conclusion is negative (attacking an item)
        """
        conclusion, premisses = argument_content.split(', ')
        if len(conclusion) > 3:
            boolean_decision = conclusion[:4] != "NOT "
            item_name = conclusion if boolean_decision else conclusion[4:]
        premiss_list = premisses.split(" and ")
        str_couple_value = premiss_list[0]
        couple_value = self.process_couple_value(str_couple_value)
        comparison = None
        if len(premiss_list) > 1:
            str_comparison = premiss_list[1]
            comparison = self.process_comparison(str_comparison)
        return {
            'boolean_decision': boolean_decision,
            'item_name': item_name,
            'couple_value': couple_value,
            'comparison': comparison,
        }
    
    def find_item_by_name(self, item_name):
        for item in self.preferences._Preferences__item_list:
            if item._Item__name == item_name:
                return item
    
    def generate_counter_argument(self, argument_elements):
        """Input the parsed argument_message and if argument is attackable, give the best counter argument."""
        item = self.find_item_from_name(argument_elements['item_name'])
        bool_dec = argument_elements['boolean_decision']
        # Argument can have either of the 3 types defined above
        comparison = argument_elements['comparison']
        couple_value = argument_elements['couple_value']
        # Case : ITEM, C = VALUE and C > C0
        if comparison:
            best_crit = comparison.best_criterion_name
            if bool_dec:
                better_item = self.preferences.has_better_item(item, best_crit, couple_value.value, bool_dec)
                if better_item:
                    return {
                        'couple_value': CoupleValue(best_crit, self.preferences.get_value(better_item, best_crit)),
                        'comparison': None,
                        'counter_bd': bool_dec,
                        'item': better_item,
                    }
            worst_crit = comparison.worst_criterion_name
            if self.preferences.is_preferred_criterion(worst_crit, best_crit):
                worst_eval = self.preferences.get_value(item, worst_crit)
                if worst_eval.value <= 1 and bool_dec:
                    counter_cv = CoupleValue(worst_crit, worst_eval)
                    counter_cmp = Comparison(worst_crit, best_crit)
                    return {
                        'couple_value': counter_cv,
                        'comparison': counter_cmp,
                        'counter_bd': not bool_dec,
                        'item': item,
                    }
                elif worst_eval.value >= 2 and not bool_dec:
                    counter_cv = CoupleValue(worst_crit, worst_eval)
                    counter_cmp = Comparison(worst_crit, best_crit)
                    return {
                        'couple_value': counter_cv,
                        'comparison': counter_cmp,
                        'counter_bd': not bool_dec,
                        'item': item,
                    }   
        # Case : ITEM, C = VALUE
        else:
            best_crit = couple_value.criterion_name
            if bool_dec:
                better_item = self.preferences.has_better_item(item, best_crit, couple_value.value, bool_dec)
                if better_item:
                    return {
                        'couple_value': CoupleValue(best_crit, self.preferences.get_value(better_item, best_crit)),
                        'comparison': None,
                        'counter_bd': bool_dec,
                        'item': better_item,
                    }
            eval = self.preferences.get_value(item, best_crit)
            if eval.value <= 1 and bool_dec:
                return {
                    'couple_value': CoupleValue(best_crit, eval),
                    'comparison': None,
                    'counter_bd': not bool_dec,
                    'item': item,
                }
            if eval.value >= 2 and not bool_dec:
                return {
                    'couple_value': CoupleValue(best_crit, eval),
                    'comparison': None,
                    'counter_bd': not bool_dec,
                    'item': item,
                }
            else:
                for criterion in self.preferences._Preferences__criterion_name_list:
                    if criterion == best_crit:
                        break
                    eval = self.preferences.get_value(item, criterion)
                    if eval.value <= 1 and bool_dec:
                        return {
                            'couple_value': CoupleValue(criterion, eval),
                            'comparison': Comparison(criterion, best_crit),
                            'counter_bd': not bool_dec,
                            'item': item,
                        }
                    elif eval.value >= 2 and not bool_dec:
                        return {
                            'couple_value': CoupleValue(criterion, eval),
                            'comparison': Comparison(criterion, best_crit),
                            'counter_bd': not bool_dec,
                            'item': item,
                        }
        return None 
    
    
    def counter_argue(self, argument_message):
        """Counter an argument"""
        # TODO:
        parsed_arg = self.argument_parsing(argument_message)
        counter = self.generate_counter_argument(parsed_arg)
        
        if counter is None:
            if parsed_arg['boolean_decision']:
                item = self.find_item_from_name(parsed_arg['item_name'])
                self.accept_item(item)
            elif not self.has_proposed_best:
                self.propose_item(self.preferences.most_preferred(evaluation_needed=False))
            else:
                self.stand_by_propose()
        else:
            bool_dec = counter['counter_bd']
            item_name = counter['item']._Item__name
            cv = counter['couple_value']
            cmp = counter['comparison']
            arg_content = f'{"NOT " if not(bool_dec) else ""}{item_name}, {str(cv)}{" and " if cmp else ""}{str(cmp) if cmp else ""}'
            message = Message(self.get_name(), self.interlocutor, MessagePerformative.ARGUE, arg_content)
            self.argumentation.append({'sender': self.get_name(), 'content': arg_content})
            self.send_message(message)
            print(self.get_name(), ' - ', message._Message__message_performative, '(', arg_content, ')')
    
    def stand_by_propose(self):
        message = Message(self.get_name(), self.interlocutor, MessagePerformative.STAND_BY, 'I am in stand by.')
        self.send_message(message)
        print(self.get_name(), ' -  Stand by, waiting for answers from {}'.format(self.interlocutor))
    
    def stand_by(self):
        print(self.get_name(), ' -  Stand by, waiting for answers from {}'.format(self.interlocutor))
    
    def is_done(self):
        print(self.get_name(), ' -  Stand by, has agreed with {}'.format(self.interlocutor))
    
    def find_item_from_name(self, item_name):
        for item in self.list_items:
            if item._Item__name == item_name:
                return item
    

class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model.
    """
    def __init__(self, corpus_size=10):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.current_id = 0

        corpus = EnginesCorpus(corpus_size)
        list_items = corpus.generate_engines_list()
        
        self.agent1 = ArgumentAgent(self.next_id(), self, "agent1")
        self.agent1.generate_preferences(list_items)
        self.schedule.add(self.agent1)
        
        self.agent2 = ArgumentAgent(self.next_id(), self, "agent2")
        self.agent2.generate_preferences(list_items)
        self.schedule.add(self.agent2)
        
        self.agent1.set_interlocutor(self.agent2)
        self.agent2.set_interlocutor(self.agent1)

        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()
    


if __name__ == "__main__":
    
    sys.stdout = open(f'outputs/experiments.txt', 'a')
        
    argument_model = ArgumentModel()
    print("Agents created")
    for _ in range(10):
        argument_model.step()
    
    print('\n\n\n---------------------------------------------------------------------------------------\n\n\n\n')
    
    sys.stdout.close()

        # To be completed