
"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    # TODO: Copy/paste your code from ex1_simulation below, and make adjustments as needed
    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str],
                 unlock_location_points: int) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id, unlock_location_points)

        # TODO: Add first event (initial location, no previous command)
        initial_location = self._game.get_location()
        initial_location_id_desc = initial_location.descriptions[1]
        first_event = Event(id_num=initial_location_id,
                            description=initial_location_id_desc)

        # TODO: Generate the remaining events based on the commands and initial location
        # Hint: Call self.generate_events with the appropriate arguments
        self._events.add_event(event=first_event, command=None)

        self.generate_events(commands=commands, current_location=initial_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        # TODO: Complete this method as specified. For each command, generate the event and add
        #  it to self._events.
        # Hint: current_location.available_commands[command] will return the next location ID
        # which executing <command> while in <current_location_id> leads to

        for command in commands:
            next_location_id = current_location.available_commands[command]
            next_location_id_desc = self._game.get_location(next_location_id).descriptions[1]

            next_event = Event(id_num=next_location_id,
                               description=next_location_id_desc)
            self._events.add_event(event=next_event, command=command)

            current_location = self._game.get_location(next_location_id)

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east"])
        >>> sim.get_id_log()
        [1, 2]

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east", "go east", "buy coffee"])
        >>> sim.get_id_log()
        [1, 2, 3, 3]
        """

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    # A list of all the commands needed to walk through our game to win it
    win_walkthrough = ["go east", "go upstairs", "pick up: key", "go downstairs", "go east", "go east",
                       "talk to sadia", "go north", "go to dorm", "get usb drive", "2", "pick up: usb drive",
                       "go downstairs", "go south", "go south", "pick up: mug", "go west", "go west",
                       "go upstairs", "get laptop charger", "1", "1", "1", "pick up: laptop charger",
                       "go downstairs", "go east", "go south", "pick up: presto card", "get on the streetcar",
                       "buy potion", "go back to campus", "go north", "go west", "go north", "go west",
                       "put down items to submit work"]

    # Log list of IDs of all locations that would be visited
    expected_log = [1, 2, 20, 20, 2, 4, 8, 8, 7, 70, 70, 70, 7, 8, 9, 9, 5, 3, 30, 30, 30, 3, 5, 6, 6, 11, 11, 6, 5,
                    3, 2, 1]

    # Uncomment the line below to test your walkthrough
    assert expected_log == AdventureGameSimulation('game_data.json', 1, win_walkthrough, 10)

    # A list of all the commands needed to walk through our game to reach a 'game over' state
    lose_demo = ["go east", "go east", "go east", "go north", "go south", "go west", "go west", "go west",
                 "go east", "go east" "go east", "go north", "go south", "go west", "go west", "go west",
                 "go east", "go east" "go east", "go north", "go south", "go west", "go west", "go west",
                 "go east", "go east" "go east", "go north", "go south", "go west", "go west", "go west",
                 "go east", "go east" "go east", "go north", "go south", "go west", "go west", "go west",
                 "go east", "go east" "go east", "go north", "go south", "go west", "go west", "go west",
                 "go east", "go east"]

    # Log list of IDs of all locations that would be visited
    expected_log = [2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4]

    # Uncomment the line below to test your demo
    assert expected_log == AdventureGameSimulation('game_data.json', 1, lose_demo, 10)

    # TODO: Add code below to provide walkthroughs that show off certain features of the game
    # TODO: Create a list of commands involving visiting locations, picking up items, and then
    #   checking the inventory, your list must include the "inventory" command at least once
    #TODO: ADD SIMPLE PUZZLE WALKTHROUGH COMMANDS
    inventory_demo = ["go east", "go upstairs", "sneak in and out", "go downstairs", "go east", "go east",
                      "talk with Sadia", "go north", "go to your friend's dorm", "go downstairs", "go south",
                      "go south", "pick up broken mug pieces (Ouch!)", "go west", "go west", "go to Sadia's office",
                      "take charger", "go downstairs", "go north", "go west", "inventory", "quit"]

    expected_log = [2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2]

    assert expected_log == AdventureGameSimulation('game_data.json', 1, inventory_demo, 10)

    scores_demo = ["go east", "go upstairs", "sneak in and out", "go downstairs", "go east", "go east",
                   "talk with Sadia", "go north", "go to your friend's dorm", "go downstairs", "go south",
                   "go south", "pick up broken mug pieces (Ouch!)", "go west", "go west", "go to Sadia's office",
                   "take charger", "go downstairs", "go north", "go west", "score", "quit"]

    expected_log = [2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2, 4, 8, 7, 8, 4, 2, 1,
                    2]

    assert expected_log == AdventureGameSimulation('game_data.json', 1, scores_demo, 10)

    teleportation_demo = ["go east", "go east", "go east", "go under the bridge", "Ford, Ford, Teleport", "Quit"]

    # TODO: Make it so the demo teleports to NC

    expected_log = [2, 4, 8, 10, 1]

    assert expected_log == AdventureGameSimulation('game_data.json', 1, teleportation_demo, 10)

    # Note: You can add more code below for your own testing purposes
