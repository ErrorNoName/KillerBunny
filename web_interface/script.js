/**
 * KillerBunny Adventure - Interactive Web Interface
 * 
 * This JavaScript provides the interactive functionality for the web demo,
 * simulating a text-based adventure game in the browser.
 */

class GameSimulator {
    constructor() {
        this.gameState = {
            location: 'Forest Entrance',
            health: 100,
            maxHealth: 100,
            attack: 20,
            inventory: [],
            bunnyDefeated: false,
            hasGrail: false,
            locations: {
                'Forest Entrance': {
                    description: 'You stand at the edge of a dark, mysterious forest.',
                    exits: ['north'],
                    items: []
                },
                'Dark Forest Path': {
                    description: 'A winding path through the dark forest.',
                    exits: ['south', 'east'],
                    items: []
                },
                'Sunny Clearing': {
                    description: 'A peaceful clearing bathed in warm sunlight.',
                    exits: ['west', 'north'],
                    items: ['Health Potion']
                },
                'Rocky Outcrop': {
                    description: 'A rocky outcrop overlooking the forest.',
                    exits: ['south', 'east'],
                    items: ['Rope']
                },
                'Cave Entrance': {
                    description: 'The entrance to the foreboding Cave of Caerbannog.',
                    exits: ['west', 'north'],
                    items: ['Ancient Shield']
                },
                'The Cave': {
                    description: 'Inside the notorious Cave of Caerbannog.',
                    exits: ['south'],
                    items: []
                }
            }
        };
        
        this.setupEventListeners();
        this.updateDisplay();
    }
    
