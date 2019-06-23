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
        self.live_vessel_count = 0
        self.board_size = board_size
        self.board_array = np.zeros(board_size, np.int8)
        self.vessels = []
        self.create_vessels(vessel_numbers)

    def create_vessels(self, vessel_numbers: tuple):
        
        for level in range(0,len(vessel_numbers)):
            for vessel in range(0,vessel_numbers[level]):
                self.live_vessel_count += 1
                if level == 0:
                    new_vessel = Submarine(self.live_vessel_count)
                if level == 1:
                    new_vessel = Destroyer(self.live_vessel_count)
                if level == 2:
                    new_vessel = Jet(self.live_vessel_count)
                self.vessels.append(new_vessel)
                self.place_vessel(new_vessel, level)
        
        new_vessel = General(self.live_vessel_count + 1)
        self.vessels.append(new_vessel)
        self.place_vessel(new_vessel, randint(0,2))
      
    def place_vessel(self, vessel, level: int):
        success = False
        while not success:
            if randint(0,1):
                vessel.area = np.transpose(vessel.area)
            x_coordinate = randint(0, self.board_size[0])
            x_max = x_coordinate + vessel.area.shape[0]
            if x_max >= self.board_size[0]:
                continue
            y_coordinate = randint(0, self.board_size[1])
            y_max = y_coordinate + vessel.area.shape[1]
            if y_max >= self.board_size[1]:
                continue
            
            sumValues = 0
            for x in range(x_coordinate, x_max):
                for y in range(y_coordinate, y_max):
                    sumValues += self.board_array[x, y, level]
                        
            if sumValues == 0:
                for x in range(0, vessel.area.shape[0]):
                    for y in range(0, vessel.area.shape[1]):
                        self.board_array[x + x_coordinate, y + y_coordinate, level] = vessel.area[x, y] * vessel.vessel_number
                success = True
                vessel.placement_coordinates = [x_coordinate, y_coordinate]

    def check_if_won(self, coordinates: tuple):
        result = self.board_array[coordinates]
        if result > 0:
            hurt_vessel = self.vessels[result-1]
            signal = hurt_vessel.hit_vessel(coordinates)
            if signal.value < 3:
                if (self.update_board(signal, coordinates, hurt_vessel)):
                    return True
            else:
                return True
        else:
            print(Signal(result)) 
        return False

    def update_board(self, signal, coordinates: tuple, hurt_vessel):
        """
        Updates board and returns True is game is over (only general left).
        """
        self.board_array[coordinates] = -signal.value
        if signal is signal.Destroyed:
            for x in range(0, hurt_vessel.area.shape[0]):
                for y in range(0, hurt_vessel.area.shape[1]):
                    self.board_array[x + hurt_vessel.placement_coordinates[0], y + hurt_vessel.placement_coordinates[1], coordinates[2]] = hurt_vessel.area[x, y] * -2
            self.live_vessel_count -= 1
            if self.live_vessel_count == 0:
                print("Entire fleet destroyed.")
                return True
        return False

class Vessel:
    """ Base class """
    def __init__(self, vessel_number: int):
        self.vessel_number = vessel_number
        self.placement_coordinates = []
        self.area = None

    def hit_vessel(self):
        print("HIT!")

    def destroy_vessel(self , vessel_name: str):
        print(vessel_name, "was destroyed.")

class Submarine(Vessel):
    """ Level 0 Vessel """
    def __init__(self, vessel_number: int):
        super().__init__(vessel_number)
        self.area = np.array([[1, 1, 1]])

    def hit_vessel(self, coordinates):
        super().hit_vessel()
        self.destroy_vessel("Submarine " + str(self.vessel_number))
        return Signal.Destroyed

class Destroyer(Vessel):
    """ Level 1 Vessel """
    def __init__(self, vessel_number: int):
        super().__init__(vessel_number)
        self.area = np.array([[1], [1], [1], [1]])
        self.durability = 4

    def hit_vessel(self, coordinates):
        super().hit_vessel()
        self.durability -= 1
        if self.durability == 0:
            self.destroy_vessel("Destroyer " + str(self.vessel_number))
            return Signal.Destroyed
        return Signal.Hit

class Jet(Vessel):
    """ Level 2 Vessel """
    def __init__(self, vessel_number: int):
        super().__init__(vessel_number)
        self.area = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]])

    def hit_vessel(self, coordinates):
        super().hit_vessel()
        self.destroy_vessel("Jet " + str(self.vessel_number))
        return Signal.Destroyed

class General(Vessel):
    """ The General """
    def __init__(self, vessel_number: int):
        super().__init__(vessel_number)
        self.area = np.array([[1]])

    def hit_vessel(self, coordinates):
        super().hit_vessel()
        self.destroy_vessel("The general")
        return Signal.Won

class GameLoop:
    """ The class running the game loop for the Submarines game """

    def __init__(self, board_size: tuple = (6, 8, 3), number_of_vessels: tuple = (1, 1, 1)):
        self.board_size = board_size
        self.board1 = Board(board_size, number_of_vessels)
        self.board2 = Board(board_size, number_of_vessels)

    def start(self):
        self.has_game_ended = False
        self.is_it_player1s_turn = True
        print("\nA new game has started!")
        print("At any given time, you can type 'quit' to exit the game,\nor 'show' to see your board.\n")
        
        while not self.has_game_ended:
            self.has_game_ended = self.process_input()
            self.is_it_player1s_turn = not self.is_it_player1s_turn
        
        if self.is_it_player1s_turn:
            print("Player 2 Wins!\n")
        else:
            print("Player 1 Wins!\n")
        
    def process_input(self):
        if self.is_it_player1s_turn:
            player_input = input("Player 1, Type in the coordinates you wish to bomb (x,y,z).")
        else:
            player_input = input("Player 2, Type in the coordinates0 you wish to bomb (x,y,z).")
        digits_in_input = []
        for char in player_input:
            if char.isdigit():
                digits_in_input.append(int(char))
        
        if len(digits_in_input) == 3 and \
                digits_in_input[0] < self.board_size[0] and \
                digits_in_input[1] < self.board_size[1] and \
                digits_in_input[2] < self.board_size[2]:
            coordinates = (digits_in_input[0], digits_in_input[1], digits_in_input[2])
            if self.is_it_player1s_turn:
                has_game_ended = self.board2.check_if_won(coordinates)
            else:       
                has_game_ended = self.board1.check_if_won(coordinates)
            return has_game_ended
            
        if len(digits_in_input) == 0:
            if player_input == 'show':
                if self.is_it_player1s_turn:
                    self.show_board(self.board1)
                else:
                    self.show_board(self.board2)
                self.is_it_player1s_turn =  not self.is_it_player1s_turn
                return False
            if player_input == 'quit':
                raise SystemExit()
                
        print("Input invalid, try again.")
        self.is_it_player1s_turn =  not self.is_it_player1s_turn
        return False

    def show_board(self, board: Board):
            print("Level 0:\n", board.board_array[..., 0], '\n')
            print("Level 1:\n", board.board_array[..., 1], '\n')
            print("Level 2:\n", board.board_array[..., 2], '\n')

if __name__ == '__main__':
    game = GameLoop()
    game.start()
