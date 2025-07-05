#!/usr/bin/env python3
"""
ASCII Art Generator for KillerBunny Adventure

This utility demonstrates Python string manipulation, file I/O, 
and creative programming techniques.
"""

import sys
import random
from typing import List, Dict


class ASCIIArtGenerator:
    """Generates ASCII art for the game."""
    
    def __init__(self):
        self.bunny_art = [
            r"""
    (\   /)
   ( ._.)
  o_(")(")
            """,
            r"""
       /|   /|   
      ( :v:  )
       |(_)|
       o_(")(")
            """,
            r"""
      (\__/)
     (  o.o  )
      > ^ <
     o_(")(")
            """,
            r"""
    /|  /|  
   (  .)( . )
    \_\ /_/
    (")(")
            """
        ]
        
        self.grail_art = r"""
         .-'''-. 
        /       \
       |  ___    |
       | ( o )   |
       |  '''    |
        \       /
         '-----'
        """
        
        self.sword_art = r"""
          /\
         |  |
         |  |
         |  |
         |  |
         |__|
        /    \
       /_____\
        """
        
        self.castle_art = r"""
        /\    /\    /\
       |  |  |  |  |  |
       |  |  |  |  |  |
      /    \/    \/    \
     |      CASTLE      |
     |   OF CAERBANNOG   |
     |__________________|
        """
    
    def get_random_bunny(self) -> str:
        """Get a random bunny ASCII art."""
        return random.choice(self.bunny_art)
    
    def get_grail(self) -> str:
        """Get the Holy Grail ASCII art."""
        return self.grail_art
    
    def get_sword(self) -> str:
        """Get sword ASCII art."""
        return self.sword_art
    
    def get_castle(self) -> str:
        """Get castle ASCII art."""
        return self.castle_art
    
    def create_banner(self, text: str, width: int = 50) -> str:
        """Create a decorative banner with text."""
        border = "=" * width
        padding = (width - len(text) - 2) // 2
        banner = f"""
{border}
{' ' * padding} {text} {' ' * padding}
{border}
        """
        return banner.strip()
    
    def create_box(self, text: str, padding: int = 2) -> str:
        """Create a box around text."""
        lines = text.split('\n')
        max_width = max(len(line) for line in lines)
        box_width = max_width + (padding * 2)
        
        top_bottom = "+" + "-" * (box_width) + "+"
        
        result = [top_bottom]
        for line in lines:
            padded_line = line.ljust(max_width)
            result.append(f"|{' ' * padding}{padded_line}{' ' * padding}|")
        result.append(top_bottom)
        
        return '\n'.join(result)
    
    def animate_text(self, text: str, delay: float = 0.1) -> None:
        """Animate text character by character (for terminal use)."""
        import time
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()  # Final newline
    
    def generate_maze(self, width: int = 15, height: int = 10) -> str:
        """Generate a simple ASCII maze."""
        # Simple maze generation (not a perfect algorithm, but demonstrates the concept)
        maze = [['#' for _ in range(width)] for _ in range(height)]
        
        # Create some paths
        for y in range(1, height - 1, 2):
            for x in range(1, width - 1, 2):
                maze[y][x] = ' '
                
                # Randomly connect paths
                if random.random() > 0.5 and x + 2 < width - 1:
                    maze[y][x + 1] = ' '
                if random.random() > 0.5 and y + 2 < height - 1:
                    maze[y + 1][x] = ' '
        
        # Add entrance and exit
        maze[1][0] = 'S'  # Start
        maze[height - 2][width - 1] = 'E'  # End
        
        # Convert to string
        return '\n'.join(''.join(row) for row in maze)
    
    def create_health_bar(self, current: int, maximum: int, width: int = 20) -> str:
        """Create a visual health bar."""
        percentage = current / maximum
        filled = int(percentage * width)
        empty = width - filled
        
        bar = '█' * filled + '░' * empty
        return f"Health: [{bar}] {current}/{maximum}"
    
    def display_art_gallery(self) -> None:
        """Display all available ASCII art."""
        print(self.create_banner("ASCII ART GALLERY", 60))
        print()
        
        print("🐰 BUNNY VARIATIONS:")
        for i, bunny in enumerate(self.bunny_art, 1):
            print(f"\nBunny #{i}:")
            print(bunny)
        
        print("\n" + "="*60)
        print("✨ HOLY GRAIL:")
        print(self.grail_art)
        
        print("\n" + "="*60)
        print("⚔️ SWORD:")
        print(self.sword_art)
        
        print("\n" + "="*60)
        print("🏰 CASTLE:")
        print(self.castle_art)
        
        print("\n" + "="*60)
        print("🌟 SAMPLE MAZE:")
        print(self.generate_maze())
        
        print("\n" + "="*60)
        print("❤️ HEALTH BAR EXAMPLES:")
        for health in [100, 75, 50, 25, 10]:
            print(self.create_health_bar(health, 100))


def main():
    """Main function for the ASCII art generator."""
    generator = ASCIIArtGenerator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "bunny":
            print(generator.get_random_bunny())
        elif command == "grail":
            print(generator.get_grail())
        elif command == "sword":
            print(generator.get_sword())
        elif command == "castle":
            print(generator.get_castle())
        elif command == "banner" and len(sys.argv) > 2:
            text = " ".join(sys.argv[2:])
            print(generator.create_banner(text))
        elif command == "box" and len(sys.argv) > 2:
            text = " ".join(sys.argv[2:])
            print(generator.create_box(text))
        elif command == "maze":
            print(generator.generate_maze())
        elif command == "health":
            current = int(sys.argv[2]) if len(sys.argv) > 2 else 75
            maximum = int(sys.argv[3]) if len(sys.argv) > 3 else 100
            print(generator.create_health_bar(current, maximum))
        elif command == "gallery":
            generator.display_art_gallery()
        else:
            print("Unknown command. Available commands:")
            print("  bunny    - Random bunny art")
            print("  grail    - Holy Grail art")
            print("  sword    - Sword art")
            print("  castle   - Castle art")
            print("  banner <text> - Create banner")
            print("  box <text>    - Create text box")
            print("  maze     - Generate maze")
            print("  health <current> <max> - Health bar")
            print("  gallery  - Show all art")
    else:
        # Interactive mode
        print(generator.create_banner("ASCII ART GENERATOR"))
        print("\nWelcome to the ASCII Art Generator!")
        print("This utility demonstrates Python programming capabilities.")
        print("\nGenerating some sample art...\n")
        
        print("🐰 Random Bunny:")
        print(generator.get_random_bunny())
        
        print("\n✨ Holy Grail:")
        print(generator.get_grail())
        
        print("\n🌟 Sample Health Bar:")
        print(generator.create_health_bar(85, 100))
        
        print(f"\n{generator.create_box('KillerBunny Adventure ASCII Art!')}")
        
        print("\nFor more options, run with 'gallery' argument!")


if __name__ == "__main__":
    main()