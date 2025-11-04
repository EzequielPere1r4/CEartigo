import random
from Models.Gene import Gene

class Chromosome:
    """
    Representa o 'Cromossomo' do GAADT: um conjunto de Genes (salas).
    Garante que os AFC (Axiomas de Formação de Cromossomos) sejam cumpridos.
    """
    
    # --- Seus AFC (Regras do Cromossomo) ---
    EXACTLY_N_BEARS = 1 # Deve haver exatamente 1 Urso no mapa todo
    # --------------------------------------
    
    def __init__(self, gene_count, genes_list=None):
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
            
        self.fitness = self.calculate_fitness()

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

    def calculate_fitness(self):
        """
        Função de Adaptação: Mede o quão "bom" é este Cromossomo.
        (Média da dificuldade das salas SEM o Urso)
        """
        total_difficulty = 0
        non_bear_gene_count = 0
        
        for gene in self.genes:
            if gene.bear_count == 0:
                total_difficulty += gene.difficulty
                non_bear_gene_count += 1
                
        if non_bear_gene_count == 0:
            return 0 # Evita divisão por zero
            
        # O objetivo é maximizar a dificuldade média das salas normais
        return total_difficulty / non_bear_gene_count

    def __repr__(self):
        gene_info = "\n".join(f"  # {i+1}: {gene}" for i, gene in enumerate(self.genes))
        return f"Cromossomo(Fitness: {self.fitness:.2f}, Genes: {len(self.genes)})\n{gene_info}"
    
    def __lt__(self, other):
        """ Permite ordenar cromossomos por fitness. """
        return self.fitness < other.fitness