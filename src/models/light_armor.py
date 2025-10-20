from src.models.armor import Armor

# Reduce el 30% del dano
class LightArmor(Armor):
    
    def __init__(self):
        self.defense = 5
        self.reduction_percentage = 0.30

    # Reduce el 30% del dano
    def calculate_damage_reduction(self, incoming_damage):
        reduction = int(incoming_damage * self.reduction_percentage)
        return max(0, incoming_damage - reduction)
    
    def get_defense_value(self):
        return self.defense