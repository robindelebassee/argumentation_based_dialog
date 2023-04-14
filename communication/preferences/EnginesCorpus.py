from communication.preferences.DieselEngine import DieselEngine
from communication.preferences.ElectricEngine import ElectricEngine


class EnginesCorpus:
    """Create a corpus of engines that will be reviewed by the different agents in the argumentation.
    
    The corpus size will be a multiple of 10 to easily check the 10 best percent engines for a reviewer.
    """
    
    def __init__(self, corpus_size):
        """Instantiate the engines corpus.

        Args:
            corpus_size (int): integer indicating the size of the corpus. It should be a multiple of 10.
        """
        
        # Input validation to check argument is a multiple of 10.
        if corpus_size // 10 != 0: 
            _corpus_size = corpus_size // 10 * 10
        else: 
            _corpus_size = corpus_size
        
        nb_iter = _corpus_size // 2
        pad_size = 1 / (nb_iter - 1)
        unique_id = 1
        
        electrics = []
        diesels = []
        
        for iter in range(nb_iter):
            
            quality_factor = pad_size * iter # quality_factor between 0 and 1 to define the engines
            name1 = 'Electric Engine {}'.format(unique_id)
            name2 = 'Diesel Engine {}'.format(unique_id)
            electric = ElectricEngine(name1, quality_factor)
            electrics.append(electric)
            diesel = DieselEngine(name2, quality_factor)
            diesels.append(diesel)
            unique_id += 1
        
        self.electrics = electrics
        self.diesels = diesels
    
    def generate_engines_list(self):
        return self.electrics + self.diesels
