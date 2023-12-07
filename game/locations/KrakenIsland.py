from game import location
import game.config as config
from game.display import announce
import random
from re import I
import game.ship as ship
import game.crewmate as crewmate
from game.context import Context
import jsonpickle
import game.items as items
import sys
import datetime

class KrakenIsland (location.Location):

    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = "Island of the Kraken"
        self.symbol = "y"
        self.visitable = True
        self.starting_location = BeachWithShip(self)
        self.locations = {}

        self.locations["South Beach"] = self.starting_location
        self.locations["Lair Gate"] = LairGate(self)
        self.locations["Mountain"] = Mountain(self)
        self.locations["Kraken Skull"] = Skull(self)
        self.locations["Kraken"] = Kraken(self)

    def enter(self, ship):
        announce ("You arrive at the Island of the Kraken ")   
        
    
    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()


class BeachWithShip (location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "South Beath"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self

    def enter(self):
        announce ("Welcome to the South Beach of the Island of the Kraken ")
        announce ("You may explore in any direction. South goes back to the ship")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Lair Gate"]
            config.the_player.go =  True
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Mountain"]
            config.the_player.go = True
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["Kraken Skull"]
            config.the_player.go = True
        if (verb == "south"):
            announce ("You returned to your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        

class LairGate (location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Lair Gate"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
        self.verbs["investigate"] = self
        self.verbs ["lair"] = self

        self.eventUsed = False
        self.riddle_amount = 5

    def enter(self):
        announce ("You climb around some rocks and find a gate to a large cave")
        

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["South Beach"]
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["Kraken Skull"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Mountain"]
        if (verb == "investigate"):
            self.HandleEvent()
        if (verb == "lair"):
            config.the_player.next_loc = self.main_location.locations["Kraken"]

    def HandleEvent(self):
        if (not self.eventUsed):
            announce ("You investigate the gate and find a three number lock that opens the gate.")
            announce ("As you look at the lock, a parrot lands on the bars and shouts out the number 1 ")
            announce ("There are 3 numbers hidden on the island that help you solve\nWithout those numbers this puzzle is impossible!")
            choice = input("Would you like to guess the code? ")
            if ("yes" in choice.lower()):
                self.HandleRiddles()
            else:
                announce ("You turn away from the gate")

        else:
            announce ("The gate lays waiting for the code")

    def HandleRiddles(self):
        riddle = self.GetRiddleAnswer()
        guesses = self.riddle_amount

        while (guesses > 0):

            print(riddle[0])
            plural = ""
            if (guesses != 1):
                plural = "s"

            print(f"You have {guesses} left")
            choice = input ("What is your guess? ")

            if riddle == choice:
                announce ("You have guessed correctly and opened the gate!")
                guesses = 0
                self.openLairGate()
            else:
                guesses -= 1
                announce ("You have guessed incorrectly, try again and make sure you have all three numbers!")


    def GetRiddleAnswer(self):
        return "716"
    
    def openLairGate(self):
        enterLair = input ("Would you like to enter the Lair? Type go after saying yes. ")
        if enterLair.lower() == 'yes':
            self.go = True
            config.the_player.next_loc = self.main_location.locations["Kraken"]
        else:
            announce ("You stay waiting at the gair of the Lair ")

class Kraken (location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Kraken"
        self.verbs["sneak"] = self
        self.verbs["attack"] = self
        self.verbs["right"] = self
        self.verbs["left"] = self
        self.verbs["back"] = self
        self.verbs["south"] = self
        self.verbs["up"] = self
        self.verbs["down"] = self


        
    def enter(self):
        announce ("You walk a ways into the Lair and find a giant Kraken that appears to be sleeping. ")
        announce ("Your options are to attack or try to sneak around it.")
        

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "sneak"):
            self.krakenSneak()
        if (verb == "attack"):
            self.krakenAttack()
        if (verb == "left"):
            self.krakenLairExit()
        if (verb == "right"):
            self.krakenFinalEscape()
        if (verb == "back" or "south"):
            config.the_player.next_loc = self.main_location.locations["South Beach"]
        if (verb == "up"):
            self.ladderUp()
        if (verb == "down"):
            self.ladderDown()

        

    def krakenSneak(self):
        announce ("You try to sneak around the Kraken and accidentally step on its tentacle")
        self.krakenEscape()

    def krakenAttack(self):
        announce ("As you aim your attack, the Kraken awakens! ")
        self.krakenEscape()

    def krakenEscape(self):
        announce("You need to run away from the Kraken, you can go left or right! ")

    def krakenLairExit(self):
        announce ("You have escaped the Lair! ")
        announce ("You can now go back to the South Beach! ")

    def krakenFinalEscape(self):
        announce ("You come to an intersection, a ladder going up or down! ")
        announce ("Going down leads to treasure but you may get trapped, going up leads you out of the Lair")

    def ladderUp(self):
        announce ("You have climbed the ladder and can now see light!")
        self.krakenLairExit()

    def ladderDown(self):
        announce ("You reach the bottom on the ladder and find the treasure that gives you maximum health")
        announce ("In order to escape in time and get the treasure you must the numbers found on the island in increasing order")
        combo = self.escapeCombo()
        escapenumber = input ("What is the code? ")
        if (escapenumber == combo):
            announce ("You have guessed correctly, earned maximum health, and climbed the ladder in time! ")
            for i in config.the_player.get_pirates():
                i.health = i.max_health
            self.krakenLairExit()
        else: 
            self.failedComboExit()

    def failedComboExit(self):
        announce ("You have guessed the code incorrectly and left without the treasure but luckily you make it out alive. ")
        self.krakenLairExit()
        


            
    def escapeCombo(self):
        return "167"




class Mountain (location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Mountain"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
        self.verbs["investigate"] = self

    def enter(self):
        announce ("You walk along the beach and come to the base of a rather large mountain.")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["South Beach"]
        if (verb == "west"):
            announce ("This way leads you straight to open water, chose a different direction! ")
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Lair Gate"]
        if (verb == "south"):
            announce ("You returned to your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "investigate"):
            self.handleMountain()

    def handleMountain(self):
        announce ("You investigate the base of the mountain and find a narrow path up the mountain")
        climb = input ("Would you like to climb the mountain? ")
        if climb.lower() == 'yes':
            self.mountainTop()
        else:
            announce ("You decide not to climb the mountain and remain at the base")

    def mountainTop(self):
        announce ("You arrive at the top of the mountain")
        announce ("In the distance you can see the gate to a large cave that is north of you")
        announce ("You see a parrot land next to you and it shouts out the number 7 ")

class Skull (location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Kraken Skull"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
        self.verbs["investigate"] = self

    def enter(self):
        announce ("While walking along the shoreline you step on what seems to be a rock.")
        announce ("It turns out to be the skull of a Kraken.")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["South Beach"]
        if (verb == "east"):
            announce ("This way leads you straight to open water, chose a different direction! ")
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Lair Gate"]
        if (verb == "south"):
            announce ("You returned to your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == "investigate"):
            self.handleSkull()

    def handleSkull(self):
        announce ("You pick up the skull and realize that it is not very old")
        dig = input ("Would you like to dig to find more of the skeleton? ")
        if dig.lower() == 'yes':
            self.digSkull()
        else:
            announce ("You decide you do not want to take the time to dig up the skeleton ")

    def digSkull(self):
        announce ("You spend hours digging up the skeleton and it turns out to be nearly 50 feet!")
        announce ("As you finish digging a parrot flys next to you and shouts the number 6 ")


        


