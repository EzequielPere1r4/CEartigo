import random

class Base:
    """ Representa a 'Base' do GAADT: um único inimigo. """
    def __init__(self, letter=None):
        self.letter = self.generate_base() if letter is None else letter
        self.difficulty = self.get_difficulty()

    def generate_base(self):
        """ Probabilidades de geração de cada inimigo """
        random_number = random.random() # 0.0 a 1.0
        if random_number < 0.50: # 50% G
            return 'G'
        elif random_number < 0.80: # 30% W
            return 'W'
        elif random_number < 0.95: # 15% T
            return 'T'
        else: # 5% B
            return 'B'

    def get_difficulty(self):
        if self.letter == 'G': return 2
        elif self.letter == 'W': return 5
        elif self.letter == 'T': return 10
        elif self.letter == 'B': return 35
        elif self.letter == '_': return 0
        else: return 0

    def __str__(self):
        return self.letter
    
    def __repr__(self):
        return self.letter