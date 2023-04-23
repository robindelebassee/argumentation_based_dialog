from communication.preferences.EnginesCorpus import EnginesCorpus
from communication.preferences.Preferences import Preferences
from communication.preferences.CriterionName import CriterionName


if __name__ == '__main__':
    """Testing the Preferences class.
    """
    
    engines = EnginesCorpus(10)
    engines_list = engines.electrics + engines.diesels
    
    agent_pref = Preferences(engines_list)
    
    diesel_engine = engines.diesels[0]
    electric_engine = engines.electrics[0]
    
    """test list of preferences"""
    print(diesel_engine)
    print(electric_engine)
    print('Production cost value for diesel engine is : ', diesel_engine.get_value(agent_pref, CriterionName.PRODUCTION_COST))
    print('The agent prefer the criterion CONSUMPTION over NOISE : ', agent_pref.is_preferred_criterion(CriterionName.CONSUMPTION, CriterionName.NOISE))
    print('Electric Engine > Diesel Engine : {}'.format(agent_pref.is_preferred_item(electric_engine, diesel_engine)))
    print('Diesel Engine > Electric Engine : {}'.format(agent_pref.is_preferred_item(diesel_engine, electric_engine)))
    print('Electric Engine (for agent 1) = {}'.format(electric_engine.get_score(agent_pref)))
    print('Diesel Engine (for agent 1) = {}'.format(diesel_engine.get_score(agent_pref)))
    print('Most preferred item is : {}'.format(agent_pref.most_preferred(engines_list, evaluation_needed=True).get_name()))
    print('Is eletric engine among 10 % preferred items: {}'.format(agent_pref.is_item_among_top_10_percent(electric_engine, item_list=engines_list, evaluation_needed=False)))
    print([item._Item__name for item in agent_pref._Preferences__item_ordered_list])
    pref_dict = agent_pref.print_preferences_dict(engines_list)
    for k,v in pref_dict.items():
        print(k, ':', v)
