from Models.Chromosome import Chromosome

class Population:
    """ Representa a População: um conjunto de Cromossomos. """
    def __init__(self, population_size, gene_count, perfect_fitness):
        self._initial_population_size = population_size  # Tamanho inicial/target
        self.gene_count = gene_count # Número de salas
        self.perfect_fitness = perfect_fitness
        self.chromosomes = self.generate_population()

    @property
    def population_size(self):
        """ Retorna o tamanho atual da população (dinâmico). """
        return len(self.chromosomes)

    def generate_population(self):
        """ Gera a população inicial de N cromossomos aleatórios e válidos. """
        return [Chromosome(self.gene_count, self.perfect_fitness) for _ in range(self._initial_population_size)]

    def get_best_chromosome(self):
        """ Encontra o melhor indivíduo da população atual. """
        return max(self.chromosomes)