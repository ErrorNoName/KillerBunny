#!/usr/bin/env python3
"""
Test suite for the KillerBunny Adventure Game

This demonstrates proper testing practices, including:
- Unit testing
- Test fixtures
- Mock objects
- Edge case testing
- Integration testing
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch
from io import StringIO

# Add the bunny_adventure directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bunny_adventure'))

from characters import Character, Player, KillerBunny, Knight, create_character
from world import GameWorld, Location
from game import GameEngine


class TestCharacters(unittest.TestCase):
    """Test cases for character classes."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.player = Player("Test Knight", 100, 20)
        self.bunny = KillerBunny("Test Bunny", 80, 30)
        self.knight = Knight("Sir Test", 80, 18)
    
    def test_character_creation(self):
        """Test character creation and initialization."""
        self.assertEqual(self.player.name, "Test Knight")
        self.assertEqual(self.player.health, 100)
        self.assertEqual(self.player.max_health, 100)
        self.assertEqual(self.player.attack_power, 20)
        self.assertFalse(self.player.is_defeated)
        self.assertEqual(len(self.player.inventory), 0)
    
    def test_take_damage(self):
        """Test damage application."""
        initial_health = self.player.health
        damage = 25
        self.player.take_damage(damage)
        
        self.assertEqual(self.player.health, initial_health - damage)
        self.assertFalse(self.player.is_defeated)
        
        # Test lethal damage
        self.player.take_damage(100)
        self.assertEqual(self.player.health, 0)
        self.assertTrue(self.player.is_defeated)
    
    def test_healing(self):
        """Test healing functionality."""
        self.player.take_damage(50)
        self.player.heal(30)
        self.assertEqual(self.player.health, 80)
        
        # Test healing beyond max health
        self.player.heal(50)
        self.assertEqual(self.player.health, self.player.max_health)
        self.assertFalse(self.player.is_defeated)
    
    def test_player_attack(self):
        """Test player attack mechanics."""
        target = Mock()
        target.take_damage = Mock()
        
        damage = self.player.attack(target)
        
        self.assertGreater(damage, 0)
        self.assertLessEqual(damage, self.player.attack_power + 5)  # Max variance
        target.take_damage.assert_called_once_with(damage)
    
    def test_bunny_rage_mode(self):
        """Test killer bunny's rage mode activation."""
        target = Mock()
        target.take_damage = Mock()
        
        initial_attack = self.bunny.attack_power
        
        # Make multiple attacks to trigger rage mode
        for _ in range(4):
            self.bunny.attack(target)
        
        self.assertTrue(self.bunny.rage_mode)
        self.assertGreater(self.bunny.attack_power, initial_attack)
    
    def test_knight_armor(self):
        """Test knight's armor damage reduction."""
        damage = 20
        expected_reduced_damage = max(1, damage - self.knight.armor_class)
        
        initial_health = self.knight.health
        self.knight.take_damage(damage)
        
        expected_health = initial_health - expected_reduced_damage
        self.assertEqual(self.knight.health, expected_health)
    
    def test_player_experience_system(self):
        """Test player experience and leveling."""
        initial_level = self.player.level
        initial_attack = self.player.attack_power
        
        # Gain enough experience to level up
        leveled_up = self.player.gain_experience(100)
        
        self.assertTrue(leveled_up)
        self.assertEqual(self.player.level, initial_level + 1)
        self.assertGreater(self.player.attack_power, initial_attack)
        self.assertGreater(self.player.max_health, 100)
    
    def test_character_factory(self):
        """Test character factory function."""
        player = create_character("player", "Test Player")
        self.assertIsInstance(player, Player)
        self.assertEqual(player.name, "Test Player")
        
        bunny = create_character("killer_bunny")
        self.assertIsInstance(bunny, KillerBunny)
        
        with self.assertRaises(ValueError):
            create_character("invalid_type")


