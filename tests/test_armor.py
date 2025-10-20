import unittest
from unittest.mock import MagicMock
from src.models.character import Character
from src.models.light_armor import LightArmor
from src.models.heavy_armor import HeavyArmor
from src.models.sword import Sword
from src.models.bow import Bow
from src.app.combat_system import CombatSystem

class TestArmorSystem(unittest.TestCase):

    def test_light_armor_reduces_damage_30_percent(self):
        """Test para que la armadura ligera reduzca 30% del daño"""
        armor = LightArmor()
        reduce_damage = armor.calculate_damage_reduction(100)
        self.assertEqual(reduce_damage, 70)

    def test_heavy_armor_reduces_damage_50_percent(self):
        """Test para que la armadura pesada reduzca 50% del daño"""
        armor = HeavyArmor()
        reduce_damage = armor.calculate_damage_reduction(100)
        self.assertEqual(reduce_damage, 50)

    def test_character_without_armor_takes_full_damage(self):
        """Test para que un personaje sin armadura reciba dano completo"""
        hero = Character("Hero")
        initial_health = hero.health
        damage_taken = hero.take_damage(20)

        self.assertEqual(damage_taken, 20)
        self.assertEqual(hero.health, initial_health - 20)

    def test_character_with_light_armor_takes_reduced_damage(self):
        """Test para que un personaje con armadura ligera reciba menos dano"""
        hero = Character("Hero", armor=LightArmor())
        initial_health= hero.health
        damage_taken = hero.take_damage(30)

        self.assertEqual(damage_taken, 21)
        self.assertEqual(hero.health, initial_health - 21)

    def test_character_with_heavy_armor_takes_reduced_damage(self):
        """Test para que un personaje con armadura pesada reciba menos dano"""
        tank = Character("Tank", armor=HeavyArmor())
        initial_health= tank.health
        damage_taken = tank.take_damage(40)

        self.assertEqual(damage_taken, 20)
        self.assertEqual(tank.health, initial_health - 20)

    def test_equip_armor_after_creation(self):
        """Test que se puede equipar armadura después de crear el personaje"""
        hero = Character("Hero")
        self.assertEqual(hero.get_total_defense(), 0)
        
        hero.equip_armor(HeavyArmor())
        self.assertEqual(hero.get_total_defense(), 10)

    def test_armor_prevents_death_from_single_hit(self):
        """Test que la armadura puede prevenir muerte en un golpe"""
        # Sin armadura: muere
        hero1 = Character("Hero1", health=50)
        hero1.take_damage(60)
        self.assertFalse(hero1.is_alive)
        
        # Con armadura pesada: sobrevive
        hero2 = Character("Hero2", health=50, armor=HeavyArmor())
        hero2.take_damage(60)  # 60 - 50% = 30 daño
        self.assertTrue(hero2.is_alive)
        self.assertEqual(hero2.health, 20)

    def test_combat_system_with_armored_target(self):
        """Test de integración: combate con objetivo que tiene armadura"""
        mock_calculator = MagicMock()
        mock_calculator.check_critical_hit.return_value = False
        
        combat = CombatSystem(mock_calculator)
        attacker = Character("Warrior")
        defender = Character("Knight", armor=HeavyArmor())
        sword = Sword()
        
        # Espada hace 15 de daño, armadura pesada reduce 50%
        result = combat.perform_attack(attacker, sword, defender)
        
        # 15 - 50% = 7.5 -> 8 (redondeado hacia arriba)
        expected_health = 100 - 8
        self.assertEqual(defender.health, expected_health)

    def test_combat_system_critical_with_armor(self):
        """Test crítico con armadura: daño crítico también se reduce"""
        mock_calculator = MagicMock()
        mock_calculator.check_critical_hit.return_value = True
        
        combat = CombatSystem(mock_calculator)
        attacker = Character("Rogue")
        defender = Character("Guardian", armor=LightArmor())
        bow = Bow()
        
        combat.perform_attack(attacker, bow, defender)
        
        # Bow: 12 daño + 10 crítico = 22 total
        # 22 - 30% = 15.4 -> 16 (redondeado hacia arriba)
        expected_health = 100 - 16
        self.assertEqual(defender.health, expected_health)

    def test_armor_defense_values(self):
        """Test que las armaduras retornan valores de defensa correctos"""
        light = LightArmor()
        heavy = HeavyArmor()
        
        self.assertEqual(light.get_defense_value(), 5)
        self.assertEqual(heavy.get_defense_value(), 10)

    def test_zero_damage_with_armor(self):
        """Test que armadura maneja correctamente daño cero"""
        armor = HeavyArmor()
        reduced_damage = armor.calculate_damage_reduction(0)
        self.assertEqual(reduced_damage, 0)

    def test_small_damage_with_armor(self):
        """Test que armadura maneja correctamente daños pequeños"""
        hero = Character("Hero", armor=HeavyArmor())
        damage_taken = hero.take_damage(1)
        
        # 1 - 50% = 0.5 -> 1 (redondeado hacia arriba)
        self.assertEqual(damage_taken, 1)
        self.assertEqual(hero.health, 99)
    