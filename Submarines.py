import numpy as np
from random import randint
from enum import Enum


class Signal(Enum):
    Already_Destroyed = -2
    Already_Hit = -1
    Miss = 0
    Hit = 1
    Destroyed = 2
    Won = 3


class Board:
    """ This class is the board each player gets """
    def __init__(self, board_size: tuple, vessel_numbers: tuple):
        self.board_size = board_size
        self.board_array = np.array(board_size)
        self.vessels = []
        self.create_vessels(vessel_numbers)

    def create_vessels(self, vessel_numbers: tuple):
        vessel_number = 0
        for level in vessel_numbers:
            for vessel in range(1,vessel_numbers(level)):
                vessel_number += 1
                if level == 0:
                    new_vessel = Submarine(vessel_number)
                if level == 1:
                    new_vessel = Destroyer(vessel_number)
                if level == 2:
                    new_vessel = Jet(vessel_number)
                self.vessels.append(new_vessel)
                self.place_vessel(new_vessel, level)
        
        #for submarine in range(1,vessel_numbers(0)):
        #    vessel_number += 1
        #    self.vessels.append(Submarine(vessel_number))
        #for destroyer in range(1,vessel_numbers(1)):
        #    vessel_number += 1
        #    self.vessels.append(Destroyer(vessel_number))
        #for jet in range(1,vessel_numbers(2)):
        #    vessel_number += 1
        #    self.vessels.append(Jet(vessel_number))
        
        new_vessel = General(vessel_number)
        self.vessels.append(new_vessel)
        self.place_vessel(new_vessel, randint(0,level))
          
    def place_vessel(self, vessel, level: int):
        success = False
        while ~success:
            x_coordinate = randint(0, self.board_size[0])
            x_max = x_coordinate + vessel.area.shape[0]
            if x_max >= self.board_size[0]:
                pass
            y_coordinate = randint(0, self.board_size[1])
            y_max = y_coordinate + vessel.area.shape[1]
            if y_max >= self.board_size[1]:
                pass
            
            sumValues = 0
            for x in range(x_coordinate, x_max):
                for y in range(y_coordinate, y_max):
                    sumValues += self.board_array([x, y, level])
                        
            if sumValues == 0:
                for x in range(0, vessel.area.shape[0]-1):
                    for y in range(0, vessel.area.shape[1]-1):
                        self.board_array[x + x_coordinate, y + y_coordinate, level] = vessel.area([x, y]) * vessel.vessel_number
                success = True


    def check_if_won(self, coordinates: tuple):

        result = self.board_array([coordinates])
        if result > 0:
            signal = self.vessels[result].hit_vessel()
            if signal.value < 3:
                signal = self.update_board(signal, coordinates, result)
                if signal.value == 3:
                    return True
            else:
                print(signal)
                return True
        else:
            print(signal)    
        return False

    def update_board(self, signal, coordinates: tuple, result: int):
        self.board_array[coordinates] = -signal.value
        if signal is signal.Destroyed:
            self.vessels.remove(result)
            self.board_array[self.vessels[result].coordinates] = -2
            if len(self.vessels) < 2:
                return Signal.Won
        return Signal


class Vessel():
    """ Base class """
    def __init__(self, vessel_number: int):
        self.vessel_number = vessel_number
        self.area = None

    def __hit_vessel(self):
        pass

class Submarine(Vessel):
    """ Level 0 Vessel """
    def __init__(self, vessel_number: int):
        super.__init__(vessel_number)
        self.area = np.array([[1, 1, 1]])
    
class Destroyer(Vessel):
    """ Level 1 Vessel """
    def __init__(self, vessel_number: int):
        super.__init__(vessel_number)
        self.area =np.array([[1], [1], [1], [1]])

class Jet(Vessel):
    """ Level 2 Vessel """
    def __init__(self, vessel_number: int):
        super.__init__(vessel_number)
        self.area = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]])

class General(Vessel):
    """ The General """
    def __init__(self, vessel_number: int):
        super.__init__(vessel_number)
        self.area = np.array([1])



class GameLoop:
    """ The class running the game loop for the Submarines game """

    def __init__(self, board_size: tuple = (6, 8, 3), number_of_vessels: tuple = (1, 1, 1)):
        self.board_size = board_size
        self.board1 = Board(board_size, number_of_vessels)
        self.board2 = Board(board_size, number_of_vessels)

    def start(self):
        self.has_game_ended = False
        self.is_it_player1s_turn = True
        print("New game has started!\n")
        print("blabla\n")
        while ~self.has_game_ended:
            self.has_game_ended = self.process_input()
            
            self.is_it_player1s_turn = ~self.is_it_player1s_turn
        
        if self.is_it_player1s_turn:
            print("Player 2 Wins!")
        else:
            print("Player 1 Wins!")
        
        
    def process_input(self):
        if self.is_it_player1s_turn:
            player_input = input("Player 1, Type in the coordinates you wish to bomb (x,y,z).")
        else:
            player_input = input("Player 2, Type in the coordinates you wish to bomb (x,y,z).")
        digits_in_input = []
        for char in player_input:
            if char.isdigit():
                digits_in_input.append(int(char))
        
        if len(digits_in_input) == 3:
            coordinates = (digits_in_input[0], digits_in_input[1], digits_in_input[2])
            if self.is_it_player1s_turn:
                has_game_ended = self.board2.check_if_won(coordinates)
            else:		
                has_game_ended = self.board2.check_if_won(coordinates)
            return has_game_ended
            
        if len(digits_in_input) == 0:
            if player_input == 'show':
                #show board and if thers tiem show where you bombed
                return False
            if player_input == 'quit':
                raise SystemExit()
                
        print("Input invalid, try again.")
        self.is_it_player1s_turn =  ~self.is_it_player1s_turn
        return False
