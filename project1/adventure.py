"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""

from __future__ import annotations
import random
import json
from typing import Optional, Any
from game_entities import Location, Item, Player
from proj1_event_logger import Event, EventList

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: the ID of the location the game is currently in
        - ongoing: whether the game is still ongoing
        - unlock_location_points: number of points added to player's score when they go to a new location

    Representation Invariants:
        - # TODO add any appropriate representation invariants as needed
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed
    unlock_location_points: int

    def __init__(self, game_data_file: str, initial_location_id: int, unlock_location_points: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        self._locations, self._items = self._load_game_data(game_data_file)
        self.current_location_id = initial_location_id
        self.unlock_location_points = unlock_location_points
        self.ongoing = True  # whether the game is ongoing

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        items = []

        for item_data in data['items']:  # Go through each element associated with the 'locations' key in the file
            my_item = Item(item_data['name'], item_data['description'],
                           (item_data['start_position'], item_data['target_position']),
                           item_data['target_points'])
            items.append(my_item)
        item_name_lst = [itm.name for itm in items]  # in convenience for initializing items in each location

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location((loc_data['id'], loc_data['name']),
                                    (loc_data['brief_description'], loc_data['long_description']),
                                    loc_data['available_commands'],
                                    [])

            for item_str in loc_data["items"]:  # convert strings of item name into the actual item
                item_index = item_name_lst.index(item_str)
                location_obj.add_item(items[item_index])
            locations[loc_data['id']] = location_obj

        return locations, items

    def get_location(self, location_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        if location_id is not None:
            return self._locations[location_id]
        else:
            return self._locations[self.current_location_id]

    def add_location_command(self, location_id: int, command: str, command_id: int) -> None:
        """Add an available command to the Location associated with loc_id of self's _locations attribute."""

        self._locations[location_id].available_commands[command] = command_id

    def remove_location_command(self, location_id: int, command: str) -> None:
        """Remove a command from a desired location"""

        # TODO: Add representation invariants

        del self._locations[location_id].available_commands[command]

    def all_location_ids(self) -> list:
        """Return all available location ids in a list."""
        return list(self._locations.keys())

    def print_basic_locations(self) -> None:
        """Print all location ids and their corresponding location name (exclude special locations)"""
        location_tuples = list(self._locations.items())
        location_tuples.sort()
        for tup in location_tuples[:9]:
            print(f"Location {tup[0]}: {tup[1].name}")

    def get_item(self, target_item_name: str) -> Any:
        """Return Item object associated with the target item name, if none, return None.

        Preconditions:
        - item_name in [self._items[i].name for i in range(len(self._items))]"""

        for _ in range(len(self._items)):
            if self._items[_].name == target_item_name:
                return self._items[_]
        return None

    # puzzles and games
    def play_word_scramble(self) -> None:
        """A word scramble puzzle."""

        with open("../ex1/common-7-letter-words.txt", "r") as f:
            words = f.read().splitlines()

        word = random.choice(words)
        word_scrambled = "".join(random.sample(word, len(word)))
        hint = 0

        print("Unscramble the word: " + word_scrambled)
        player_guess = input("Enter guess (enter 1 for hint, 0 to give up): ")

        while player_guess != word and player_guess != "0" and hint != len(word):

            if player_guess == "1":
                print("The next letter is: " + word[hint])
                hint += 1
            else:
                print("Try again.")

            player_guess = input("Enter guess (enter 1 for hint, 0 to give up): ")

        if player_guess == "0" or hint == len(word):
            print("Challenge failed... The word was: " + word)
        else:
            print("You Win!")

    def shuffling_drawers_game(self, game_player: Player, target_item_name: str) -> None:
        """A shuffling drawers puzzle for retrieving an item"""
        max_guesses = 3

        print(f"The {target_item_name} is in one of the three drawers. You must guess which drawer. Reshuffling occurs "
              f"after each incorrect guess.")

        while max_guesses > 0:
            correct_guess = random.randint(1, 3)
            guess = int(input(f"Enter guess (1, 2 or 3). You have {max_guesses} chance(s): "))

            if guess == correct_guess:
                print(f"You Win! The {target_item_name} shows up. +20 points")
                game_player.score += 20
                return
            else:
                print("Wrong! Reshuffled.")
                max_guesses -= 1

        print(f"The drawers feel bad for you... the {target_item_name} reveals itself in disappointment. "
              f"+0 points")

    def lying_backpacks_game(self, game_player: Player, target_item_name: str) -> None:
        """A lying backpacks game for retrieving items"""

        print(f"You entered the messy room and found three backpacks on the floor. The {target_item_name} is in one of "
              f"the backpacks.")
        print(f"Backpack 1 was labelled with 'The {target_item_name} is in me!'")
        print(f"Backpack 2 was labelled with 'The {target_item_name} is in not in me!'")
        print(f"Backpack 3 was labelled with 'The {target_item_name} is not in Backpack 1!'")
        print("Only one of the backpacks is telling the truth. Where is the key?")

        guess = int(input("Enter guess (1, 2 or 3), you have only one chance: "))

        if guess == 2:
            print(f"You are so smart! The {target_item_name} shows up. +20 points")
            game_player.score += 20
        else:
            print(f"Haha, you're deceived by the backpacks! The {target_item_name} reveals itself in disappointment. "
                  f"+0 points")

# ==================================================================
# =================special event functions==========================


def first_event_initializer(key_items: list[str]) -> Event:
    """Initialize the first event."""

    intro = ("The submission deadline is at 4PM. You promised your friend you would get it done, but you are missing "
             "key, items: " + ', '.join(key_items) + "\nFind them before the deadline to save you grade and the project"
                                                     "!\n")

    command_intro = ("\nCOMMANDS:\nlook: to get a long description of your location\ninventory: to check items in your "
                     "inventory\nscore: to check you game score\nundo: to go back to the last event (location change or"
                     " item pick up/drop\nlog: to get game log\nquit: quit the game\n\nAt certain locations, you can "
                     "pick up items. You will also be able to drop items.\n\nCertain locations will have special "
                     "command options.")

    first_event = Event(id_num=1, description=intro + command_intro)
    return first_event


def submit_work(game_player: Player, items_to_win: list[str]) -> bool:
    """Return whether the player has all the items in items_to_win in their inventory."""

    for x in items_to_win:
        if x not in game_player.inventory_to_string():
            print("You don't have everything you need to submit!")

            return False
    return True


def ford_ford_teleport(current_game: AdventureGame) -> int:
    """Special function for Location 10: Queen's Park. Teleport the player to any location they asked for."""

    current_game.print_basic_locations()
    answer = int(input("Hey Premier Ford! Teleport me to location... (Enter desired location id)"))
    while answer not in game.all_location_ids():
        answer = int(input("Invalid Location id. Try again:"))

    return answer


def talk_with_sadia(current_game: AdventureGame, location_id: int, command: str, command_id: int) -> None:
    """Print message from Sadia."""
    print("Sadia tells you that she had found a left-behind charger after the morning lecture and that she brought it"
          "to her office! She tells you go to second floor Bahen to retrieve it.")

    current_game.add_location_command(location_id, command, command_id)


def buy_hotdog(current_game: AdventureGame, game_player: Player, game_loc_id: int) -> None:
    """Special event for buying hotdog"""

    print("You rushed to the hotdog station and took a free hotdog!")
    current_game.remove_location_command(game_loc_id, "buy hotdog")
    game_player.moves_left += 5


def buy_potion(current_game: AdventureGame, game_player: Player) -> None:
    """Special event for buying potion"""

    print("You are desperately looking for something useful at T&T, and suddenly you came across a special desk selling"
          "repairing potion - that might be helpful! There's a line up in front of the desk and there is only a few "
          "left. 'Please be quick....' you thought. Finally it's your turn and you managed to take the last bottle of "
          "potion!")

    current_game.remove_location_command(11, "buy potion")
    game_player.inventory.append(current_game.get_item("potion"))


def get_usb_drive(current_game: AdventureGame, game_player: Player, location_id: int) -> None:
    """Add USB to player's inventory if they have the key in their inventory."""

    key = current_game.get_item("key")
    if key in game_player.inventory:
        print("You unlock your friend's door and step inside.")
        current_game.lying_backpacks_game(player, "usb drive")
        current_game.get_location(location_id).add_item(current_game.get_item("usb drive"))
        current_game.remove_location_command(location_id, "get usb drive")
    else:
        print("You can't enter your friend's dorm without his key!")


def get_laptop_charger(current_game: AdventureGame, game_player: Player, location_id: int) -> None:
    """Get laptop charger by solving a puzzle"""

    print("You pushed the door and go inside the office. There are three magic drawers.")
    current_game.shuffling_drawers_game(game_player, "laptop charger")
    current_game.get_location(location_id).add_item(current_game.get_item("laptop charger"))
    current_game.remove_location_command(location_id, "get laptop charger")

# ==================================================================
# =================function for menu commands============================


def undo(current_game: AdventureGame, current_log: EventList, game_player: Player) -> None:
    """Remove the last command."""

    last_loc = current_game.get_location(current_log.last.id_num)
    last_event = current_log.last

    if last_event.item_involved:
        my_choice = last_event.description

        if "pick up" in my_choice:
            my_item_name = my_choice[my_choice.find(": ") + 2:]
            prev_item = game_player.get_inventory_item(my_item_name)

            last_loc.items.append(prev_item)
            game_player.remove_inventory_item(prev_item)

            print(f"{my_item_name} is back at Location {last_loc.id_num}: {last_loc.name}")

        elif "drop" in my_choice:
            my_item_name = my_choice[my_choice.find(": ") + 2:]
            prev_item = last_loc.get_item(my_item_name)

            last_loc.remove_item(prev_item)
            game_player.inventory.append(prev_item)

            print(f"{my_item_name} from Location {last_loc.id_num}: {last_loc.name} is back in your inventory.")

        current_log.remove_last_event()

    else:
        current_log.remove_last_event()
        current_game.current_location_id = current_log.last.id_num

        print(f"You are back at Location {game.current_location_id}: {game.get_location(game.current_location_id).name}")

    print(game_player.inventory_to_string())

# ==================================================================
# =========================main function============================


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    player = Player()
    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    necessary_items = ["laptop charger", "mug", "usb drive", "potion"]
    game = AdventureGame('game_data.json', 1, 10)  # load data, setting
    # initial location ID to 1 and unlock_location_points to 10.
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None

    # for cleaner code
    trinity2f_name = "Trinity College 2F"
    usb_drive_name = "usb drive"
    trinity_key_name = "key"
    SS_id = 2

    # beginning of the game
    game_log.add_event(first_event_initializer(necessary_items))
    print("Game Start! \nLocation 1: New College")
    print(game_log.last.description)

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        curr_location = game.get_location()
        item_involved = None

        # Display possible actions at this location
        print("\nWhat to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in curr_location.available_commands:
            print("-", action)
        # Display items available for picking up and dropping
        pick_drop = []
        for item in curr_location.items:
            choice_name = f"pick up: {item.name}"
            pick_drop.append(choice_name)
            print("-", choice_name)
        if player.inventory:
            for item in player.inventory:
                choice_name1 = f"drop: {item.name}"
                pick_drop.append(choice_name1)
                print("-", choice_name1)
        else:
            print("No drop options available.")

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in curr_location.available_commands and choice not in menu and choice not in pick_drop:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("----------")

        if choice in menu:
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            if choice == "log":
                event_lst = game_log.display_events()
                for i in range(len(event_lst) - 1):
                    loc_id = event_lst[i][0]
                    print(f"Location: {game.get_location(loc_id).name} (id: {loc_id}), you chose to {event_lst[i][1]}")
                print(f"You are currently at Location {event_lst[-1][0]}: {game.get_location(event_lst[-1][0]).name}")
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)

            elif choice == "look":
                print(curr_location.descriptions[1])

            elif choice == "inventory":
                print(player.inventory_to_string())

            elif choice == "score":
                print(player.score)

            elif choice == "undo":
                undo(game, game_log, player)

            else:  # player choice is "quit"
                print("Thanks for playing!")
            continue
        else:
            # Handle non-menu actions
            if "pick up" in choice:

                item_name = choice[choice.find(": ") + 2:]
                item = game.get_item(item_name)
                item_involved = item

                # add item to inventory
                player.inventory.append(item)

                # remove item from current location's items
                curr_location.remove_item(item)

            elif "drop" in choice:

                item_name = choice[choice.find(": ") + 2:]
                for i in range(len(player.inventory)):
                    if player.inventory[i].name == item_name:
                        item_involved = player.inventory[i]

                        # remove item from inventory and add to current location
                        curr_location.items.append(player.inventory.pop(i))  #
                        break

            elif choice == "talk to sadia":
                talk_with_sadia(current_game=game, location_id=3, command="go upstairs", command_id=30)
                item_involved = None
                game.remove_location_command(location_id=8, command="talk to sadia")

            elif choice == "get usb drive":
                get_usb_drive(game, player, 70)
                item_involved = game.get_item("usb drive")

            elif choice == "get laptop charger":
                get_laptop_charger(game, player, 30)
                item_involved = game.get_item("laptop charger")

            elif choice == "buy hotdog":
                buy_hotdog(game, player, 4)
                item_involved = game.get_item("hotdog")

            elif choice == "ford, ford, teleport":
                target = ford_ford_teleport(game)
                item_involved = None
                game.current_location_id = target

            elif choice == "put down items to submit work":
                if submit_work(player, necessary_items):
                    game.ongoing = False

            else:
                if choice == "get on the streetcar" and game.get_item("presto card") not in player.inventory:
                    print("You are not allowed to board a streetcar without a PRESTO card!")

                # for all other commands that moves player's location
                else:
                    item_involved = None
                    result = curr_location.available_commands[choice]
                    game.current_location_id = result
                    print(f"You decided to: {choice}.")

            # TODO: add target points if item is used at target position

        if item_involved:
            print(f"Item description: {item_involved.description}")

        # create the next event
        next_location = game.get_location()

        if not item_involved:  # if location changed
            if next_location.visited:
                event_description = next_location.descriptions[0]
            else:
                event_description = next_location.descriptions[1]
                next_location.visited = True
                player.score += game.unlock_location_points
        else:
            if choice in pick_drop:
                event_description = choice
            else:
                event_description = f"Completed special event '{choice}'"

        new_event = Event(id_num=next_location.id_num, description=event_description, item_involved=item_involved)
        game_log.add_event(new_event, choice)

        print("==========")
        print(f"Location {next_location.id_num}: {next_location.name}")
        print(game_log.last.description)

        # minus the player's moves left by 1
        player.moves_left -= 1

        if player.moves_left == 0:
            game.ongoing = False

    if player.moves_left == 0:
        print("\nYou ran out of moves. It's 4 PM and you missed the deadline. What will you tell your friend...")
        print("GAME OVER.")

    else:

        print("You open your laptop, plug the charger in as well as the USB drive and begin uploading your files."
              "After a while, your project is only 30% uploaded. You glance at the clock: 3:50 PM! In the remaining 10 "
              "minutes, you frantically use Reparo! on to fix your mug, wishing for luck. And it works! Your project "
              "is ready! You promptly hit 'submit' at exactly 3:59 PM and let out a long sigh of relief. Your grade is "
              "saved and your friendship is preserved. Great Work!")

        player.score += len(necessary_items) * 20

        print("YOU SUCCESSFULLY COMPLETED THE GAME. Final score: " + str(player.score))
