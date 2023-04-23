import sys


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
from pw_argumentation import ArgumentAgent, ArgumentModel



def evaluation_metric(agent1_prefs, agent2_prefs, agreed_item):
    # Calculates a metric for a dialogue between two agents based on their preferences and the agreed-upon item.
    # Find the rank of the agreed item in each agent's preferences
    agent1_rank = agent1_prefs._Preferences__item_ordered_list.index(agreed_item)
    agent2_rank = agent2_prefs._Preferences__item_ordered_list.index(agreed_item)
    # Calculate a score for the agreed item for each agent
    agent1_score = 1.0 / (agent1_rank + 1)
    agent2_score = 1.0 / (agent2_rank + 1)
    total_score = agent1_score + agent2_score
    return total_score




if __name__ == "__main__":
    
    n = 50
    
    sys.stdout = open(f'outputs/experiments_{n}_items.txt', 'a')
    
    argument_model = ArgumentModel(corpus_size=n)
    print("Agents created")
    for _ in range(10):
        argument_model.step()
    
    agreed_item = argument_model.agent1.agreed_item
    if argument_model.agent2.agreed_item and agreed_item:
        
        print(agreed_item)
        
        score = evaluation_metric(
            argument_model.agent1.preferences,
            argument_model.agent2.preferences,
            agreed_item,
        )
    else:
        score = 0
    print('\nscore = ', score)
    
    
    print('\n\n\n---------------------------------------------------------------------------------------\n\n\n\n')
    
    sys.stdout.close()
    
    sys.stdout = open(f'outputs/experiments_{n}_items_scores.txt', 'a')
    
    print('score = ', score)
    
    sys.stdout.close()