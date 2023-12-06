from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu


class Yourisland(location.Location):

    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = "Logan's Island"
        self.symbol = "L"
        self.visitable = True
        self.starting_location = SouthBeachWithShip(self)
        self.locations = {}
        self.locations["southbeach"] = self.starting_location
        self.locations["lagoon"] = Lagoon(self)
        self.locations["mountain"] = Mountain(self)
        self.locations["castle"] = Castle(self)
        self.locations["forest"] = Forest(self)

        self.lagoonKey = False
        self.castleKey = False
        self.treasure_found = False
        self.gameWon = False
        self.gameStart = False


    def enter(self, ship):
        print("You arrive at your Logans island")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class SouthBeachWithShip(location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "southbeach"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs['investigate'] = self
    
    def enter(self):
        print (f"\nYou arrived on the Logans Islands south beach")
        if self.main_location.gameStart == False:
          self.strangeMen()
        print('')
        print('a: investigate')
        print('b: go north')
        print('c: go east')
        print('c: go south')
        print(f'c: go west\n')

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["mountain"]
            config.the_player.go =  True
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["lagoon"] 
            config.the_player.go =  True
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["castle"]
            config.the_player.go =  True
        elif (verb == "south"):
            if self.main_location.gameWon == False:
                print("The men tell you to find their treasure")
            
            else:
              print("You returned to your ship")
              config.the_player.next_loc = config.the_player.ship
              config.the_player.visiting = False
        elif (verb == "investigate"):
            self.explore_sand()
            
        else:
            print(f'{verb} is not a valid command.')

    def explore_sand(self):
        print('You begin searching through the sand')
        if self.main_location.treasure_found == False:
            if random.random() < .50:
                print('You have found the ancient goat head but its missing its horns')
                self.unlocked_treasure()
            else:
                print('You search dilligently but do not find much. Maybe you should investigate some more.')

        elif self.main_location.treasure_found == True:
            print('You come back to the ancient goat head')
            self.unlocked_treasure()

    def unlocked_treasure(self):
        self.main_location.treasure_found = True
        if self.main_location.castleKey == True and self.main_location.lagoonKey == True:
            print('It looks like the horns in your inventory will fit. You put them on and')
            print(f'You have found what the treasure the men were looking for. \nGo back and return to your ship')
            self.main_location.gameWon = True

        elif self.main_location.lagoonKey == True or self.main_location.castleKey == True:
            print('You are half way there find the other horn')

        else:
            print('You must find the missing horns')

    def strangeMen(self):
        if self.main_location.gameStart == False:
          print(f'You meet a strange group of armed men. The men tell you that you must find their ancient treasure or else \nthey will not let you back on your boat.')
          self.main_location.gameStart = True
        
        if self.main_location.gameWon == True:
            print('The armed men drop their weapons and let you rerturn to your ship')

class Mountain(location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "mountain"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
        self.verbs["investigate"] = self

        self.eventUsed = False
        self.riddle_amount = 3

    def enter(self):
        print("You have reached the top of middle mountain. There is a great view to the rest of the island.")
        print('a: investigate')
        print('b: south')
        print(f'c: west\n')

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):#verb == "north" or verb == "west" or verb == "east" or verb == "south"
            config.the_player.next_loc = self.main_location.locations["southbeach"]
        if (verb == "west"):#verb == "north" or verb == "west" or verb == "east" or verb == "south"
            config.the_player.next_loc = self.main_location.locations["forest"]
        if (verb == "north") or (verb == "east"):
            print(f'You tried to go {verb} but theres no where to go')
        if (verb == "investigate"):
            self.handleEvent()

    def handleEvent(self):
        if random.random() < .3:
            self.rockslide()
        if (not self.eventUsed):
            print('You investigate the mountain and meet a friendly mountain goat.')
            choice = input("Would you like to feed the goat?")
            if ("yes" in choice.lower()):
                self.feedGoat()
            else:
                print("You turn away from the the goat")

        else:
            print("The goat has disappeared")

    def feedGoat(self):
        print(f"\nYou feed the mountain goat. It seems happy and shares a hint about the island's secrets.")
        print(f'He blabs about people always rearranging the decorations in his castle. And enchants everyone with max health.\n')

        self.eventUsed = True
        self.goatReward()

    def goatReward(self):
        for i in config.the_player.get_pirates():
            i.health = i.max_health

    def rockslide(self):
        print('oh no.. the pirates were hit by a rockslide')
        for pirate in config.the_player.get_pirates():
          damage_percentage = random.uniform(0.1, 0.4)  # Random damage between 10% and 40%
          damage = int(pirate.max_health * damage_percentage)
        
        print(f"{pirate.get_name()} takes {damage} damage from the rockslide.")
        
        pirate.health -= damage

class Lagoon(location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "lagoon"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
        self.verbs["investigate"] = self
        self.verbs['swim'] = self

        self.lagoonKey = False
        self.oxygen = 2

    def enter(self):
        print("You have arrived at the lagoons. There seems to be a large wildlife presence surrounding the pool of water.")
        print('a: investigate')
        print(f'b: go west\n')

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west"):#verb == "north" or verb == "west" or verb == "east" or verb == "south"
            config.the_player.next_loc = self.main_location.locations["southbeach"]
        if (verb == "east") or (verb == "south") or (verb == 'north'):
            print(f'You tried to go {verb} but theres no where to go')
        if (verb == "investigate"):
            self.handleEnviorment()
        if(verb == 'swim'):
            self.swimKey()

    def handleEnviorment(self):
        print("You notice two animals by the lagoon: a tiger and a duck.")
        print("a: Approach the tiger")
        print("b: Feed the duck")

        choice = input("Choose an option (a, b): ")

        if choice.lower() == 'a':
            self.approach_tiger()
        elif choice.lower() == 'b':
            self.feed_duck()
        else:
            print("Invalid choice. Please choose again.")

    def approach_tiger(self):
        print("You cautiously approach the tiger.")
        outcome = random.choice(["food", "attack", "interaction"])
        self.handle_animal_outcome(outcome, "tiger")

    def feed_duck(self):
        print("You decide to feed the duck.")
        outcome = random.choice(["food", "interaction"])
        self.handle_animal_outcome(outcome, "duck")

    def handle_animal_outcome(self, outcome, animal_name):
        if outcome == "food":
            print('The duck leaves you with some food it found for your travels home. The duck runs away.')
            health_gain_percentage = random.uniform(0.1, 0.2)
            for i in config.the_player.get_pirates():
                health_gain = int(i.max_health * health_gain_percentage)
                i.health = min(i.max_health, i.health + health_gain)
                print(f"{i.get_name()} eats the food and gets {health_gain} Health back")

        elif outcome == "attack":
            print(f"The {animal_name} attacks you! And runs away.")
            damage_percentage = random.uniform(0.1, 0.3)
            for pirate in config.the_player.get_pirates():
                damage = int(pirate.max_health * damage_percentage)
                pirate.health -= damage 
                print(f"{pirate.get_name()} takes {damage} attack damage from {animal_name}.")

        elif outcome == "interaction":
            print(f"You have a friendly interaction with the {animal_name}.")


    def swimKey(self):
        print("You swim down")
        self.oxygen = 2
        depth = -1
        while depth !=0:
            swim_more = input('Would you like to swim up (yes or no): ')
            if swim_more.lower() == 'no':
                self.findingKey()
                self.oxygen -= 1
                depth -= 1
                print(f'You have {self.oxygen} oxygen left.')
                print(f'depth = {depth}')

                if self.oxygen < 1:
                    self.drowning()

                elif depth == 1:
                    print('You return to the lagoon\'s land.')
                    config.the_player.next_loc = self.main_location.locations["lagoon"]
                    break

            elif swim_more.lower() == 'yes':
                print('You swim up a little')
                
                depth += 1.5
                print(f'You have {self.oxygen} oxygen left.')
                print(f'depth = {depth}')
                
                if self.oxygen < 1:
                    self.drowning()

                if depth >= 0:
                    print('You return to the lagoon')
                    config.the_player.next_loc = self.main_location.locations["lagoon"]
                    break
                        
    def drowning(self):
        drowningDamage = 10
        for pirate in config.the_player.get_pirates():
                
                pirate.health -= drowningDamage
                print(f"{pirate.get_name()} takes {drowningDamage} from drowning damage.")

                
    def findingKey(self):
        
        if random.random() < .35:
            self.keyFound = True
            print('You find a mysterious goat horn at the bottom of the lagoon.')
            #get the item
            self.main_location.lagoonKey = True
            print('The lagoon key is added to inventory')
            
        else:
            print('You search diligently but find nothing of interest.')

class Castle(location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "castle"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
        self.verbs["investigate"] = self

        self.eventUsed = False
        self.riddle_amount = 3
        self.correct_order = random.sample(["1", "2", "3"], 3)

    def enter(self):
        print("You have arrived at the castle")
        print('a: investigate')
        print('b: go north')
        print(f'c: go east\n')

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "east"):#verb == "north" or verb == "west" or verb == "east" or verb == "south"
            config.the_player.next_loc = self.main_location.locations["southbeach"]
        if (verb == "north"):#verb == "north" or verb == "west" or verb == "east" or verb == "south"
            config.the_player.next_loc = self.main_location.locations["forest"]
        if (verb == "west") or (verb == "south"):
            print(f'You tried to go {verb} but theres no where to go')
        if (verb == "investigate"):
            self.HandleEvent()

    def HandleEvent(self):
        if (not self.castleKey):
            print("You ivestigate the castle and hear mysterious sounds...")
            choice = input("Would you like to explore further?")
            if ("yes" in choice.lower()):
                #self.correct_order = random.sample(["1", "2", "3"], 3)
                self.HandleEvent()
            else:
                print("You let the castle be")

        else:
            print("The castle remains dormant.")

    def HandleEvent(self):
        print("You explore the castle courtyard, theres three pedestals with objects on them.")
        print("1. A suit of armor standing to the right.")
        print("2. A sword in the middle.")
        print("3. A potted plant on the left one.")
        print(f'\nIt looks like you must arrange them in a specific order')

        #creates a random order
        #correct_order = random.sample(["1", "2", "3"], 3)
        

        #is the players choice correct
        while not self.eventUsed:
            # choose order of the objects
            choice = input("How would you like to arrange the objects (ex: 1,2,3): ")
        
            if choice.split(",") == self.correct_order:
                print("A hidden compartment in the suit of armor reveals a mountain goat horn")
                print(f'Goat Horn Put in user Inventory\n')
                self.main_location.castleKey = True
                self.eventUsed = True
                
                
            else:
                print(f"\nYou arrange the objects, but nothing happens. Try a different order!")              
        
class Forest(location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "forest"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
        self.verbs["wonder"] = self

        self.noteFound = False
        self.wondering = False

    def enter(self):
        print("You have arrived at the forest. Theres a storm overhead")
        print('a: wonder')
        print('b: go east')
        print(f'c: go south\n')

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "east"):#verb == "north" or verb == "west" or verb == "east" or verb == "south"
            config.the_player.next_loc = self.main_location.locations["mountain"]
        if (verb == "south"):#verb == "north" or verb == "west" or verb == "east" or verb == "south"
            config.the_player.next_loc = self.main_location.locations["castle"]
        if (verb == "north") or (verb == "west"):
            print(f'You tried to go {verb} but theres no where to go')
        if (verb == "wonder"):
            self.wondering = True # you want to wonder
            self.HandleEvent()
            

    def HandleEvent(self):
        while self.wondering and not self.noteFound:#if you still want to wonder but you have not found the note
            print("You investigate the forest and...")
            self.fallingTree()

            if random.random() < .43:
                self.findNote()

            self.ask_to_continue_wondering()
        
        if not self.wondering:
            print("It looks like you explored the whole forest and cant really wonder anymore")


    
    def fallingTree(self):
        if random.choice([True, False]):
            damage_percentage = random.uniform(0.1, 0.5) #Random damage between 10% and 50%
            for pirate in config.the_player.get_pirates():
                damage = int(pirate.max_health * damage_percentage)
                pirate.health -= damage 
                print(f"A tree falls! {pirate.get_name()} takes {damage} damage.")
        else:
            print('A tree crashes besides you.')

    def findNote(self):
        print("You find a weathered note on the forest floor.")
        print(f"The note hints at having to 'swim' to the bottom of water.\n")

        self.noteFound = True  

    def ask_to_continue_wondering(self):
        self.wonder_question = input('Would you like to continue wondering? (yes/no): ')

        if self.wonder_question.lower() == 'no':
            self.wondering = False
        else:
            self.HandleEvent()