import random
import copy
from itertools import combinations
from statistics import mean
from Models.Population import Population
from Models.Chromosome import Chromosome
from Models.Gene import Gene
from Models.Base import Base

class GeneticAlgorithm:
    """
    Orquestra o processo de evolução (Seleção, Crossover, Mutação)
    para otimizar a população.
    """
    def __init__(self, population_size, gene_count, mutation_rate, crossover_rate, elitism_count, perfect_fitness):
        self.population_size = population_size
        self.gene_count = gene_count
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        self.perfect_fitness = perfect_fitness

        # Inicializa a primeira população
        self.population = Population(self.population_size, self.gene_count, self.perfect_fitness)


    def dominant_gene_comparator(self, gene1, gene2):
        """
        Função de Dominância (GAADT): Compara dois genes (salas) e
        retorna o "dominante" (o melhor).
        
        Neste caso, o "dominante" é o que tiver MAIOR DIFICULDADE (grau).
        """
        if gene1.bear_count != gene2.bear_count:
            return Gene(enemies_list=[Base('_')])
        else:
            return gene1 if gene1.difficulty >= gene2.difficulty else gene2



    def crossover(self, parent1, parent2):
        # Realizar a seleção dos melhores cromossomos
        child_population = self.fertilization(parent1, parent2)

        for child in child_population:
            if child.fitness > parent1.fitness or child.fitness > parent2.fitness:
                self.population.chromosomes.append(child)


    def fertilization(self, parent1, parent2):
        """
        Operador de Fertilização (GAADT):
        Cria um novo filho a partir de dois pais, garantindo que o AFC seja mantido.
        """
        child_genes = set()
        descendants = []

        for gene in parent1.genes:
            for gene2 in parent2.genes:
                dominant_gene = self.dominant_gene_comparator(gene, gene2)
                # Filtra genes inválidos (genes com Base('_') ou que não atendem aos AFG)
                if dominant_gene.bear_count >= 0 and len(dominant_gene.enemies) >= Gene.MIN_ENEMIES:
                    # Verifica se o gene atende aos AFG
                    if Gene._validate_gene_static(dominant_gene.enemies):
                        child_genes.add(dominant_gene)
        # Converte o set para lista para poder trabalhar com índices
        child_genes_list = list(child_genes)
        
        # Separa genes com urso dos genes sem urso
        bear_genes = [g for g in child_genes_list if g.bear_count == 1]
        non_bear_genes = [g for g in child_genes_list if g.bear_count == 0]

        # Gera todas as combinações válidas de cromossomos
        # Cada cromossomo deve ter exatamente 1 gene com urso e (gene_count - 1) genes sem urso
        remaining_slots = self.gene_count - 1  # Quantos slots restam após colocar o urso
        
        for bear_gene in bear_genes:
            # Para cada gene com urso, gera todas as combinações possíveis dos outros genes
            if len(non_bear_genes) >= remaining_slots:
                for combo in combinations(non_bear_genes, remaining_slots):
                    # Cria um cromossomo com: 1 urso + (gene_count - 1) genes sem urso
                    genes_list = [bear_gene] + list(combo)
                    # Embaralha para não ter o urso sempre na primeira posição
                    random.shuffle(genes_list)
                    descendants.append(Chromosome(self.gene_count, self.perfect_fitness, genes_list=genes_list))
        
        return descendants
        

    def selection(self, subpopulation_size = 2, mutation = False):
        """
        Seleção por Torneio: Escolhe N indivíduos aleatórios e 
        retorna o melhor deles (o vencedor do torneio).
        """
        if mutation:
            # Retorna os últimos N elementos da população (os piores)
            return copy.deepcopy(self.population.chromosomes[-subpopulation_size:])
        else:
            # Retorna os primeiros N elementos da população (os melhores)
            return copy.deepcopy(self.population.chromosomes[:subpopulation_size])


    def mutation(self, chromosome):
        """
        Operador de Mutação (GAADT-Adaptado):
        Altera aleatoriamente um gene, garantindo que o AFC não seja violado.
        """
        new_genes = []
        for i, gene in enumerate(chromosome.genes):
            if random.random() < self.mutation_rate:
                if gene.bear_count > 0:
                    new_genes.append(Gene(enemies_list=Gene.generate_valid_enemies(must_have_bear=True)))
                else:
                    new_genes.append(Gene(enemies_list=Gene.generate_valid_enemies(must_have_bear=False)))
            else:
                new_genes.append(gene)
        
        new_chromosome = Chromosome(self.gene_count, self.perfect_fitness, genes_list=new_genes)

        if new_chromosome.fitness > chromosome.fitness:
            self.population.chromosomes.append(new_chromosome)


    def evolve(self):
        crossover_population = []
        mutation_population = []

        self.population.chromosomes = sorted(self.population.chromosomes, reverse=True)
        subpopulation_size = self.population_size // 10 if (self.population_size // 10) % 2 == 0 else self.population_size // 10 + 1
        #subpopulation_size = 10

        mutation_population = self.selection(subpopulation_size, mutation = True)
        
        crossover_population = self.selection(subpopulation_size)
        male_crossover_population = crossover_population[:len(crossover_population)//2]
        female_crossover_population = crossover_population[len(crossover_population)//2:]

        for i in range(len(male_crossover_population)):
            if random.random() < self.crossover_rate:
                self.crossover(male_crossover_population[i], female_crossover_population[i])
        
        for chromosome in mutation_population:
            if random.random() < self.mutation_rate:
                self.mutation(chromosome)
            


    def run_evolution(self, generations):
        """ Roda o loop de evolução por N gerações. """
        print(f"--- Iniciando Evolução ---")
        print(f"População: {self.population_size} | Salas: {self.gene_count}")
        print(f"Mutação: {self.mutation_rate*100}% | Crossover: {self.crossover_rate*100}% | Elitismo: {self.elitism_count}")
        print("-" * 30)
        
        best_fitness_history = []
        avg_fitness_history = []
        
        initial_best = self.population.get_best_chromosome()
        print(f"Geração 0: pop_size: {self.population.population_size}: Dificuldade Média = {initial_best.difficulty_mean:.2f} | Melhor Fitness = {initial_best.fitness:.2f}")
        gen = 0

        while self.population.get_best_chromosome().fitness < 1 and gen < generations:
        
            # Roda uma geração
            self.evolve()

            # Coleta estatísticas
            best_chromosome = self.population.get_best_chromosome()
            avg_fitness = mean(c.fitness for c in self.population.chromosomes)
            
            best_fitness_history.append(best_chromosome.fitness)
            avg_fitness_history.append(avg_fitness)
            
            if gen % 10 == 0 or gen == generations or gen < 10 or best_chromosome.fitness == 1:
                print(f"Geração {gen + 1} pop_size: {self.population.population_size}: Dificuldade Média = {best_chromosome.difficulty_mean:.2f} | Melhor Fitness = {best_chromosome.fitness:.2f} | Média Fitness = {avg_fitness:.2f}")
            gen += 1
               
        
        # for g in range(1, generations + 1):
        #     # Roda uma geração
        #     self.evolve()
            
        #     # Coleta estatísticas
        #     best_chromosome = self.population.get_best_chromosome()
        #     avg_fitness = mean(c.fitness for c in self.population.chromosomes)
            
        #     best_fitness_history.append(best_chromosome.fitness)
        #     avg_fitness_history.append(avg_fitness)
        #     if g % 10 == 0 or g == generations or g < 10:
        #         print(f"Geração {g} pop_size: {self.population.population_size}: Dificuldade Média = {best_chromosome.difficulty_mean:.2f} | Melhor Fitness = {best_chromosome.fitness:.2f} | Média Fitness = {avg_fitness:.2f}")
        print("--- Evolução Concluída ---")
        
        # Retorna o melhor indivíduo encontrado e o histórico
        final_best = self.population.get_best_chromosome()
        return final_best, (best_fitness_history, avg_fitness_history)