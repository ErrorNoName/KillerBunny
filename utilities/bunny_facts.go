package main

import (
	"fmt"
	"math/rand"
	"os"
	"strings"
	"time"
)

// BunnyFact represents an interesting fact about rabbits
type BunnyFact struct {
	Category string
	Fact     string
	Fun      bool
}

// BunnyFactsDatabase contains interesting facts about rabbits
type BunnyFactsDatabase struct {
	facts []BunnyFact
}

// NewBunnyFactsDatabase creates and initializes the facts database
func NewBunnyFactsDatabase() *BunnyFactsDatabase {
	db := &BunnyFactsDatabase{
		facts: []BunnyFact{
			{Category: "Physical", Fact: "Rabbits can see nearly 360 degrees around them", Fun: true},
			{Category: "Physical", Fact: "A rabbit's teeth never stop growing throughout their life", Fun: false},
			{Category: "Behavior", Fact: "Rabbits can jump up to 3 feet high and 10 feet long", Fun: true},
			{Category: "Behavior", Fact: "Baby rabbits are called kits or bunnies", Fun: true},
			{Category: "Biology", Fact: "Rabbits have 28 teeth", Fun: false},
			{Category: "Biology", Fact: "A rabbit's heart can beat up to 325 times per minute", Fun: false},
			{Category: "Social", Fact: "Rabbits live in groups called colonies", Fun: false},
			{Category: "Physical", Fact: "Rabbits can't vomit due to their digestive system", Fun: false},
			{Category: "Behavior", Fact: "Rabbits purr when they're happy, similar to cats", Fun: true},
			{Category: "Physical", Fact: "Rabbit ears can be up to 10 cm (4 inches) long", Fun: false},
			{Category: "Behavior", Fact: "Rabbits can be trained to use a litter box", Fun: true},
			{Category: "Biology", Fact: "Rabbits have excellent hearing and can detect sounds from 2 miles away", Fun: false},
			{Category: "Legendary", Fact: "The Killer Bunny of Caerbannog once defeated an entire army of knights", Fun: true},
			{Category: "Legendary", Fact: "Some rabbits are said to guard ancient treasures", Fun: true},
			{Category: "Legendary", Fact: "In medieval times, rabbits were symbols of fertility and rebirth", Fun: false},
			{Category: "Fun", Fact: "A group of baby rabbits is called a litter", Fun: true},
			{Category: "Fun", Fact: "Rabbits can recognize their names and come when called", Fun: true},
			{Category: "Fun", Fact: "The world's longest rabbit ears measured 79 cm (31.1 inches)", Fun: true},
		},
	}
	return db
}

// GetRandomFact returns a random fact from the database
func (db *BunnyFactsDatabase) GetRandomFact() BunnyFact {
	return db.facts[rand.Intn(len(db.facts))]
}

// GetFactsByCategory returns all facts in a specific category
func (db *BunnyFactsDatabase) GetFactsByCategory(category string) []BunnyFact {
	var result []BunnyFact
	for _, fact := range db.facts {
		if strings.EqualFold(fact.Category, category) {
			result = append(result, fact)
		}
	}
	return result
}

// GetFunFacts returns only the fun facts
func (db *BunnyFactsDatabase) GetFunFacts() []BunnyFact {
	var result []BunnyFact
	for _, fact := range db.facts {
		if fact.Fun {
			result = append(result, fact)
		}
	}
	return result
}

// GetAllCategories returns a list of all available categories
func (db *BunnyFactsDatabase) GetAllCategories() []string {
	categoryMap := make(map[string]bool)
	for _, fact := range db.facts {
		categoryMap[fact.Category] = true
	}
	
	var categories []string
	for category := range categoryMap {
		categories = append(categories, category)
	}
	return categories
}

// GetFactCount returns the total number of facts
func (db *BunnyFactsDatabase) GetFactCount() int {
	return len(db.facts)
}

// BunnyStatsCalculator provides statistics about bunnies
type BunnyStatsCalculator struct{}

// CalculateJumpDistance calculates theoretical jump distance based on size
func (calc *BunnyStatsCalculator) CalculateJumpDistance(sizeCategory string) float64 {
	switch strings.ToLower(sizeCategory) {
	case "small":
		return 6.0 // feet
	case "medium":
		return 8.5
	case "large":
		return 10.0
	case "killer":
		return 15.0 // The legendary killer bunny
	default:
		return 8.0
	}
}

// EstimateLifespan estimates bunny lifespan based on environment
func (calc *BunnyStatsCalculator) EstimateLifespan(environment string) string {
	switch strings.ToLower(environment) {
	case "wild":
		return "1-2 years"
	case "domestic":
		return "8-12 years"
	case "legendary":
		return "Immortal (until defeated by a brave knight)"
	default:
		return "5-8 years"
	}
}

