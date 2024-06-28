"""Game Introduction Module"""
from characters.inventory import PlayerInventory

class GameIntroduction:
    def __init__(self):
        self.player_name = ""
        self.player_inventory = PlayerInventory()

    def set_weapon(self):
        while True:
            weapon_choice = input("""
                                \nChoose your weapon:
                                \n 1: sword
                                \n 2: axe
                                \n 3: bow
                                \n 4: staff
                                \n Enter number:""").lower().strip()
            match weapon_choice:
                case "1":
                    self.player_inventory.add_weapon("sword", damage=4)
                    print("\nYou feel the weight of the sword in your hand, the blade gleaming in the torchlight. +4 strength has been added to your stats.")
                    break
                case "2":
                    self.player_inventory.add_weapon("axe", damage=4)
                    print("\nYou feel the weight of the axe in your hand, the blade gleaming in the torchlight. +4 strength has been added to your stats.")
                    break
                case "3":
                    self.player_inventory.add_weapon("bow", damage=4)
                    print("\nYou feel the tension of the bowstring as you draw it back, the arrow poised to strike. +4 strength has been added to your stats.")
                    break
                case "4":
                    self.player_inventory.add_weapon("staff", damage=4)
                    print("\nYou feel the power of the staff coursing through your veins, the magic within it waiting to be unleashed. +2 intellegence has been added to your stats.")
                    break
                case _:
                    print("\nThat is not a valid weapon choice. Choose again.")
                    continue

    def start_introduction(self):
        print("\nThe first thing you notice as you regain consciousness is the cold, unyielding stone beneath you. The air is thick with the scent of dust and decay, and the only sound is the distant echo of your own heartbeat.")
        print("\nYou open your eyes to find yourself in a dimly lit chamber, the walls lined with ancient runes and symbols that seem to pulse with an otherworldly energy. As you struggle to your feet, you realize that you have no memory of how you came to be here, or even who you are.")
        print("\nAn angry voice yells in the darkness, 'Take that prisoner to the arena where he shall be masecured in front of our people.'")
        print("\nYou feel a surge of panic as you realize that you are not alone. A group of shadowy figures surrounds you, their faces obscured by hoods and masks. You try to speak, but your voice catches in your throat.")
        print("\nOne of the figures steps forward, a glint of malice in their eyes. 'You have been chosen, mortal. Chosen to face the trials of the arena, to prove your worth in the eyes of the gods.'")
        print("\n'You may choose 1 weapon to try and salvage your life... Choose wisely.'")

        self.set_weapon()

        print("\nAhh, the prisoner has chosen his weapon. Very well, let us proceed to the arena where your fate shall be decided.")
        print("\nYou are dragged through a series of winding corridors, the torchlight flickering off the ancient stones. The air grows colder with each step, and the sense of foreboding in your chest deepens.")
        print("\nFinally, you emerge into a vast, circular chamber, the walls lined with towering statues and the floor covered in sand and bloodstains. The crowd roars as you are led to the center of the arena, the sound echoing in your ears like thunder.")
        print("\nYou steel yourself for the battle to come, your heart pounding in your chest. The figure who spoke before steps forward once more, their voice ringing out over the crowd.")
        print("\n'Let the battle begin!'")
