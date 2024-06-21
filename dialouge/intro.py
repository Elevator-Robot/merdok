"""Game Introduction Module"""

def shun_player():
    print("Cowardice does not become you. The world has no place for those who shirk from destiny. Begone, and let the true heroes forge their path without you.")
    # Terminate the program
    import sys
    sys.exit(0)  # or return some appropriate error code

def introduction():
    print("In a realm where the scorching fury of embers clashes with the piercing chill of ice, a land stands divided. The ashes of once-great kingdoms lay scattered, whispering tales of heroism and ruin. As the shadows of the past linger and the fate of the world hangs by a thread, a new hero must rise to challenge the encroaching darkness.\n")
    print("Welcome to Endless Ashes of Ember and Ice.\n")
    print("Will you stand against the tide of destruction, braving fire and frost to restore balance to this shattered land? Will you embark on a quest that will test your courage, wits, and willpower to their very limits?\n")
    response = input("Are you ready for the quest, brave soul?\nType 'yes' to accept your destiny or 'no' to turn away: ").lower()

    if response.lower().strip() == "yes":
        player_name = input("Enter your name, hero: ")
        print(f"\nWelcome, {player_name}! Your journey begins now. May the gods watch over you as you face the trials that await...")
    else:
        shun_player()


introduction()