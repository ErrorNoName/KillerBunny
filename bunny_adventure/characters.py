"""
Character classes for the KillerBunny adventure game.

This module defines the base Character class and specific character types
including Player, KillerBunny, and Knight classes.
"""

import random
from typing import List
from abc import ABC, abstractmethod


class Character(ABC):
    """Abstract base class for all game characters."""
    
    def __init__(self, name: str, health: int, attack_power: int):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.is_defeated = False
    
    def take_damage(self, damage: int):
        """Apply damage to the character."""
        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.is_defeated = True
    
    def heal(self, amount: int):
        """Heal the character."""
        self.health = min(self.max_health, self.health + amount)
        if self.health > 0:
            self.is_defeated = False
    
    @abstractmethod
    def attack(self, target: 'Character') -> int:
        """Attack another character. Returns damage dealt."""
        pass
    
    def __str__(self):
        return f"{self.name} (Health: {self.health}/{self.max_health})"


class Player(Character):
    """Player character class."""
    
    def __init__(self, name: str, health: int, attack_power: int):
        super().__init__(name, health, attack_power)
        self.inventory: List[str] = []
        self.experience = 0
        self.level = 1
    
    def attack(self, target: Character) -> int:
        """Player attack with slight randomization."""
        base_damage = self.attack_power
        # Add some randomness to combat
        damage_variance = random.randint(-3, 5)
        actual_damage = max(1, base_damage + damage_variance)
        
        target.take_damage(actual_damage)
        return actual_damage
    
    def gain_experience(self, amount: int):
        """Gain experience points and potentially level up."""
        self.experience += amount
        new_level = 1 + (self.experience // 100)
        
        if new_level > self.level:
            old_level = self.level
            self.level = new_level
            # Increase stats on level up
            health_increase = 10 * (new_level - old_level)
            attack_increase = 2 * (new_level - old_level)
            
            self.max_health += health_increase
            self.health += health_increase  # Full heal on level up
            self.attack_power += attack_increase
            
            return True  # Leveled up
        return False  # No level up
    
    def use_item(self, item_name: str) -> bool:
        """Use an item from inventory."""
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            
            # Basic item effects
            if "potion" in item_name.lower():
                heal_amount = 30
                self.heal(heal_amount)
                return True
            elif "sword" in item_name.lower():
                self.attack_power += 5
                return True
                
        return False


class KillerBunny(Character):
    """The notorious Killer Bunny of Caerbannog."""
    
    def __init__(self, name: str, health: int, attack_power: int):
        super().__init__(name, health, attack_power)
        self.rage_mode = False
        self.attacks_made = 0
    
    def attack(self, target: Character) -> int:
        """Killer bunny's vicious attack."""
        self.attacks_made += 1
        
        # Bunny gets more dangerous as fight continues
        if self.attacks_made >= 3 and not self.rage_mode:
            self.rage_mode = True
            self.attack_power += 10
            print("🔥 The bunny enters RAGE MODE! Its eyes glow red!")
        
        # Critical hit chance
        is_critical = random.random() < 0.25  # 25% critical hit chance
        base_damage = self.attack_power
        
        if is_critical:
            actual_damage = int(base_damage * 1.5)
            print("💥 CRITICAL HIT! The bunny's teeth find their mark!")
        else:
            # Normal attack with some variance
            damage_variance = random.randint(-2, 4)
            actual_damage = max(1, base_damage + damage_variance)
        
        # Special attacks based on health
        if self.health < self.max_health * 0.3:  # Below 30% health
            if random.random() < 0.3:  # 30% chance for desperate attack
                actual_damage += 8
                print("🐰 The bunny makes a desperate, wild attack!")
        
        target.take_damage(actual_damage)
        return actual_damage
    
    def take_damage(self, damage: int):
        """Override to add special behavior when taking damage."""
        super().take_damage(damage)
        
        # Taunt messages based on health
        if not self.is_defeated:
            if self.health < self.max_health * 0.2:
                print("The bunny is badly wounded but still dangerous!")
            elif self.health < self.max_health * 0.5:
                print("The bunny snarls and shows its bloody teeth!")


class Knight(Character):
    """A generic knight character (for potential future use)."""
    
    def __init__(self, name: str, health: int = 80, attack_power: int = 18):
        super().__init__(name, health, attack_power)
        self.armor_class = 5  # Damage reduction
        self.weapon = "Sword"
        self.shield = True
    
    def attack(self, target: Character) -> int:
        """Knight's disciplined attack."""
        base_damage = self.attack_power
        
        # Knights have consistent damage (less variance)
        damage_variance = random.randint(-1, 3)
        actual_damage = max(1, base_damage + damage_variance)
        
        # Bonus damage if target is wounded
        if hasattr(target, 'health') and target.health < target.max_health * 0.3:
            actual_damage += 3  # Finishing blow bonus
        
        target.take_damage(actual_damage)
        return actual_damage
    
    def take_damage(self, damage: int):
        """Knights have armor that reduces damage."""
        reduced_damage = max(1, damage - self.armor_class)
        super().take_damage(reduced_damage)
        
        if reduced_damage < damage:
            print(f"Your armor absorbs {damage - reduced_damage} damage!")
    
    def raise_shield(self):
        """Defensive action that reduces next attack damage."""
        self.armor_class += 3
        print("You raise your shield defensively!")
    
    def lower_shield(self):
        """Reset armor after shield use."""
        self.armor_class = max(5, self.armor_class - 3)


# Character factory function
def create_character(char_type: str, name: str = None) -> Character:
    """Factory function to create different character types."""
    char_type = char_type.lower()
    
    if char_type == "player":
        return Player(name or "Brave Knight", 100, 20)
    elif char_type == "killer_bunny":
        return KillerBunny(name or "The Killer Bunny of Caerbannog", 80, 30)
    elif char_type == "knight":
        return Knight(name or "Sir Knight", 80, 18)
    else:
        raise ValueError(f"Unknown character type: {char_type}")


# Character stats for reference
CHARACTER_STATS = {
    "player": {"base_health": 100, "base_attack": 20, "special": "Experience/Leveling"},
    "killer_bunny": {"base_health": 80, "base_attack": 30, "special": "Rage Mode, Critical Hits"},
    "knight": {"base_health": 80, "base_attack": 18, "special": "Armor, Shield Defense"}
}