class TestWorld(unittest.TestCase):
    """Test cases for world and location classes."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.world = GameWorld()
        self.test_location = Location("Test Room", "A test room for testing.")
    
    def test_location_creation(self):
        """Test location creation and initialization."""
        self.assertEqual(self.test_location.name, "Test Room")
        self.assertEqual(self.test_location.description, "A test room for testing.")
        self.assertEqual(len(self.test_location.exits), 0)
        self.assertEqual(len(self.test_location.items), 0)
        self.assertFalse(self.test_location.visited)
    
    def test_location_exits(self):
        """Test location exit management."""
        self.test_location.add_exit("north", "North Room")
        self.test_location.add_exit("south", "South Room")
        
        self.assertIn("north", self.test_location.exits)
        self.assertIn("south", self.test_location.exits)
        self.assertEqual(self.test_location.exits["north"], "North Room")
    
    def test_location_items(self):
        """Test location item management."""
        self.test_location.add_item("Test Item")
        self.test_location.add_item("Hidden Item", hidden=True)
        
        self.assertIn("Test Item", self.test_location.items)
        self.assertIn("Hidden Item", self.test_location.hidden_items)
        self.assertNotIn("Hidden Item", self.test_location.items)
        
        # Test revealing hidden items
        self.test_location.reveal_hidden_items()
        self.assertIn("Hidden Item", self.test_location.items)
        self.assertEqual(len(self.test_location.hidden_items), 0)
    
    def test_world_creation(self):
        """Test world creation and initialization."""
        self.assertIsNotNone(self.world.current_location)
        self.assertGreater(len(self.world.locations), 0)
        
        # Check that all expected locations exist
        expected_locations = [
            "Forest Entrance", "Dark Forest Path", "Sunny Clearing",
            "Rocky Outcrop", "Cave Entrance", "The Cave"
        ]
        for location_name in expected_locations:
            self.assertIn(location_name, self.world.locations)
    
    def test_world_movement(self):
        """Test player movement in the world."""
        initial_location = self.world.current_location.name
        
        # Try valid movement
        valid_moves = list(self.world.current_location.exits.keys())
        if valid_moves:
            direction = valid_moves[0]
            result = self.world.move(direction)
            self.assertTrue(result)
            self.assertNotEqual(self.world.current_location.name, initial_location)
        
        # Try invalid movement
        result = self.world.move("invalid_direction")
        self.assertFalse(result)
    
    def test_world_statistics(self):
        """Test world statistics generation."""
        stats = self.world.get_world_stats()
        
        self.assertIn("total_locations", stats)
        self.assertIn("visited_locations", stats)
        self.assertIn("exploration_percentage", stats)
        self.assertGreater(stats["total_locations"], 0)
        self.assertGreaterEqual(stats["exploration_percentage"], 0)
        self.assertLessEqual(stats["exploration_percentage"], 100)


class TestGameEngine(unittest.TestCase):
    """Test cases for the main game engine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = GameEngine()
    
    def test_game_initialization(self):
        """Test game engine initialization."""
        self.assertIsNotNone(self.game.world)
        self.assertIsNotNone(self.game.player)
        self.assertIsNotNone(self.game.killer_bunny)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.has_holy_grail)
    
    @patch('builtins.input', return_value='help')
    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command(self, mock_stdout, mock_input):
        """Test help command functionality."""
        self.game.process_action('help')
        output = mock_stdout.getvalue()
        self.assertIn("Available Commands", output)
        self.assertIn("help", output)
        self.assertIn("look", output)
        self.assertIn("go", output)
    
    def test_movement_commands(self):
        """Test movement command processing."""
        # Test direct movement
        with patch.object(self.game, 'move_player') as mock_move:
            self.game.process_action('north')
            mock_move.assert_called_with('north')
            
            self.game.process_action('go south')
            mock_move.assert_called_with('south')
    
    def test_combat_system(self):
        """Test combat mechanics."""
        # Move to cave for combat
        self.game.world.current_location = self.game.world.locations["The Cave"]
        
        initial_bunny_health = self.game.killer_bunny.health
        
        # Simulate combat
        with patch('builtins.print'):  # Suppress output
            self.game.combat()
        
        # Combat should have occurred (health changed or bunny defeated)
        self.assertTrue(
            self.game.killer_bunny.health < initial_bunny_health or 
            self.game.killer_bunny.is_defeated or
            self.game.player.health < self.game.player.max_health
        )
    
    def test_item_management(self):
        """Test item taking and inventory."""
        # Add an item to current location
        self.game.world.current_location.add_item("Test Item")
        
        # Take the item
        self.game.take_item("Test Item")
        
        self.assertIn("Test Item", self.game.player.inventory)
        self.assertNotIn("Test Item", self.game.world.current_location.items)
    
    def test_holy_grail_victory(self):
        """Test winning condition with Holy Grail."""
        # Set up victory scenario
        self.game.world.current_location.add_item("Holy Grail")
        
        self.game.take_item("Holy Grail")
        
        self.assertTrue(self.game.has_holy_grail)
        self.assertTrue(self.game.game_over)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete game system."""
    
    def test_complete_game_flow(self):
        """Test a complete game playthrough scenario."""
        game = GameEngine()
        
        # Start at forest entrance
        self.assertEqual(game.world.current_location.name, "Forest Entrance")
        
        # Move through the world
        moves = ["north", "east", "north", "east", "north"]
        for move in moves:
            if move in game.world.current_location.exits:
                game.move_player(move)
        
        # Should eventually reach the cave
        self.assertEqual(game.world.current_location.name, "The Cave")
        
        # Test combat scenario
        if not game.killer_bunny.is_defeated:
            with patch('builtins.print'):  # Suppress combat output
                game.combat()
    
    def test_error_handling(self):
        """Test error handling in various scenarios."""
        game = GameEngine()
        
        # Test invalid commands
        with patch('builtins.print') as mock_print:
            game.process_action('invalid_command')
            mock_print.assert_called()
        
        # Test taking non-existent items
        game.take_item("Nonexistent Item")
        self.assertNotIn("Nonexistent Item", game.player.inventory)
        
        # Test moving in invalid directions
        result = game.world.move("invalid_direction")
        self.assertFalse(result)


def run_test_suite():
    """Run the complete test suite with detailed output."""
    print("🧪 KillerBunny Adventure - Test Suite")
    print("=" * 50)
    
    # Create test loader
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestCharacters,
        TestWorld, 
        TestGameEngine,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('\n')[-2]}")
    
    if result.errors:
        print("\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\n')[-2]}")
    
    if not result.failures and not result.errors:
        print("\n✅ All tests passed! The game is working correctly.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Check if specific test is requested
    if len(sys.argv) > 1:
        # Run specific test
        unittest.main()
    else:
        # Run complete test suite
        success = run_test_suite()
        sys.exit(0 if success else 1)