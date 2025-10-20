import unittest
from unittest.mock import MagicMock
from src.models.character import Character
from src.models.armor import Armor

class DummyArmor(Armor):
    """Armadura dummy para testing"""
    def __init__(self, defense_value = 0, reduction = 0):
        self.defense_value = defense_value
        self.reduction = reduction

    def calculate_damage_reduction(self, incoming_damage):
        return max(0, incoming_damage - self.reduction)
    
    def get_defense_value(self):
        return self.defense_value
    
class TestArmorDependencyInjection(unittest.TestCase):

    def test_character_accepts_any_armor_implementation(self):
        """Test que Character acepta cualquier implementacion de Armor"""
        dummy_armor = DummyArmor(defense_value=15, reduction=25)
        hero = Character("Hero", armor=dummy_armor)

        self.assertEqual(hero.get_total_defense(), 15)
        damage_taken = hero.take_damage(50)
        self.assertEqual(damage_taken, 25)

    def test_mock_armor_with_specific_behavior(self):
        """Test usando MagicMock para simular comportamiento de armadura"""
        mock_armor = MagicMock(spec=Armor)
        mock_armor.calculate_damage_reduction.return_value = 5
        mock_armor.get_defense_value.return_value = 20
        
        hero = Character("Hero")
        hero.equip_armor(mock_armor)
        
        self.assertEqual(hero.get_total_defense(), 20)
        damage_taken = hero.take_damage(100)
        
        # Verificamos que se llamó al método correcto
        mock_armor.calculate_damage_reduction.assert_called_once_with(100)
        self.assertEqual(damage_taken, 5)

    def test_armor_can_be_changed_dynamically(self):
        """Test que se puede cambiar armadura dinámicamente"""
        light_armor = DummyArmor(defense_value=5, reduction=10)
        heavy_armor = DummyArmor(defense_value=20, reduction=30)
        
        warrior = Character("Warrior", armor=light_armor)
        self.assertEqual(warrior.get_total_defense(), 5)
        
        warrior.equip_armor(heavy_armor)
        self.assertEqual(warrior.get_total_defense(), 20)
        
        damage_taken = warrior.take_damage(50)
        self.assertEqual(damage_taken, 20)  # 50 - 30

    def test_multiple_characters_different_armors(self):
        """Test que múltiples personajes pueden tener diferentes armaduras"""
        armor1 = DummyArmor(defense_value=10, reduction=15)
        armor2 = DummyArmor(defense_value=25, reduction=40)
        
        hero1 = Character("Hero1", armor=armor1)
        hero2 = Character("Hero2", armor=armor2)
        
        hero1.take_damage(50)
        hero2.take_damage(50)
        
        # Hero1: 50 - 15 = 35 damage
        # Hero2: 50 - 40 = 10 damage
        self.assertEqual(hero1.health, 65)
        self.assertEqual(hero2.health, 90)