// formatFact formats a fact for display
func formatFact(fact BunnyFact) string {
	funIndicator := ""
	if fact.Fun {
		funIndicator = " 🎉"
	}
	return fmt.Sprintf("📚 [%s]%s %s", fact.Category, funIndicator, fact.Fact)
}

// displayBanner displays a decorative banner
func displayBanner(title string) {
	border := strings.Repeat("=", 60)
	fmt.Println(border)
	fmt.Printf("🐰 %s 🐰\n", strings.ToUpper(title))
	fmt.Println(border)
}

// displayFactsTable displays facts in a formatted table
func displayFactsTable(facts []BunnyFact) {
	if len(facts) == 0 {
		fmt.Println("No facts found in this category.")
		return
	}
	
	fmt.Printf("Found %d fact(s):\n\n", len(facts))
	for i, fact := range facts {
		fmt.Printf("%d. %s\n", i+1, formatFact(fact))
	}
}

// main function
func main() {
	// Seed random number generator
	rand.Seed(time.Now().UnixNano())
	
	// Initialize database and calculator
	db := NewBunnyFactsDatabase()
	calc := &BunnyStatsCalculator{}
	
	// Check command line arguments
	if len(os.Args) > 1 {
		command := strings.ToLower(os.Args[1])
		
		switch command {
		case "random":
			fmt.Println("🎲 Random Bunny Fact:")
			fact := db.GetRandomFact()
			fmt.Println(formatFact(fact))
			
		case "fun":
			displayBanner("Fun Bunny Facts")
			facts := db.GetFunFacts()
			displayFactsTable(facts)
			
		case "category":
			if len(os.Args) > 2 {
				category := os.Args[2]
				displayBanner(fmt.Sprintf("Facts: %s", category))
				facts := db.GetFactsByCategory(category)
				displayFactsTable(facts)
			} else {
				fmt.Println("Available categories:")
				categories := db.GetAllCategories()
				for _, cat := range categories {
					fmt.Printf("  - %s\n", cat)
				}
			}
			
		case "stats":
			displayBanner("Bunny Statistics Calculator")
			fmt.Println("Jump distances by size:")
			sizes := []string{"small", "medium", "large", "killer"}
			for _, size := range sizes {
				distance := calc.CalculateJumpDistance(size)
				fmt.Printf("  %s: %.1f feet\n", strings.Title(size), distance)
			}
			
			fmt.Println("\nLifespan by environment:")
			environments := []string{"wild", "domestic", "legendary"}
			for _, env := range environments {
				lifespan := calc.EstimateLifespan(env)
				fmt.Printf("  %s: %s\n", strings.Title(env), lifespan)
			}
			
		case "all":
			displayBanner("All Bunny Facts")
			displayFactsTable(db.facts)
			
		case "count":
			fmt.Printf("📊 Total facts in database: %d\n", db.GetFactCount())
			
		case "help":
			displayHelp()
			
		default:
			fmt.Printf("Unknown command: %s\n", command)
			displayHelp()
		}
	} else {
		// Interactive mode - display a sample of capabilities
		displayBanner("Bunny Facts Database")
		fmt.Println("🐰 Welcome to the Bunny Facts Database!")
		fmt.Println("This Go program demonstrates:")
		fmt.Println("  • Struct and interface usage")
		fmt.Println("  • Data management and filtering")
		fmt.Println("  • Command-line argument parsing")
		fmt.Println("  • Random number generation")
		fmt.Println("  • String manipulation")
		fmt.Println()
		
		// Show some sample data
		fmt.Println("🎲 Here's a random fact:")
		fact := db.GetRandomFact()
		fmt.Println(formatFact(fact))
		fmt.Println()
		
		fmt.Printf("📊 Database contains %d facts across %d categories\n", 
			db.GetFactCount(), len(db.GetAllCategories()))
		fmt.Println()
		
		fmt.Println("For more options, run with 'help' argument!")
	}
}

// displayHelp shows usage information
func displayHelp() {
	fmt.Println("Bunny Facts Database - Usage:")
	fmt.Println("  go run bunny_facts.go [command]")
	fmt.Println()
	fmt.Println("Available commands:")
	fmt.Println("  random     - Show a random fact")
	fmt.Println("  fun        - Show only fun facts")
	fmt.Println("  category <name> - Show facts by category")
	fmt.Println("  stats      - Show bunny statistics")
	fmt.Println("  all        - Show all facts")
	fmt.Println("  count      - Show total fact count")
	fmt.Println("  help       - Show this help message")
	fmt.Println()
	fmt.Println("Examples:")
	fmt.Println("  go run bunny_facts.go random")
	fmt.Println("  go run bunny_facts.go category Physical")
	fmt.Println("  go run bunny_facts.go fun")
}