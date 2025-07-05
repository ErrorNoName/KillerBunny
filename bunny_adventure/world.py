"""
World and location classes for the KillerBunny adventure game.

This module defines the game world, locations, and navigation system.
"""

from typing import Dict, List, Optional


class Location:
    """Represents a location in the game world."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.exits: Dict[str, str] = {}  # direction -> location_name
        self.items: List[str] = []
        self.visited = False
        self.hidden_items: List[str] = []  # Items revealed through special actions
        
    def add_exit(self, direction: str, destination: str):
        """Add an exit to another location."""
        self.exits[direction] = destination
        
    def add_item(self, item: str, hidden: bool = False):
        """Add an item to this location."""
        if hidden:
            self.hidden_items.append(item)
        else:
            self.items.append(item)
            
    def reveal_hidden_items(self):
        """Move all hidden items to visible items."""
        self.items.extend(self.hidden_items)
        self.hidden_items.clear()
        
    def remove_item(self, item: str) -> bool:
        """Remove an item from this location."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
        
    def get_full_description(self) -> str:
        """Get full description including items and exits."""
        desc = self.description
        
        if self.items:
            desc += f"\n\nYou see: {', '.join(self.items)}"
            
        if self.exits:
            desc += f"\nExits: {', '.join(self.exits.keys())}"
            
        return desc
        
    def __str__(self):
        return f"{self.name}: {self.description}"


