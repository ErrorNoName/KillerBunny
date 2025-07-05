#!/usr/bin/env python3
"""
KillerBunny Adventure Game

A text-based adventure game featuring a killer bunny protecting the Holy Grail.
Demonstrates object-oriented programming, game state management, and user interaction.
"""

import random
import sys
from typing import Dict, List, Optional
from characters import Player, KillerBunny, Knight
from world import GameWorld, Location


class GameEngine:
    """Main game engine that manages game flow and state."""
    
    def __init__(self):
        self.world = GameWorld()
        self.player = Player("Brave Knight", 100, 20)
        self.killer_bunny = KillerBunny("The Killer Bunny of Caerbannog", 80, 30)
        self.game_over = False
        self.has_holy_grail = False
        
    def start_game(self):
        """Start the adventure game."""
        self.display_intro()
        
        while not self.game_over:
            self.display_current_status()
            action = self.get_player_action()
            self.process_action(action)
            
        self.display_ending()
    
    def display_intro(self):
        """Display the game introduction."""
        print("\n" + "="*60)
        print("🐰 WELCOME TO THE KILLER BUNNY ADVENTURE! 🐰")
        print("="*60)
        print("""
You are a brave knight on a quest to retrieve the Holy Grail,
guarded by the most foul, cruel, and bad-tempered rodent
you ever set eyes on - The Killer Bunny of Caerbannog!

Your mission: Outsmart or defeat the bunny and claim the grail.
But beware... this is no ordinary bunny!

Type 'help' for available commands.
        """)
        
    def display_current_status(self):
        """Display current game status."""
        print(f"\n📍 Location: {self.world.current_location.name}")
        print(f"🏥 Health: {self.player.health}/{self.player.max_health}")
        print(f"⚔️  Attack: {self.player.attack_power}")
        
        if self.has_holy_grail:
            print("✨ You possess the Holy Grail!")
            
        print(f"\n{self.world.current_location.description}")
        
        # Show available exits
        if self.world.current_location.exits:
            print(f"Exits: {', '.join(self.world.current_location.exits.keys())}")
    
    def get_player_action(self):
        """Get and validate player input."""
        return input("\n> ").strip().lower()
    
    def process_action(self, action: str):
        """Process player action and update game state."""
        parts = action.split()
        command = parts[0] if parts else ""
        
        if command == "help":
            self.show_help()
        elif command == "look":
            self.look_around()
        elif command in ["go", "move", "walk"]:
            if len(parts) > 1:
                self.move_player(parts[1])
            else:
                print("Go where? (north, south, east, west)")
        elif command in ["north", "south", "east", "west", "n", "s", "e", "w"]:
            direction_map = {"n": "north", "s": "south", "e": "east", "w": "west"}
            direction = direction_map.get(command, command)
            self.move_player(direction)
        elif command in ["attack", "fight", "battle"]:
            self.combat()
        elif command in ["take", "get", "grab"]:
            if len(parts) > 1:
                self.take_item(" ".join(parts[1:]))
            else:
                print("Take what?")
        elif command in ["inventory", "inv", "items"]:
            self.show_inventory()
        elif command in ["quit", "exit", "q"]:
            print("Thanks for playing! Goodbye!")
            self.game_over = True
        else:
            print("I don't understand that command. Type 'help' for available commands.")
    
    def show_help(self):
        """Display available commands."""
        print("""
Available Commands:
  help              - Show this help message
  look              - Look around the current area
  go <direction>    - Move in a direction (north, south, east, west)
  n, s, e, w        - Quick movement commands
  attack/fight      - Attack the killer bunny (if present)
  take <item>       - Take an item
  inventory/inv     - Show your items
  quit/exit         - Exit the game
        """)
    
    def look_around(self):
        """Provide detailed description of current location."""
        location = self.world.current_location
        print(f"\n{location.name}")
        print(f"{location.description}")
        
        if location.items:
            print(f"You see: {', '.join(location.items)}")
            
        if location.name == "The Cave" and not self.killer_bunny.is_defeated:
            print(f"\n🐰 {self.killer_bunny.name} is here, guarding the Holy Grail!")
            print("The bunny has big, sharp, pointy teeth!")
    
    def move_player(self, direction: str):
        """Move player to a new location."""
        if self.world.move(direction):
            print(f"You move {direction}.")
            
            # Special events in certain locations
            if self.world.current_location.name == "The Cave":
                if not self.killer_bunny.is_defeated:
                    print(f"\n🐰 Suddenly, {self.killer_bunny.name} appears!")
                    print("It has nasty, big, pointy teeth! It's looking at you menacingly!")
        else:
            print("You can't go that way.")
    
    def combat(self):
        """Handle combat with the killer bunny."""
        if self.world.current_location.name != "The Cave":
            print("There's nothing to fight here.")
            return
            
        if self.killer_bunny.is_defeated:
            print("The killer bunny has already been defeated.")
            return
            
        print(f"\n⚔️  COMBAT BEGINS! ⚔️")
        print(f"You face {self.killer_bunny.name}!")
        
        while not self.player.is_defeated and not self.killer_bunny.is_defeated:
            # Player attacks first
            damage = self.player.attack(self.killer_bunny)
            print(f"You attack for {damage} damage!")
            
            if self.killer_bunny.is_defeated:
                print(f"\n🎉 Victory! You have defeated {self.killer_bunny.name}!")
                print("The bunny lies motionless. The cave is now safe!")
                self.world.current_location.items.append("Holy Grail")
                break
                
            # Bunny counter-attacks
            damage = self.killer_bunny.attack(self.player)
            print(f"The bunny attacks you for {damage} damage!")
            
            if self.player.is_defeated:
                print(f"\n💀 Game Over! {self.killer_bunny.name} has defeated you!")
                print("The bunny gnaws on your bones... Your quest has failed!")
                self.game_over = True
                break
                
            print(f"Your health: {self.player.health}, Bunny health: {self.killer_bunny.health}")
    
    def take_item(self, item_name: str):
        """Take an item from the current location."""
        location = self.world.current_location
        
        if item_name.lower() in [item.lower() for item in location.items]:
            # Find the actual item name (preserve case)
            actual_item = next(item for item in location.items if item.lower() == item_name.lower())
            location.items.remove(actual_item)
            self.player.inventory.append(actual_item)
            
            if actual_item == "Holy Grail":
                self.has_holy_grail = True
                print(f"\n✨ You have obtained the {actual_item}! ✨")
                print("Your quest is complete! You are victorious!")
                self.game_over = True
            else:
                print(f"You take the {actual_item}.")
        else:
            print(f"There's no {item_name} here.")
    
    def show_inventory(self):
        """Display player's inventory."""
        if self.player.inventory:
            print("You are carrying:")
            for item in self.player.inventory:
                print(f"  - {item}")
        else:
            print("Your inventory is empty.")
    
    def display_ending(self):
        """Display appropriate ending based on game state."""
        print("\n" + "="*60)
        if self.has_holy_grail:
            print("🏆 CONGRATULATIONS! QUEST COMPLETED! 🏆")
            print("""
You have successfully retrieved the Holy Grail!
Your bravery in facing the Killer Bunny of Caerbannog
will be remembered for generations!

The realm is safe, and you are hailed as a hero!
            """)
        elif self.player.is_defeated:
            print("💀 QUEST FAILED 💀")
            print("""
The Killer Bunny has proven too powerful.
Your bones join those of countless other knights
who dared to challenge the beast.

Perhaps another brave soul will succeed where you failed...
            """)
        else:
            print("👋 FAREWELL, BRAVE KNIGHT! 👋")
            print("Your quest remains incomplete, but you may return another day...")
        print("="*60)


def main():
    """Main entry point for the game."""
    try:
        game = GameEngine()
        game.start_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("The game will now exit.")


if __name__ == "__main__":
    main()