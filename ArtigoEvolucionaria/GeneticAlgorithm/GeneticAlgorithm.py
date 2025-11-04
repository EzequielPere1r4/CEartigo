import random
import copy
from statistics import mean
from Models.Population import Population
from Models.Chromosome import Chromosome
from Models.Gene import Gene

class GeneticAlgorithm:
    """
    Orquestra o processo de evolução (Seleção, Crossover, Mutação)
    para otimizar a população.
    """
    def __init__(self, population_size, gene_count, mutation_rate, crossover_rate, elitism_count):
        self.population_size = population_size
        self.gene_count = gene_count
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        
        # Inicializa a primeira população
        self.population = Population(self.population_size, self.gene_count)

    def dominant_gene_comparator(self, gene1, gene2):
        """
        Função de Dominância (GAADT): Compara dois genes (salas) e
        retorna o "dominante" (o melhor).
        
        Neste caso, o "dominante" é o que tiver MAIOR DIFICULDADE (grau).
        """
    # Agora o dominante é o de MENOR dificuldade
        return gene1 if gene1.difficulty <= gene2.difficulty else gene2

        #return gene1 if gene1.difficulty >= gene2.difficulty else gene2

    def selection(self, tournament_size=3):
        """
        Seleção por Torneio: Escolhe N indivíduos aleatórios e 
        retorna o melhor deles (o vencedor do torneio).
        """
        tournament = random.sample(self.population.chromosomes, tournament_size)
        return max(tournament) # Retorna o cromossomo com maior fitness

    def crossover(self, parent1, parent2):
        """
        Operador de Crossover (GAADT-Adaptado):
        Cria um novo filho a partir de dois pais, garantindo que o AFC seja mantido.
        """
        
        # 1. Preparar a lista de genes do filho
        child_genes = [None] * self.gene_count
        
        # 2. TRATAR O AFC (O Urso) PRIMEIRO:
        # Encontra o gene do Urso em cada pai
        geneA_bear = next((g for g in parent1.genes if g.bear_count == 1), None)
        geneB_bear = next((g for g in parent2.genes if g.bear_count == 1), None)
        
        # Validação: Se um pai não tiver urso, algo está errado (AFC quebrado)
        if not geneA_bear or not geneB_bear:
             raise Exception("Erro de Crossover: Pelo menos um pai quebrou o AFC (sem Urso).")

        indexA_bear = parent1.genes.index(geneA_bear)
        indexB_bear = parent2.genes.index(geneB_bear)
        
        # Aplica a "dominância" para escolher o gene do Urso do filho
        dominant_bear_gene = self.dominant_gene_comparator(geneA_bear, geneB_bear)
        
        # O filho herda o gene do Urso em uma das posições dos pais
        child_bear_index = random.choice([indexA_bear, indexB_bear])
        child_genes[child_bear_index] = dominant_bear_gene
        
        # 3. TRATAR OS OUTROS GENES (Dominância GAADT):
        for i in range(self.gene_count):
            if i == child_bear_index:
                continue # Pula a posição que já preenchemos
                
            geneA = parent1.genes[i]
            geneB = parent2.genes[i]
            
            # Precisamos garantir que estamos comparando dois genes NÃO-URSO.
            if geneA.bear_count > 0: 
                geneA = Gene(enemies_list=Gene.generate_valid_enemies(must_have_bear=False))
            
            if geneB.bear_count > 0: 
                geneB = Gene(enemies_list=Gene.generate_valid_enemies(must_have_bear=False))
                
            # Agora temos certeza que geneA e geneB são não-ursos.
            # Aplicamos a dominância GAADT.
            dominant_gene = self.dominant_gene_comparator(geneA, geneB)
            child_genes[i] = dominant_gene
            
        # 4. Retorna um novo cromossomo com a lista de genes criada
        return Chromosome(self.gene_count, genes_list=child_genes)

    def mutation(self, chromosome):
        """
        Operador de Mutação (GAADT-Adaptado):
        Altera aleatoriamente um gene, garantindo que o AFC não seja violado.
        """
        for i in range(self.gene_count):
            if random.random() < self.mutation_rate:
                # Este gene sofrerá mutação!
                
                is_bear_gene = chromosome.genes[i].bear_count > 0
                
                if is_bear_gene:
                    # Se era um gene de Urso, substitui por um NOVO gene de Urso
                    new_enemies = Gene.generate_valid_enemies(must_have_bear=True)
                    chromosome.genes[i] = Gene(enemies_list=new_enemies)
                else:
                    # Se era um gene normal, substitui por um NOVO gene normal
                    new_enemies = Gene.generate_valid_enemies(must_have_bear=False)
                    chromosome.genes[i] = Gene(enemies_list=new_enemies)
        
        # Recalcula o fitness após a mutação
        chromosome.fitness = chromosome.calculate_fitness()
        return chromosome

    def evolve(self):
        """
        Executa uma geração do algoritmo:
        1. Seleciona os melhores (Elitismo)
        2. Cria novos filhos (Seleção + Crossover)
        3. Aplica mutações
        4. Substitui a população antiga pela nova
        """
        new_population = []
        
        # 1. Elitismo: Os melhores X indivíduos passam direto
        sorted_population = sorted(self.population.chromosomes, reverse=True) # Ordena do melhor para o pior
        for i in range(self.elitism_count):
            new_population.append(copy.deepcopy(sorted_population[i]))
            
        # 2. Preenche o resto da população com novos filhos
        while len(new_population) < self.population_size:
            
            # 3. Seleção
            parent1 = self.selection()
            parent2 = self.selection()
            
            # 4. Crossover
            if random.random() < self.crossover_rate:
                child = self.crossover(parent1, parent2)
            else:
                # Se não houver crossover, um dos pais é clonado
                child = copy.deepcopy(parent1)
            
            # 5. Mutação
            child = self.mutation(child)
            
            new_population.append(child)
            
        # 6. Substitui a população antiga
        self.population.chromosomes = new_population

    def run_evolution(self, generations):
        """ Roda o loop de evolução por N gerações. """
        print(f"--- Iniciando Evolução ---")
        print(f"População: {self.population_size} | Salas: {self.gene_count}")
        print(f"Mutação: {self.mutation_rate*100}% | Crossover: {self.crossover_rate*100}% | Elitismo: {self.elitism_count}")
        print("-" * 30)
        
        best_fitness_history = []
        avg_fitness_history = []
        
        initial_best = self.population.get_best_chromosome()
        print(f"Geração 0: Melhor Fitness = {initial_best.fitness:.2f}")
        
        for g in range(1, generations + 1):
            # Roda uma geração
            self.evolve()
            
            # Coleta estatísticas
            best_chromosome = self.population.get_best_chromosome()
            avg_fitness = mean(c.fitness for c in self.population.chromosomes)
            
            best_fitness_history.append(best_chromosome.fitness)
            avg_fitness_history.append(avg_fitness)
            
            if g % 10 == 0 or g == generations:
                print(f"Geração {g}: Melhor Fitness = {best_chromosome.fitness:.2f} | Média Fitness = {avg_fitness:.2f}")
                
        print("--- Evolução Concluída ---")
        
        # Retorna o melhor indivíduo encontrado e o histórico
        final_best = self.population.get_best_chromosome()
        return final_best, (best_fitness_history, avg_fitness_history)