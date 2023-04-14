from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.EnginesCorpus import EnginesCorpus
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative


class ArgumentAgent(CommunicatingAgent):
    """ ArgumentAgent which inherit from CommunicatingAgent.
    """
    def __init__ (self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.preferences = None
        self.list_items = None
        self.interlocutor = None
        self.proposition_made = False
        self.has_committed = False
        self.return_commit_received = False
        
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
                self.argue_item()
        elif not self.proposition_made:
            proposed_item = self.preferences.most_preferred()
            self.propose_item(proposed_item)
        elif self.has_committed and self.return_commit_received:
            self.is_done()
        else:
            self.stand_by()

    def get_preference(self):
        return self.preference

    def generate_preferences(self, List_items):
        self.list_items = List_items
        self.preferences = Preferences(List_items)
    
    def set_interlocutor(self, other_agent):
        self.interlocutor = other_agent.get_name()
    
    def propose_item(self, item):
        message = Message(self.get_name(), self.interlocutor, MessagePerformative.PROPOSE, item._Item__name)
        self.send_message(message)
        self.proposition_made = True
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
        print(self.get_name(), ' - ', message._Message__message_performative, '(', item._Item__name, ')')
    
    def argue_item(self):
        message = Message(self.get_name(), self.interlocutor, MessagePerformative.ARGUE, 'Empty content')
        self.send_message(message)
        print(self.get_name(), ' - ', message._Message__message_performative, '(', 'Empty content', ')')
    
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
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.current_id = 0

        # To be completed
        corpus = EnginesCorpus(10)
        list_items = corpus.generate_engines_list()
        
        agent1 = ArgumentAgent(self.next_id(), self, "agent1")
        agent1.generate_preferences(list_items)
        self.schedule.add(agent1)
        
        agent2 = ArgumentAgent(self.next_id(), self, "agent2")
        agent2.generate_preferences(list_items)
        self.schedule.add(agent2)
        
        agent1.set_interlocutor(agent2)
        agent2.set_interlocutor(agent1)

        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()
    


if __name__ == "__main__":
    
    argument_model = ArgumentModel()
    print("Agents created")
    for _ in range(5):
        argument_model.step()

    # To be completed