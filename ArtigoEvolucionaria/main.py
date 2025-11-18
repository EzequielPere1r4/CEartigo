from MapGeneration.MapGeneration import Map
from GeneticAlgorithm.GeneticAlgorithm import GeneticAlgorithm
import matplotlib.pyplot as plt

def calculate_phenotype_variation(solutions_fenotype):
    """
    Calcula a porcentagem de variação entre os fenótipos dos cromossomos.
    
    :param solutions_fenotype: Lista de fenótipos (cada fenótipo é uma lista de vetores [G, W, T, B])
    :return: Porcentagem de variação média entre todos os pares de fenótipos
    """
    if len(solutions_fenotype) < 2:
        return 0.0
    
    def calculate_difference(fenotype1, fenotype2):
        """
        Compara dois fenótipos gene por gene (sala por sala).
        Retorna a porcentagem de genes (salas) que são diferentes.
        """
        # Determina o número de salas (usa o máximo entre os dois)
        num_salas = max(len(fenotype1), len(fenotype2))
        
        if num_salas == 0:
            return 0.0
        
        # Conta quantas salas são diferentes
        salas_diferentes = 0
        
        for i in range(num_salas):
            # Se uma sala não existir em um dos fenótipos, considera diferente
            if i >= len(fenotype1) or i >= len(fenotype2):
                salas_diferentes += 1
            else:
                # Compara os vetores [G, W, T, B] da sala (gene)
                gene1 = fenotype1[i]
                gene2 = fenotype2[i]
                
                # Se os genes forem diferentes, conta como diferente
                if gene1 != gene2:
                    salas_diferentes += 1
        
        # Retorna a porcentagem de genes diferentes
        return (salas_diferentes / num_salas) * 100
    
    # Calcula a variação entre todos os pares
    variations = []
    for i in range(len(solutions_fenotype)):
        for j in range(i + 1, len(solutions_fenotype)):
            variation = calculate_difference(solutions_fenotype[i], solutions_fenotype[j])
            variations.append(variation)
    
    # Retorna a variação média
    return sum(variations) / len(variations) if variations else 0.0

def plot_evolution_history(best_history, avg_history):
    """ Plota um gráfico da evolução do fitness. """
    plt.figure(figsize=(10, 5))
    plt.plot(best_history, label="Melhor Fitness")
    plt.plot(avg_history, label="Fitness Médio", linestyle="--")
    plt.title("Histórico de Evolução do Fitness")
    plt.xlabel("Geração")
    plt.ylabel("Fitness (Dificuldade Média)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    
    # --- 1. Geração do Mapa (Ambiente) ---
    print("Gerando layout do mapa...")
    map_instance = Map(mapWidth=50, mapHeight=50, minRoomWidth=10, minRoomHeight=10, offset=1)
    rooms, corridors = map_instance.generate_map()
    # O número de salas define o número de genes no cromossomo
    num_salas = len(rooms)
    print(f"Mapa gerado com {num_salas} salas.")

    # --- 2. Configuração do Algoritmo Genético ---
    POPULATION_SIZE = 10        # Quantos mapas de inimigos testar por geração
    GENE_COUNT = num_salas       # Número de salas (genes)
    MUTATION_RATE = 0.2        # 20% de chance de um gene (sala) sofrer mutação
    CROSSOVER_RATE = 0.8         # 80% de chance de gerar filhos (vs. clonar pais)
    ELITISM_COUNT = 2            # Os 2 melhores indivíduos passam direto para a próxima geração
    GENERATIONS = 100            # Quantas gerações rodar
    PERFECT_FITNESS = 20         # Fitness que reflete a dificuldade escolhida pelo usuário (FÁCIL = 20, MÉDIO = 40, DIFÍCIL = 60)
    TRIALS = 1000

    # --- 3. Execução do Loop de Evolução ---
    
    
    best_solutions = []

    # Roda a evolução
    #for i in range(TRIALS):
    #print(f"Executando trial {i+1} de {TRIALS}...")
    ga = GeneticAlgorithm(
        population_size=POPULATION_SIZE,
        gene_count=GENE_COUNT,
        mutation_rate=MUTATION_RATE,
        crossover_rate=CROSSOVER_RATE,
        elitism_count=ELITISM_COUNT,
        perfect_fitness=PERFECT_FITNESS
    )
    best_solution, history = ga.run_evolution(GENERATIONS)
    best_solutions.append(best_solution)

    solutions_fenotype = []
    #for best_solution in best_solutions:
    #    solutions_fenotype.append(best_solution.fenotype)

    # Calcula a porcentagem de variação entre os fenótipos
    #variation_percentage = calculate_phenotype_variation(solutions_fenotype)
    #print(f"\n--- Variação entre Fenótipos ---")
    #print(f"Porcentagem de variação média: {variation_percentage:.2f}%")
    
    #print(solutions_fenotype)

    # --- 4. Exibição dos Resultados ---
    print("\n--- Melhor Solução Encontrada ---")
    print(best_solution) # Imprime os detalhes do melhor cromossomo

    #Visualiza o mapa VAZIO (opcional)
    print("Visualizando mapa vazio...")
    map_instance.visualize_map(rooms, corridors)
    plt.show()

    #Plota o gráfico de histórico
    plot_evolution_history(history[0], history[1])

    #Visualiza o mapa FINAL com os inimigos da melhor solução
    print("Visualizando o melhor mapa gerado com inimigos...")
    map_instance.visualize_map(rooms, corridors, chromosome=best_solution)
    plt.show()