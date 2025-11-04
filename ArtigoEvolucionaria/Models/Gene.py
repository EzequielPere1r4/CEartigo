import random
from Models.Base import Base

class Gene:
    """ 
    Representa o 'Gene' do GAADT: um conjunto de Bases (inimigos) em uma sala.
    Garante que os AFG (Axiomas de Formação de Genes) sejam cumpridos.
    """
    
    # --- Seus AFG (Regras do Gene) ---
    MIN_DIFFICULTY = 3
    MAX_DIFFICULTY = 60
    MIN_ENEMIES = 3
    MAX_BEARS = 1
    MAX_GOBLINS = 8
    MAX_WOLVES = 6
    # ---------------------------------
    
    def __init__(self, enemies_list=None):
        """ Cria um Gene. Se enemies_list não for fornecido, gera um novo Gene válido. """
        if enemies_list is None:
            self.enemies = Gene.generate_valid_enemies()
        else:
            self.enemies = enemies_list

    # --- Propriedades (Getters) para fácil acesso ---
    @property
    def enemy_letters(self):
        return [enemy.letter for enemy in self.enemies]
    
    @property
    def difficulty(self):
        return sum(enemy.difficulty for enemy in self.enemies)
    
    @property
    def bear_count(self):
        return self.enemy_letters.count('B')

    # --- Métodos Estáticos (Fábricas) para gerar Genes Válidos ---
    
    @staticmethod
    def _generate_random_enemies():
        """ Gera uma lista aleatória de inimigos, sem garantia de validade. """
        num_enemies = random.randint(Gene.MIN_ENEMIES, Gene.MAX_GOBLINS + 1) # Ex: 3 a 9 inimigos
        return [Base() for _ in range(num_enemies)]

    @staticmethod
    def _validate_gene_static(enemies):
        """ 
        Verificador de AFG: Checa se uma lista de inimigos obedece a *todas* as regras.
        """
        if len(enemies) < Gene.MIN_ENEMIES:
            return False
        
        enemy_letters = [enemy.letter for enemy in enemies]
        if enemy_letters.count('B') > Gene.MAX_BEARS:
            return False
        if enemy_letters.count('G') > Gene.MAX_GOBLINS:
            return False
        if enemy_letters.count('W') > Gene.MAX_WOLVES:
            return False
        
        difficulty = sum(enemy.difficulty for enemy in enemies)
        if not (Gene.MIN_DIFFICULTY <= difficulty <= Gene.MAX_DIFFICULTY):
            return False
            
        return True

    @staticmethod
    def generate_valid_enemies(must_have_bear=None):
        """
        Fábrica de Genes: Gera inimigos *até* encontrar uma combinação válida 
        que satisfaça os AFG e a restrição 'must_have_bear'.
        """
        attempts = 0
        while attempts < 1000: # Proteção contra loop infinito
            enemies = Gene._generate_random_enemies()
            
            if not Gene._validate_gene_static(enemies):
                continue
                
            bear_count = [e.letter for e in enemies].count('B')
            
            if must_have_bear is True and bear_count == 1:
                return enemies # Válido E tem o Urso
            elif must_have_bear is False and bear_count == 0:
                return enemies # Válido E NÃO tem o Urso
            elif must_have_bear is None and bear_count <= Gene.MAX_BEARS:
                return enemies # Válido, não importa o urso
            
            attempts += 1
        
        raise Exception("Não foi possível gerar um Gene válido. Verifique as regras (AFG).")

    def __repr__(self):
        return f"Gene({''.join(self.enemy_letters)}, Dific:{self.difficulty})"