    setupEventListeners() {
        const commandInput = document.getElementById('commandInput');
        const submitButton = document.getElementById('submitCommand');
        
        // Handle command submission
        submitButton.addEventListener('click', () => {
            this.executeCommand(commandInput.value.trim());
            commandInput.value = '';
            commandInput.focus();
        });
        
        // Handle Enter key in input
        commandInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.executeCommand(commandInput.value.trim());
                commandInput.value = '';
            }
        });
        
        // Focus input on page load
        commandInput.focus();
    }
    
    executeCommand(command) {
        if (!command) return;
        
        const lowerCommand = command.toLowerCase();
        const parts = lowerCommand.split(' ');
        const action = parts[0];
        
        // Add command to terminal output
        this.addOutput(`> ${command}`, 'user-command');
        
        // Process different commands
        switch (action) {
            case 'help':
                this.showHelp();
                break;
            case 'look':
                this.lookAround();
                break;
            case 'go':
            case 'move':
                if (parts.length > 1) {
                    this.move(parts[1]);
                } else {
                    this.addOutput('Go where? (north, south, east, west)');
                }
                break;
            case 'north':
            case 'south':
            case 'east':
            case 'west':
            case 'n':
            case 's':
            case 'e':
            case 'w':
                const directionMap = { 'n': 'north', 's': 'south', 'e': 'east', 'w': 'west' };
                const direction = directionMap[action] || action;
                this.move(direction);
                break;
            case 'attack':
            case 'fight':
                this.attack();
                break;
            case 'take':
            case 'get':
                if (parts.length > 1) {
                    this.takeItem(parts.slice(1).join(' '));
                } else {
                    this.addOutput('Take what?');
                }
                break;
            case 'inventory':
            case 'inv':
                this.showInventory();
                break;
            case 'reset':
                this.resetGame();
                break;
            case 'status':
                this.showStatus();
                break;
            default:
                this.addOutput("I don't understand that command. Type 'help' for available commands.");
        }
        
        this.updateDisplay();
    }
    
    addOutput(text, className = '') {
        const terminal = document.getElementById('terminalOutput');
        const outputLine = document.createElement('div');
        outputLine.className = `output-line ${className}`;
        outputLine.innerHTML = text;
        
        // Remove the cursor line temporarily
        const cursorLine = terminal.querySelector('.prompt');
        if (cursorLine) {
            terminal.removeChild(cursorLine);
        }
        
        terminal.appendChild(outputLine);
        
        // Add cursor line back
        const newCursorLine = document.createElement('div');
        newCursorLine.className = 'output-line prompt';
        newCursorLine.innerHTML = `📍 ${this.gameState.location} > <span class="cursor">_</span>`;
        terminal.appendChild(newCursorLine);
        
        // Scroll to bottom
        terminal.scrollTop = terminal.scrollHeight;
    }
    
    showHelp() {
        this.addOutput('Available Commands:', 'command-help');
        this.addOutput('  help              - Show this help message');
        this.addOutput('  look              - Look around the current area');
        this.addOutput('  go <direction>    - Move in a direction (north, south, east, west)');
        this.addOutput('  n, s, e, w        - Quick movement commands');
        this.addOutput('  attack/fight      - Attack the killer bunny (if present)');
        this.addOutput('  take <item>       - Take an item');
        this.addOutput('  inventory/inv     - Show your items');
        this.addOutput('  status            - Show current status');
        this.addOutput('  reset             - Reset the game');
    }
    
    lookAround() {
        const currentLoc = this.gameState.locations[this.gameState.location];
        this.addOutput(`🔍 ${this.gameState.location}`);
        this.addOutput(currentLoc.description);
        
        if (currentLoc.items.length > 0) {
            this.addOutput(`You see: ${currentLoc.items.join(', ')}`);
        }
        
        if (currentLoc.exits.length > 0) {
            this.addOutput(`Exits: ${currentLoc.exits.join(', ')}`);
        }
        
        if (this.gameState.location === 'The Cave' && !this.gameState.bunnyDefeated) {
            this.addOutput('🐰 The Killer Bunny of Caerbannog is here, guarding the Holy Grail!');
            this.addOutput('It has big, sharp, pointy teeth and is looking at you menacingly!');
        }
        
        if (this.gameState.location === 'The Cave' && this.gameState.bunnyDefeated && !this.gameState.hasGrail) {
            this.addOutput('✨ The Holy Grail sits on a pedestal, gleaming in the dim light!');
            currentLoc.items = ['Holy Grail'];
        }
    }
    
    move(direction) {
        const currentLoc = this.gameState.locations[this.gameState.location];
        
        if (!currentLoc.exits.includes(direction)) {
            this.addOutput("You can't go that way.");
            return;
        }
        
        // Simple navigation logic
        const navigationMap = {
            'Forest Entrance': { 'north': 'Dark Forest Path' },
            'Dark Forest Path': { 'south': 'Forest Entrance', 'east': 'Sunny Clearing' },
            'Sunny Clearing': { 'west': 'Dark Forest Path', 'north': 'Rocky Outcrop' },
            'Rocky Outcrop': { 'south': 'Sunny Clearing', 'east': 'Cave Entrance' },
            'Cave Entrance': { 'west': 'Rocky Outcrop', 'north': 'The Cave' },
            'The Cave': { 'south': 'Cave Entrance' }
        };
        
        const newLocation = navigationMap[this.gameState.location]?.[direction];
        if (newLocation) {
            this.gameState.location = newLocation;
            this.addOutput(`You move ${direction} to ${newLocation}.`);
            
            // Special events
            if (newLocation === 'The Cave' && !this.gameState.bunnyDefeated) {
                this.addOutput('🐰 Suddenly, the Killer Bunny appears!');
                this.addOutput('It has nasty, big, pointy teeth! It\'s blocking your path to the grail!');
            }
        } else {
            this.addOutput("You can't go that way.");
        }
    }
    
    attack() {
        if (this.gameState.location !== 'The Cave') {
            this.addOutput("There's nothing to fight here.");
            return;
        }
        
        if (this.gameState.bunnyDefeated) {
            this.addOutput("The killer bunny has already been defeated.");
            return;
        }
        
        this.addOutput('⚔️ COMBAT BEGINS!');
        this.addOutput('You engage the Killer Bunny in fierce combat!');
        
        // Simulate combat
        const playerDamage = Math.floor(Math.random() * 10) + 15;
        const bunnyDamage = Math.floor(Math.random() * 15) + 10;
        
        this.addOutput(`You attack for ${playerDamage} damage!`);
        
        if (Math.random() > 0.3) { // 70% chance to win
            this.addOutput('🎉 Victory! You have defeated the Killer Bunny!');
            this.addOutput('The bunny lies motionless. The cave is now safe!');
            this.gameState.bunnyDefeated = true;
            this.gameState.locations['The Cave'].items = ['Holy Grail'];
        } else {
            this.addOutput(`The bunny counter-attacks for ${bunnyDamage} damage!`);
            this.gameState.health = Math.max(0, this.gameState.health - bunnyDamage);
            
            if (this.gameState.health <= 0) {
                this.addOutput('💀 Game Over! The Killer Bunny has defeated you!');
                this.addOutput('Your quest has failed... but you can try again!');
                this.resetGame();
                return;
            }
            
            this.addOutput('The battle continues! Try attacking again!');
        }
    }
    
    takeItem(itemName) {
        const currentLoc = this.gameState.locations[this.gameState.location];
        const item = currentLoc.items.find(i => i.toLowerCase().includes(itemName.toLowerCase()));
        
        if (item) {
            currentLoc.items = currentLoc.items.filter(i => i !== item);
            this.gameState.inventory.push(item);
            
            if (item === 'Holy Grail') {
                this.gameState.hasGrail = true;
                this.addOutput('✨ You have obtained the Holy Grail! ✨');
                this.addOutput('🏆 QUEST COMPLETE! You are victorious!');
                this.addOutput('Your bravery will be remembered for generations!');
            } else {
                this.addOutput(`You take the ${item}.`);
                
                // Apply item effects
                if (item === 'Health Potion') {
                    this.gameState.health = Math.min(this.gameState.maxHealth, this.gameState.health + 30);
                    this.addOutput('The potion restores 30 health!');
                } else if (item === 'Ancient Shield') {
                    this.gameState.attack += 5;
                    this.addOutput('The shield increases your combat effectiveness!');
                }
            }
        } else {
            this.addOutput(`There's no ${itemName} here.`);
        }
    }
    
    showInventory() {
        if (this.gameState.inventory.length === 0) {
            this.addOutput('Your inventory is empty.');
        } else {
            this.addOutput('You are carrying:');
            this.gameState.inventory.forEach(item => {
                this.addOutput(`  - ${item}`);
            });
        }
    }
    
    showStatus() {
        this.addOutput('=== CURRENT STATUS ===');
        this.addOutput(`Location: ${this.gameState.location}`);
        this.addOutput(`Health: ${this.gameState.health}/${this.gameState.maxHealth}`);
        this.addOutput(`Attack Power: ${this.gameState.attack}`);
        this.addOutput(`Items: ${this.gameState.inventory.length}`);
        if (this.gameState.bunnyDefeated) {
            this.addOutput('✅ Killer Bunny: Defeated');
        }
        if (this.gameState.hasGrail) {
            this.addOutput('✨ Holy Grail: Obtained');
        }
    }
    
    resetGame() {
        this.gameState = {
            location: 'Forest Entrance',
            health: 100,
            maxHealth: 100,
            attack: 20,
            inventory: [],
            bunnyDefeated: false,
            hasGrail: false,
            locations: {
                'Forest Entrance': {
                    description: 'You stand at the edge of a dark, mysterious forest.',
                    exits: ['north'],
                    items: []
                },
                'Dark Forest Path': {
                    description: 'A winding path through the dark forest.',
                    exits: ['south', 'east'],
                    items: []
                },
                'Sunny Clearing': {
                    description: 'A peaceful clearing bathed in warm sunlight.',
                    exits: ['west', 'north'],
                    items: ['Health Potion']
                },
                'Rocky Outcrop': {
                    description: 'A rocky outcrop overlooking the forest.',
                    exits: ['south', 'east'],
                    items: ['Rope']
                },
                'Cave Entrance': {
                    description: 'The entrance to the foreboding Cave of Caerbannog.',
                    exits: ['west', 'north'],
                    items: ['Ancient Shield']
                },
                'The Cave': {
                    description: 'Inside the notorious Cave of Caerbannog.',
                    exits: ['south'],
                    items: []
                }
            }
        };
        
        // Clear terminal
        const terminal = document.getElementById('terminalOutput');
        terminal.innerHTML = `
            <div class="output-line">Game Reset! Welcome back to the KillerBunny Adventure!</div>
            <div class="output-line">Type commands to explore the world...</div>
            <div class="output-line prompt">📍 Forest Entrance > <span class="cursor">_</span></div>
        `;
        
        this.updateDisplay();
    }
    
    updateDisplay() {
        // Update stats display
        document.getElementById('playerHealth').textContent = `${this.gameState.health}/${this.gameState.maxHealth}`;
        document.getElementById('playerAttack').textContent = this.gameState.attack;
        document.getElementById('currentLocation').textContent = this.gameState.location;
        document.getElementById('itemCount').textContent = this.gameState.inventory.length;
        
        // Update health bar
        const healthPercentage = (this.gameState.health / this.gameState.maxHealth) * 100;
        document.getElementById('healthBar').style.width = `${healthPercentage}%`;
        
        // Update prompt in terminal
        const prompts = document.querySelectorAll('.prompt');
        if (prompts.length > 0) {
            const lastPrompt = prompts[prompts.length - 1];
            lastPrompt.innerHTML = `📍 ${this.gameState.location} > <span class="cursor">_</span>`;
        }
    }
}

