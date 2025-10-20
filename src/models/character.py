class Character:
    def __init__(self, name, health=100, armor = None):
        self.name = name
        self.health = health
        self.is_alive = True
        # Agrego la armadura
        self.armor = armor
    
    def take_damage(self, damage):
        # Cambios implementando la armadura
        initial_damage = damage

        if self.armor:
            initial_damage = self.armor.calculate_damage_reduction(damage)
        
        self.health -= initial_damage

        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        
        return initial_damage
    
    def heal(self, amount):
        if self.is_alive:
            self.health += amount

    # Equipa la armadura
    def equip_armor(self, armor):
        self.armor = armor

    def get_total_defense(self):
        if self.armor:
            return self.armor.get_defense_value()
        return 0