from arguments.Argument import Argument
from pw_argumentation import ArgumentAgent, ArgumentModel
from communication.preferences.EnginesCorpus import EnginesCorpus


if __name__ == '__main__':
    model = ArgumentModel()
    agent = ArgumentAgent(1, model, "Agent1")
    engines_corpus = EnginesCorpus(10)
    engines_list = engines_corpus.generate_engines_list()
    agent.generate_preferences(engines_list)
    arg = Argument(True, engines_list[0]._Item__name)
    arg.List_supporting_proposal(arg.item_name, agent.preferences)
    print([str(premiss) for premiss in arg.comparison_list])
    print([str(premiss) for premiss in arg.couple_values_list])