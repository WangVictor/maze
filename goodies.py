'''
    goodies.py

    Definitions for some example goodies
'''

import random

from maze import Goody, Baddy, Position, UP, DOWN, LEFT, RIGHT, STAY, STEP, PING

class StaticGoody(Goody):
    ''' A static goody - does not move from its initial position '''

    def take_turn(self, _obstruction, _ping_response):
        ''' Stay where we are '''
        return STAY

class RandomGoody(Goody):
    ''' A random-walking goody '''

    def take_turn(self, obstruction, _ping_response):
        ''' Ignore any ping information, just choose a random direction to walk in, or ping '''
        possibilities = [PING]
        for direction in [UP, DOWN, LEFT, RIGHT]: # STEP.keys()
            if not obstruction[direction]:
                possibilities.append(direction)
        return random.choice(possibilities)

class GreedyGoody(Goody):
    ''' A goddy that pings once and then walks towards the other goody.  '''

    last_ping_response = None

    def vector_len_2(self, vector):
        return (vector.x * vector.x) + (vector.y * vector.y)

    def take_turn(self, obstruction, ping_response):
        ''' Ignore any ping information, just choose a random direction to walk in, or ping '''
        if ping_response is not None:
            self.last_ping_response = ping_response

        if self.last_ping_response is None:
            # If we don't know where the other goody is, then send a ping so that we can find out.
            print("Pinging to find our friend and foe")
            return PING

        friend, = [player for player in self.last_ping_response.keys()
                   if isinstance(player, Goody) and player is not self]
        foe, = [player for player in self.last_ping_response.keys() if isinstance(player, Baddy)]

        # For the four possible moves, find the resulting distance to our friend after each one:
        last_known_friend_position = self.last_ping_response[friend]
        len_and_dirs = []
 
        for direction in [UP, DOWN, LEFT, RIGHT]: # STEP.keys()
            # Choose the one that takes us closest to the our friend
            if not obstruction[direction]:
                # STEP[direction] turns the direction label into a vector (dx, dy) which we can add 
                # to a Position (another vector):
                new_vector = last_known_friend_position - STEP[direction]
                entry = [direction, new_vector, self.vector_len_2(new_vector)]
                len_and_dirs.append(entry)
        
        len_and_dirs.sort(key=lambda len_and_dir: len_and_dir[2])
        print(len_and_dirs)
        
        return len_and_dirs[0][0]

class MemoryGreedyGoody(Goody):
    ''' A goddy that pings once and then walks towards the other goody.  '''

    last_ping_response = None
    last_action = None
    stuckpoints = []

    def vector_len_2(self, vector):
        return (vector.x * vector.x) + (vector.y * vector.y)

    def take_turn(self, obstruction, ping_response):
        ''' Ignore any ping information, just choose a random direction to walk in, or ping '''
	
        if ping_response is not None:
            self.last_ping_response = ping_response

        if self.last_ping_response is None:
            # If we don't know where the other goody is, then send a ping so that we can find out.
            print("Pinging to find our friend and foe")
            return PING

        friend, = [player for player in self.last_ping_response.keys()
                   if isinstance(player, Goody) and player is not self]
        foe, = [player for player in self.last_ping_response.keys() if isinstance(player, Baddy)]

        # For the four possible moves, find the resulting distance to our friend after each one:
        last_known_friend_position = self.last_ping_response[friend]
        len_and_dirs = []
 
        for direction in [UP, DOWN, LEFT, RIGHT]: # STEP.keys()
            # Choose the one that takes us closest to the our friend
            if not obstruction[direction]:
                # STEP[direction] turns the direction label into a vector (dx, dy) which we can add 
                # to a Position (another vector):
                new_vector = last_known_friend_position - STEP[direction]
                stuck = True
                if len(self.stuckpoints) == 0:
                    stuck = False
                for point in self.stuckpoints:
                    stuck = (stuck * (new_vector.x == point.x) * (new_vector.y == point.y))
                if stuck:
                    print('I remember I got stuck :(')
                else:
                    entry = [direction, new_vector, self.vector_len_2(new_vector)]
                    len_and_dirs.append(entry)
        
        len_and_dirs.sort(key=lambda len_and_dir: len_and_dir[2])
        if len(len_and_dirs) == 0:
            action = UP
        else:
            action = len_and_dirs[0][0]
        if self.last_action is not None:
            if (STEP[action].x == - STEP[self.last_action].x) * (STEP[action].y == - STEP[self.last_action].y) :
                self.stuckpoints.append(last_known_friend_position)
                print('I got stuck :(')

        self.last_action = action
        print(len_and_dirs)
        
        return action

class RandomGreedyGoody(Goody):
    ''' A goddy that pings once and then walks towards the other goody.  '''

    last_ping_response = None

    def vector_len_2(self, vector):
        return (vector.x * vector.x) + (vector.y * vector.y)

    def take_turn(self, obstruction, ping_response):
        ''' Ignore any ping information, just choose a random direction to walk in, or ping '''
        if ping_response is not None:
            self.last_ping_response = ping_response

        if self.last_ping_response is None:
            # If we don't know where the other goody is, then send a ping so that we can find out.
            print("Pinging to find our friend and foe")
            return PING

        friend, = [player for player in self.last_ping_response.keys()
                   if isinstance(player, Goody) and player is not self]
        foe, = [player for player in self.last_ping_response.keys() if isinstance(player, Baddy)]

        # For the four possible moves, find the resulting distance to our friend after each one:
        last_known_friend_position = self.last_ping_response[friend]
        len_and_dirs = []
 
        for direction in [UP, DOWN, LEFT, RIGHT]: # STEP.keys()
            # Choose the one that takes us closest to the our friend
            if not obstruction[direction]:
                # STEP[direction] turns the direction label into a vector (dx, dy) which we can add 
                # to a Position (another vector):
                new_vector = last_known_friend_position - STEP[direction]
                entry = [direction, new_vector, self.vector_len_2(new_vector)]
                len_and_dirs.append(entry)
        
        len_and_dirs.sort(key=lambda len_and_dir: len_and_dir[2])
        print(len_and_dirs)
        possibilities = [PING]
        for i in range(len(len_and_dirs)):
            for j in range(len(len_and_dirs) - i):
                possibilities.append(len_and_dirs[i][0])
        return random.choice(possibilities)
