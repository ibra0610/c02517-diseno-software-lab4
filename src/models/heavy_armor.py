from src.models.armor import Armor

# Armadura pesada, reduce 50% del dano
class HeavyArmor(Armor):

    def __init__(self):
        self.defense = 10
        self.reduction_percentage = 0.50

    # Reduce el 50% del dano
    def calculate_damage_reduction(self, incoming_damage):
        reduction = int(incoming_damage * self.reduction_percentage)
        return max(0, incoming_damage - reduction)
    
    def get_defense_value(self):
        return self.defense