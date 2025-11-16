import random
from functools import total_ordering
from math import fabs
from Models.Gene import Gene

@total_ordering
class Chromosome:
    """
    Representa o 'Cromossomo' do GAADT: um conjunto de Genes (salas).
    Garante que os AFC (Axiomas de Formação de Cromossomos) sejam cumpridos.
    """
    
    # --- Seus AFC (Regras do Cromossomo) ---
    EXACTLY_N_BEARS = 1 # Deve haver exatamente 1 Urso no mapa todo
    # --------------------------------------
    
    def __init__(self, gene_count, perfect_fitness, genes_list=None):
        """
        Cria um Cromossomo.
        :param gene_count: O número total de genes (salas) que este cromossomo deve ter.
        :param genes_list: Uma lista de Genes pré-definida (vinda do crossover/mutação).
                           Se for None, gera um novo cromossomo aleatório válido.
        """
        self.gene_count = gene_count
        if genes_list:
            self.genes = genes_list
        else:
            self.genes = self.generate_valid_chromosome()
            
        self.perfect_fitness = perfect_fitness
        self.fitness = self.calculate_fitness(perfect_fitness)
        

    @property
    def difficulty_mean(self):
        return sum(gene.difficulty for gene in self.genes) / len(self.genes) if len(self.genes) > 0 else 0

    def generate_valid_chromosome(self):
        """
        Fábrica de Cromossomos: Gera uma lista de Genes que *garantidamente*
        obedece ao AFC (exatamente 1 Urso).
        """
        genes = []
        
        # 1. Cria a(s) sala(s) do Chefe (Urso)
        for _ in range(Chromosome.EXACTLY_N_BEARS):
            bear_enemies = Gene.generate_valid_enemies(must_have_bear=True)
            genes.append(Gene(enemies_list=bear_enemies))
            
        # 2. Cria o resto das salas (sem Ursos)
        remaining_genes = self.gene_count - Chromosome.EXACTLY_N_BEARS
        for _ in range(remaining_genes):
            non_bear_enemies = Gene.generate_valid_enemies(must_have_bear=False)
            genes.append(Gene(enemies_list=non_bear_enemies))
            
        # 3. Embaralha as salas para o Urso não estar sempre na primeira
        random.shuffle(genes)
        return genes

    def calculate_fitness(self, perfect_fitness):
        """
        Função de Adaptação: Mede o quão "bom" é este Cromossomo.
        A melhor fitness é aquela que diminui a diferença entre a média da dificuldade das salas e a dificuldade perfeita.
        """
        total_difficulty = 0
        fitness = 0

        for gene in self.genes:
            total_difficulty += gene.difficulty
        if fabs((total_difficulty / len(self.genes)) - perfect_fitness) == 0:
            fitness = 10
        else:
            fitness = 1 / fabs((total_difficulty / len(self.genes)) - perfect_fitness)

        return fitness

    def __repr__(self):
        total_difficulty = 0
        for gene in self.genes:
            total_difficulty += gene.difficulty
        gene_info = "\n".join(f"  # {i+1}: {gene}" for i, gene in enumerate(self.genes))
        return f"Cromossomo(Dificuldade Média: {total_difficulty / len(self.genes):.2f}, Fitness: {self.fitness:.2f}, Genes: {len(self.genes)})\n{gene_info}"
    
    def __lt__(self, other):
        """ Permite ordenar cromossomos por fitness. """
        if not isinstance(other, Chromosome):
            return NotImplemented
        return self.fitness < other.fitness
    
    def __eq__(self, other):
        """ Compara dois cromossomos por fitness. """
        if not isinstance(other, Chromosome):
            return NotImplemented
        return self.fitness == other.fitness