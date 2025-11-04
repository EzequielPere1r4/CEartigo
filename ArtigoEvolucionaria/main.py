from MapGeneration.MapGeneration import Map
from GeneticAlgorithm.GeneticAlgorithm import GeneticAlgorithm
import matplotlib.pyplot as plt

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
    map_instance = Map(mapWidth=40, mapHeight=40, minRoomWidth=6, minRoomHeight=6, offset=1)
    rooms, corridors = map_instance.generate_map()
    
    # O número de salas define o número de genes no cromossomo
    num_salas = len(rooms)
    print(f"Mapa gerado com {num_salas} salas.")
    
    # Visualiza o mapa VAZIO (opcional)
    # print("Visualizando mapa vazio...")
    # map_instance.visualize_map(rooms, corridors)
    # plt.show()


    # --- 2. Configuração do Algoritmo Genético ---
    POPULATION_SIZE = 100        # Quantos mapas de inimigos testar por geração
    GENE_COUNT = num_salas       # Número de salas (genes)
    MUTATION_RATE = 0.10        # 5% de chance de um gene (sala) sofrer mutação
    CROSSOVER_RATE = 0.8         # 80% de chance de gerar filhos (vs. clonar pais)
    ELITISM_COUNT = 2            # Os 2 melhores indivíduos passam direto para a próxima geração
    GENERATIONS = 100            # Quantas gerações rodar

    # --- 3. Execução do Loop de Evolução ---
    ga = GeneticAlgorithm(
        population_size=POPULATION_SIZE,
        gene_count=GENE_COUNT,
        mutation_rate=MUTATION_RATE,
        crossover_rate=CROSSOVER_RATE,
        elitism_count=ELITISM_COUNT
    )
    
    # Roda a evolução
    best_solution, history = ga.run_evolution(GENERATIONS)

    # --- 4. Exibição dos Resultados ---
    print("\n--- Melhor Solução Encontrada ---")
    print(best_solution) # Imprime os detalhes do melhor cromossomo
    
    # Plota o gráfico de histórico
    plot_evolution_history(history[0], history[1])
    
    # Visualiza o mapa FINAL com os inimigos da melhor solução
    print("Visualizando o melhor mapa gerado com inimigos...")
    map_instance.visualize_map(rooms, corridors, chromosome=best_solution)
    plt.show()