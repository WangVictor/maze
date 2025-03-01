'''
    example.py

    Some examples of creating mazes, running games and collecting statistics.
'''

import sys
import time

from collections import defaultdict

from maze import Maze, Game, game_repeater
from goodies import RandomGreedyGoody
from baddies import RandomBaddy


EXAMPLE_MAZE = Maze(10, 10, "0001010000"
                            "0111010101"
                            "0100000011"
                            "0110100010"
                            "0000100110"
                            "1111100000"
                            "0000001000"
                            "1000111010"
                            "0010001010"
                            "1100101010")

def text_example():
    ''' Prints the state of the game to stdout after each round of turns '''

    goody0 = RandomGoody()
    goody1 = RandomGoody()
    baddy = RandomBaddy()

    game = Game(EXAMPLE_MAZE * (2, 2), goody0, goody1, baddy)

    def hook(game):
        print(game, "\n")
        time.sleep(0.1)  # Max speed of 10 updates per second

    game.play(hook=hook)

def stats_example(total_games):
    ''' Plays many games, printing cumulative and final stats '''

    results = defaultdict(int)
    for game_number, game in enumerate(game_repeater(EXAMPLE_MAZE, RandomGoody, RandomGoody, RandomBaddy)):
        if game_number == total_games:
            break
        result, _rounds = game.play()
        results[result] += 1
        if game_number % 10 == 0:
            print(game_number, "/", total_games, ":", dict(results))

    print(dict(results))

if __name__ == "__main__":
    # Uncomment whichever example you want to run
    text_example()
    #stats_example(1000)