// Enhanced animations and effects
class UIEffects {
    static addGlowEffect(element, duration = 1000) {
        element.style.animation = `glow ${duration}ms ease-in-out`;
        setTimeout(() => {
            element.style.animation = '';
        }, duration);
    }
    
    static typeWriter(element, text, speed = 50) {
        element.textContent = '';
        let i = 0;
        const timer = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
            }
        }, speed);
    }
    
    static shakeElement(element, duration = 500) {
        element.style.animation = `shake ${duration}ms ease-in-out`;
        setTimeout(() => {
            element.style.animation = '';
        }, duration);
    }
}

// Add shake animation to CSS
const shakeCSS = `
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-3px); }
    20%, 40%, 60%, 80% { transform: translateX(3px); }
}
`;

// Inject CSS
const style = document.createElement('style');
style.textContent = shakeCSS;
document.head.appendChild(style);

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    new GameSimulator();
    
    // Add some visual flair
    const title = document.querySelector('.game-title');
    if (title) {
        title.addEventListener('click', () => {
            UIEffects.addGlowEffect(title, 2000);
        });
    }
    
    // Add hover effects to cards
    const cards = document.querySelectorAll('.stat-card, .character-card, .tech-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            UIEffects.addGlowEffect(card, 500);
        });
    });
});

// Console easter egg
console.log(`
🐰 KillerBunny Adventure - Developer Console 🐰

Welcome to the developer console! Here are some fun commands you can try:
- game.gameState           // View current game state
- game.addOutput('text')   // Add custom output to terminal
- game.resetGame()         // Reset the game
- UIEffects.shakeElement(document.querySelector('.game-title'))

The game demonstrates full-stack development capabilities including:
✅ Object-oriented JavaScript
✅ DOM manipulation
✅ Event handling
✅ CSS animations
✅ Responsive design
✅ Game state management

Created with ❤️ by AI Coding Agent
`);

// Make game accessible in console for debugging
window.game = null;
document.addEventListener('DOMContentLoaded', () => {
    window.game = document.gameSimulator;
});