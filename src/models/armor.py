from abc import ABC, abstractmethod

# Clase abstracta para armaduras
class Armor(ABC):

    # Calcula el dano reducido por la armadura
    @abstractmethod
    def calculate_damage_reduction(self, incoming_damage):
        pass
    
    # Retorna el valor de defensa de la armadura
    @abstractmethod
    def get_defense_value(self):
        pass