class GameWorld:
    """Manages the game world and player movement."""
    
    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.current_location: Optional[Location] = None
        self._create_world()
        
    def _create_world(self):
        """Create the game world with all locations."""
        
        # Create locations
        forest_entrance = Location(
            "Forest Entrance",
            "You stand at the edge of a dark, mysterious forest. Ancient trees loom overhead, "
            "their branches creating an canopy that blocks much of the sunlight. A narrow path "
            "leads deeper into the woods to the north. You can hear strange sounds echoing "
            "from within the forest depths."
        )
        
        dark_path = Location(
            "Dark Forest Path",
            "You're on a winding path through the dark forest. The trees seem to whisper "
            "ancient secrets as the wind rustles through their leaves. Twisted roots cross "
            "the path, making travel treacherous. To the east, you notice a clearing where "
            "sunlight breaks through the canopy."
        )
        
        sunny_clearing = Location(
            "Sunny Clearing",
            "A beautiful clearing bathed in warm sunlight provides a peaceful respite from "
            "the dark forest. Wildflowers bloom in colorful patches, and a small stream "
            "babbles nearby. This seems like a safe place to rest and gather your strength. "
            "To the north, the path continues deeper into the forest."
        )
        
        rocky_outcrop = Location(
            "Rocky Outcrop",
            "You've climbed to a rocky outcrop that overlooks the forest below. From here, "
            "you can see the entire woodland spread out beneath you. To the east, you notice "
            "a dark cave entrance carved into the hillside. Ancient warning signs in long-dead "
            "languages are carved into the rocks around the cave."
        )
        
        cave_entrance = Location(
            "Cave Entrance",
            "You stand before the entrance to a foreboding cave. The opening is roughly "
            "circular and disappears into darkness. Scattered around the entrance are the "
            "bleached bones of previous adventurers who dared to enter. A rusty sign reads: "
            "'Danger! Cave of Caerbannog! Beware the Rabbit!' "
            "Do you dare to enter?"
        )
        
        the_cave = Location(
            "The Cave",
            "You are inside the infamous Cave of Caerbannog. The cave is surprisingly spacious, "
            "with rough stone walls and a high ceiling. In the center of the cave, on a small "
            "pedestal of ancient stone, sits a magnificent golden chalice that gleams even in "
            "the dim light - the Holy Grail! But between you and your prize lurks the most "
            "foul, cruel, and bad-tempered rodent you ever set eyes on..."
        )
        
        # Add locations to world
        self.locations = {
            "Forest Entrance": forest_entrance,
            "Dark Forest Path": dark_path,
            "Sunny Clearing": sunny_clearing,
            "Rocky Outcrop": rocky_outcrop,
            "Cave Entrance": cave_entrance,
            "The Cave": the_cave
        }
        
        # Set up exits (bidirectional connections)
        self._add_bidirectional_exit("Forest Entrance", "north", "Dark Forest Path", "south")
        self._add_bidirectional_exit("Dark Forest Path", "east", "Sunny Clearing", "west")
        self._add_bidirectional_exit("Sunny Clearing", "north", "Rocky Outcrop", "south")
        self._add_bidirectional_exit("Rocky Outcrop", "east", "Cave Entrance", "west")
        self._add_bidirectional_exit("Cave Entrance", "north", "The Cave", "south")
        
        # Add items to locations
        self.locations["Sunny Clearing"].add_item("Health Potion")
        self.locations["Sunny Clearing"].add_item("Old Sword", hidden=True)  # Found by searching
        self.locations["Cave Entrance"].add_item("Ancient Shield")
        self.locations["Rocky Outcrop"].add_item("Rope")
        
        # Set starting location
        self.current_location = self.locations["Forest Entrance"]
        
    def _add_bidirectional_exit(self, loc1_name: str, dir1: str, loc2_name: str, dir2: str):
        """Add exits in both directions between two locations."""
        self.locations[loc1_name].add_exit(dir1, loc2_name)
        self.locations[loc2_name].add_exit(dir2, loc1_name)
        
    def move(self, direction: str) -> bool:
        """Move the player in the specified direction."""
        direction = direction.lower()
        
        if direction in self.current_location.exits:
            destination_name = self.current_location.exits[direction]
            self.current_location = self.locations[destination_name]
            
            # Mark location as visited
            if not self.current_location.visited:
                self.current_location.visited = True
                
            return True
        return False
        
    def get_current_location(self) -> Location:
        """Get the current location."""
        return self.current_location
        
    def get_location(self, name: str) -> Optional[Location]:
        """Get a specific location by name."""
        return self.locations.get(name)
        
    def get_all_locations(self) -> Dict[str, Location]:
        """Get all locations in the world."""
        return self.locations.copy()
        
    def search_current_location(self) -> List[str]:
        """Search the current location for hidden items."""
        if self.current_location.hidden_items:
            found_items = self.current_location.hidden_items.copy()
            self.current_location.reveal_hidden_items()
            return found_items
        return []
        
    def get_visited_locations(self) -> List[str]:
        """Get a list of all visited location names."""
        return [name for name, location in self.locations.items() if location.visited]
        
    def get_map_description(self) -> str:
        """Get a textual description of the world map."""
        map_desc = "World Map (visited locations marked with *):\n\n"
        
        # Create a simple ASCII representation
        map_layout = [
            "                    [The Cave]",
            "                        |",
            "[Rocky Outcrop] --- [Cave Entrance]",
            "        |",
            "[Sunny Clearing]",
            "        |",
            "[Dark Forest Path]",
            "        |",
            "[Forest Entrance]"
        ]
        
        for line in map_layout:
            # Mark visited locations
            for loc_name in self.locations:
                if self.locations[loc_name].visited:
                    line = line.replace(f"[{loc_name}]", f"[{loc_name}]*")
                    
            # Mark current location
            if self.current_location:
                line = line.replace(f"[{self.current_location.name}]", 
                                  f"[{self.current_location.name}] <-- YOU ARE HERE")
                line = line.replace(f"[{self.current_location.name}]*", 
                                  f"[{self.current_location.name}]* <-- YOU ARE HERE")
                                  
            map_desc += line + "\n"
            
        return map_desc
        
    def get_world_stats(self) -> Dict[str, int]:
        """Get statistics about the world."""
        total_locations = len(self.locations)
        visited_locations = len(self.get_visited_locations())
        total_items = sum(len(loc.items) + len(loc.hidden_items) for loc in self.locations.values())
        
        return {
            "total_locations": total_locations,
            "visited_locations": visited_locations,
            "exploration_percentage": int((visited_locations / total_locations) * 100),
            "total_items": total_items
        }


# World constants and data
WORLD_LORE = {
    "Cave of Caerbannog": (
        "Legend tells of a cave guarded by a creature so foul, so cruel, "
        "that no knight has ever returned alive. The beast within is said to have "
        "teeth like daggers and a hunger for human flesh."
    ),
    "Holy Grail": (
        "The Holy Grail, the most sacred relic in all the land. It is said to grant "
        "eternal life to those pure of heart who drink from it. Many have sought it, "
        "but none have succeeded in claiming it."
    ),
    "Forest of Caerbannog": (
        "An ancient woodland shrouded in mystery and danger. The trees themselves "
        "seem alive, and strange creatures lurk in the shadows. Few dare to enter, "
        "and fewer still emerge unchanged."
    )
}

LOCATION_HINTS = {
    "Forest Entrance": "Listen carefully - you might hear clues about what lies ahead.",
    "Dark Forest Path": "The path splits here - choose your direction wisely.",
    "Sunny Clearing": "This peaceful spot might be perfect for finding useful items.",
    "Rocky Outcrop": "A high vantage point often reveals hidden secrets.",
    "Cave Entrance": "Prepare yourself well before entering the cave.",
    "The Cave": "The ultimate test awaits within these ancient walls."
}