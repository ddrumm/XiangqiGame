# Author: Don Drummond
# Date: 24 February 2020
# Description: Xiangqi Game is a python program
# to play the Xiangqi game for more details about
# the game visit: https://en.wikipedia.org/wiki/Xiangqi


class XiangqiGame:
    """
    XiangqiGame class runs the game. The class relies on the
    Board class to maintain the game state, but validates that
    the game should continue based the current players positions.
    """

    def __init__(self):
        self._game_state = "UNFINISHED"
        self._board = Board()
        self._most_recent_end_position = None
        self._red_check = False
        self._black_check = False

    @property
    def board(self):
        return self._board

    def get_game_state(self):
        return self._game_state

    def is_in_check(self, color):
        # implementation -- look at the positions around the general. must be 'soldier, horse, cannon, rook' check
        if color == 'red':
            positions_to_check = []
            red_position = self.get_numeric_array_position(self._board.rg.position)
            for x in self.get_positions_around_general(red_position):
                for c in x:
                    positions_to_check.append(self._board.game_board[10 - c[1]][self.convert_numeric_array_to_board(c)])
            positions_to_check = self.trim_positions(positions_to_check, "R")
            for z in positions_to_check:
                if z.authorized_move(self._board.rg.position, self.get_numeric_array_position(z._position),
                                     self.get_numeric_array_position(self._board.rg.position)):
                    self._red_check = True
                    return True
            return False
        elif color == 'black':
            positions_to_check = []
            black_position = self.get_numeric_array_position(self._board.bg.position)
            for x in self.get_positions_around_general(black_position):
                for c in x:
                    positions_to_check.append(self._board.game_board[10 - c[1]][self.convert_numeric_array_to_board(c)])
            positions_to_check = self.trim_positions(positions_to_check, "B")
            for z in positions_to_check:
                if z.authorized_move(self._board.bg.position, self.get_numeric_array_position(z._position),
                                     self.get_numeric_array_position(self._board.bg.position)):
                    self._black_check = True
                    return True
            return False




    def trim_positions(self, positions, color):
        """
        to trim None and the general's own pieces from the array for 'in check' possibilities
        :param positions: array of positions that could attack the general
        :return: a trimmed array that removes None type and the general's own pieces
        """
        # trim None off
        positions = [i for i in positions if i]
        # trim same color as general pieces
        trim_positions = []
        for x in positions:
            if x._color != color:
                trim_positions.append(x)

        return trim_positions



    def get_positions_around_general(self, general_positions):
        row_check = []
        column_check = []
        horse_check = []
        ensure_horse_on_board = []
        all_positions = []
        for i in range(10):
            column_check.append([general_positions[0], i+1])
        for k in range(9):
            row_check.append([k+1, general_positions[1]])

        horse_check.append(self.get_numeric_array_position(self._board._rh1._position))
        horse_check.append(self.get_numeric_array_position(self._board._rh2._position))
        horse_check.append(self.get_numeric_array_position(self._board._bh1._position))
        horse_check.append(self.get_numeric_array_position(self._board._bh2._position))
        ensure_horse_on_board.append(self._board._rh1)
        ensure_horse_on_board.append(self._board._rh2)
        ensure_horse_on_board.append(self._board._bh1)
        ensure_horse_on_board.append(self._board._bh1)
        for c, o in enumerate(horse_check):
            if self.board.game_board[10 - o[1]][self.convert_numeric_array_to_board(o)] != ensure_horse_on_board[c]:
                horse_check.remove(o)
        all_positions.append(row_check)
        all_positions.append(column_check)
        all_positions.append(horse_check)

        return all_positions


    def get_numeric_array_position(self, position):
        position = list(position)
        numeric_position = []
        if position[0] == "a":
            numeric_position.append(1)
        elif position[0] == "b":
            numeric_position.append(2)
        elif position[0] == "c":
            numeric_position.append(3)
        elif position[0] == "d":
            numeric_position.append(4)
        elif position[0] == "e":
            numeric_position.append(5)
        elif position[0] == "f":
            numeric_position.append(6)
        elif position[0] == "g":
            numeric_position.append(7)
        elif position[0] == "h":
            numeric_position.append(8)
        elif position[0] == "i":
            numeric_position.append(9)

        if len(position) == 3:
            numeric_position.append(10)
        else:
            numeric_position.append(int(position[1]))

        return numeric_position



    def convert_numeric_array_to_board(self, positions):
        board_location = ""
        if positions[0] == 1:
            board_location = board_location + "a"
        elif positions[0] == 2:
            board_location = board_location + "b"
        elif positions[0] == 3:
            board_location = board_location + "c"
        elif positions[0] == 4:
            board_location = board_location + "d"
        elif positions[0] == 5:
            board_location = board_location + "e"
        elif positions[0] == 6:
            board_location = board_location + "f"
        elif positions[0] == 7:
            board_location = board_location + "g"
        elif positions[0] == 8:
            board_location = board_location + "h"
        elif positions[0] == 9:
            board_location = board_location + "i"

        board_location = board_location + str(positions[1])

        return board_location



    def elephant_check(self, piece_object, start_move_array, end_move_array, start_position, end_position):
        check_if_blocking = piece_object.is_blocked_check(start_move_array, end_move_array)
        check_board_location = self.convert_numeric_array_to_board(check_if_blocking)
        if self._board.game_board[10 - check_if_blocking[1]][check_board_location] is not None:
            print("Not a possible move")
            return False
        else:
            self._board.set_board_space(10 - start_move_array[1], start_position, - end_move_array[1],
                                        end_position, piece_object)
            self._most_recent_end_position = end_position
            self._board.update_player_turn()
            return True



    def horse_check(self, piece_object, start_move_array, end_move_array, start_position, end_position):
        check_if_blocking = piece_object.is_blocked_check(start_move_array, end_move_array)
        check_board_location = self.convert_numeric_array_to_board(check_if_blocking)
        if self._board.game_board[10 - check_if_blocking[1]][check_board_location] is not None:
            print("Not a possible move")
            return False
        else:
            self._board.set_board_space(10 - start_move_array[1], start_position, - end_move_array[1],
                                        end_position, piece_object)
            self._most_recent_end_position = end_position
            self._board.update_player_turn()
            return True



    def rook_check(self, piece_object, start_move_array, end_move_array, start_position, end_position):
        for i in piece_object.is_blocked_check(start_move_array, end_move_array):
            check = self.convert_numeric_array_to_board(i)
            if self._board.game_board[10 - i[1]][check] is not None:
                print("Not a possible move")
                return False
        self._board.set_board_space(10 - start_move_array[1], start_position, - end_move_array[1],
                                    end_position, piece_object)
        self._most_recent_end_position = end_position
        self._board.update_player_turn()
        return True



    def cannon_check(self, piece_object, start_move_array, end_move_array, start_position, end_position):
        one_piece_in_way = 0
        final_spot = self.convert_numeric_array_to_board(end_move_array)
        for i in piece_object.is_blocked_check(start_move_array, end_move_array):
            check = self.convert_numeric_array_to_board(i)
            if self._board.game_board[10 - i[1]][check] is not None:
                one_piece_in_way += 1
        if one_piece_in_way == 0:
            self._board.set_board_space(10 - start_move_array[1], start_position, - end_move_array[1],
                                        end_position, piece_object)
            self._most_recent_end_position = end_position
            self._board.update_player_turn()
            return True
        elif one_piece_in_way == 1:
            print("Not a possible move")
            return False
        elif one_piece_in_way == 2 and self._board.game_board[10 - end_move_array[1]][final_spot] is not None:
            self._board.set_board_space(10 - start_move_array[1], start_position, - end_move_array[1],
                                        end_position, piece_object)
            self._most_recent_end_position = end_position
            self._board.update_player_turn()
            return True
        elif one_piece_in_way > 2:
            print("Not a possible move")
            return False

    def will_move_get_out_check(self, start_position, end_position):
        test_board = self._board._game_board
        print(test_board)

    def make_move(self, start_position, end_position):
        """
        :param start_position: position input for the player's piece
        :param end_position: position input for where the player would
        like to move their piece
        :return: returns "Not a possible move" in the case a move
        is not within the board, otherwise the function returns a new
        game state
        """

        print("players turn: " + self._board.get_player_turn())

        possible_moves = [
            "a10", "b10", "c10", "d10", "e10", "f10", "g10", "h10", "i10",
            "a9", "b9", "c9", "d9", "e9", "f9", "g9", "h9", "i9",
            "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "i8",
            "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "i7",
            "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6", "i6",
            "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "i5",
            "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "i4",
            "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "i3",
            "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2", "i2",
            "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "i1"]

        # these if statements valid input
        if start_position not in possible_moves:
            print("Not a possible move")
            return False

        if end_position not in possible_moves:
            print("Not a possible move")
            return False

        if start_position is None:
            print("Not a possible move")
            return False

        # building arrays of the move will enables utilizing the
        # pieces classes rules for the game logic
        start_move_array = self.get_numeric_array_position(start_position)
        end_move_array = self.get_numeric_array_position(end_position)


        # generate a number based position array on the board
        def convert_letter_to_int(move_array):
            letter = move_array[0]
            if letter == "a":
                letter = 1
            elif letter == "b":
                letter = 2
            elif letter == "c":
                letter = 3
            elif letter == "d":
                letter = 4
            elif letter == "e":
                letter = 5
            elif letter == "f":
                letter = 6
            elif letter == "g":
                letter = 7
            elif letter == "h":
                letter = 8
            elif letter == "i":
                letter = 9
            move_array[0] = letter
            return move_array

        convert_letter_to_int(start_move_array)
        convert_letter_to_int(end_move_array)

        def convert_numeric_array_to_board(location):
            board_location = ""
            if location[0] == 1:
                board_location = board_location + "a"
            elif location[0] == 2:
                board_location = board_location + "b"
            elif location[0] == 3:
                board_location = board_location + "c"
            elif location[0] == 4:
                board_location = board_location + "d"
            elif location[0] == 5:
                board_location = board_location + "e"
            elif location[0] == 6:
                board_location = board_location + "f"
            elif location[0] == 7:
                board_location = board_location + "g"
            elif location[0] == 8:
                board_location = board_location + "h"
            elif location[0] == 9:
                board_location = board_location + "i"

            board_location = board_location + str(location[1])

            return board_location

        # get the piece object from the board
        row_dict_start = self._board.game_board[10 - start_move_array[1]]
        row_dict_end = self._board.game_board[10 - end_move_array[1]]
        piece_object = row_dict_start.get(start_position)

        # checks to see if a player's move ends on their own piece
        # rejects the move if that is the case
        if row_dict_end.get(end_position) is not None:
            # ensures a player can't move from a spot that has no piece
            if piece_object is None:
                print("Not a possible move")
                return False
            end_position_piece = row_dict_end.get(end_position)
            if end_position_piece.get_name()[0] == piece_object.get_name()[0]:
                print("Not a possible move")
                return False

        # ensures a player can't move from a spot that has no piece
        if piece_object is None:
            print("Not a possible move")
            return False

        # ensures a player can only move their own pieces
        if piece_object.get_name()[0] != self.board.get_player_turn():
            print("Not a possible move")
            return False

        if self._black_check:
            print("ChECK")
            self.will_move_get_out_check(start_position, end_position)

        is_valid_move = piece_object.authorized_move(end_position, start_move_array, end_move_array)

        # checks if an Elephant piece movement is blocked due to blocking restrictions on different pieces
        if isinstance(piece_object, Elephant) and is_valid_move:
            return self.elephant_check(piece_object, start_move_array, end_move_array, start_position, end_position)

        if isinstance(piece_object, Horse) and is_valid_move:
            return self.horse_check(piece_object, start_move_array, end_move_array, start_position, end_position)

        if isinstance(piece_object, Rook) and is_valid_move:
            return self.rook_check(piece_object, start_move_array, end_move_array, start_position, end_position)

        if isinstance(piece_object, Cannon) and is_valid_move:
            return self.cannon_check(piece_object, start_move_array, end_move_array, start_position, end_position)

        if is_valid_move:
            self._board.set_board_space(10 - start_move_array[1], start_position, - end_move_array[1],
                                        end_position, piece_object)
            self._most_recent_end_position = end_position
            self._board.update_player_turn()
            return True
        else:
            return False


class Board:
    """
    The Board class builds out all the game pieces and sets
    up the starting board. The class also holds the
    state of the board. Once a player has made a validated move
    then the board is updated within the game class using the
    Board object
    """

    def __init__(self):
        self._br1 = Rook("B", "a10")
        self._br2 = Rook("B", "i10")
        self._bh1 = Horse("B", "b10")
        self._bh2 = Horse("B", "h10")
        self._be1 = Elephant("B", "c10")
        self._be2 = Elephant("B", "g10")
        self._ba1 = Advisor("B", "d10")
        self._ba2 = Advisor("B", "f10")
        self._bg = General("B", "e10")
        self._bc1 = Cannon("B", "b8")
        self._bc2 = Cannon("B", "h8")
        self._bs1 = Soldier("B", "a7")
        self._bs2 = Soldier("B", "c7")
        self._bs3 = Soldier("B", "e7")
        self._bs4 = Soldier("B", "g7")
        self._bs5 = Soldier("B", "i7")
        self._rr1 = Rook("R", "a1")
        self._rr2 = Rook("R", "i1")
        self._rh1 = Horse("R", "b1")
        self._rh2 = Horse("R", "h1")
        self._re1 = Elephant("R", "c1")
        self._re2 = Elephant("R", "g1")
        self._ra1 = Advisor("R", "d1")
        self._ra2 = Advisor("R", "f1")
        self._rg = General("R", "e1")
        self._rc1 = Cannon("R", "b3")
        self._rc2 = Cannon("R", "h3")
        self._rs1 = Soldier("R", "a4")
        self._rs2 = Soldier("R", "c4")
        self._rs3 = Soldier("R", "e4")
        self._rs4 = Soldier("R", "g4")
        self._rs5 = Soldier("R", "i4")

        self._game_board = [
            {"a10": self._br1, "b10": self._bh1, "c10": self._be1, "d10": self._ba1,
             "e10": self._bg, "f10": self._ba2, "g10": self._be2, "h10": self._bh2,
             "i10": self._br2},
            {"a9": None, "b9": None, "c9": None, "d9": None,
             "e9": None, "f9": None, "g9": None, "h9": None, "i9": None},
            {"a8": None, "b8": self._bc1, "c8": None, "d8": None,
             "e8": None, "f8": None, "g8": None, "h8": self._bc2, "i8": None},
            {"a7": self._bs1, "b7": None, "c7": self._bs2, "d7": None,
             "e7": self._bs3, "f7": None, "g7": self._bs4, "h7": None, "i7": self._bs5},
            {"a6": None, "b6": None, "c6": None, "d6": None,
             "e6": None, "f6": None, "g6": None, "h6": None, "i6": None},
            {"a5": None, "b5": None, "c5": None, "d5": None,
             "e5": None, "f5": None, "g5": None, "h5": None, "i5": None},
            {"a4": self._rs1, "b4": None, "c4": self._rs2, "d4": None,
             "e4": self._rs3, "f4": None, "g4": self._rs4, "h4": None, "i4": self._rs5},
            {"a3": None, "b3": self._rc1, "c3": None, "d3": None,
             "e3": None, "f3": None, "g3": None, "h3": self._rc2, "i3": None},
            {"a2": None, "b2": None, "c2": None, "d2": None,
             "e2": None, "f2": None, "g2": None, "h2": None, "i2": None},
            {"a1": self._rr1, "b1": self._rh1, "c1": self._re1, "d1": self._ra1,
             "e1": self._rg, "f1": self._ra2, "g1": self._re2, "h1": self._rh2,
             "i1": self._rr2}]

        # set Red to go first
        self._turn = "R"

        # opposing general's position
        self._opposing_general = self._bg.position

    def set_board_space(self, row_start, old_space, row_end, new_space, piece):
        """
        This function sets the game pieces new position on the board
        and then sets the game pieces old spot to None
        :param row_start: the row of the start_position input
        :param old_space: the actual start_position input
        :param row_end: the row of the end_position input
        :param new_space: the actual end_position input
        :param piece: the game piece object
        :return: None
        """
        self._game_board[row_end][new_space] = piece
        piece.set_position(new_space)
        self._game_board[row_start][old_space] = None

    def update_player_turn(self):
        """
        Updates a player's turn after a valid move is made
        :return: None
        """
        if self._turn == "R":
            self._turn = "B"
            self._opposing_general = self._bg.position
        elif self._turn == "B":
            self._turn = "R"
            self._opposing_general = self._rg.position

    def get_player_turn(self):
        """
        Getter function for player's turn
        :return: None
        """
        return self._turn

    def get_full_player_turn(self):
        if self._turn == "R":
            return "red"
        elif self._turn == "B":
            return "black"

    def check_win_condition(self):
        """
        Update the Game Class's game state. The function
        will be utilized to determine if either Red or Black
        has "checkmated" the other's General
        :return: if Red won, return: RED_WON
        if Black won, return: BLACK_WON
        if game remains unfinished return: UNFINISHED
        """
        pass

    def is_space_occupied(self, space):
        for i in self._game_board:
            print(i)

    def flying_general_check(self):
        """
        validate such that columns d, e, f do not allow a flying
        general situation to occur
        :return:
        """

    def print_board(self):
        print("a    b    c    d    e    f    g    h    i")
        for k in self._game_board:
            count = 0
            for v, n in k.items():
                if count % 10 == 0:
                    print("\n")
                    print("____ ____ ____ ____ ____ ____ ____ ____ ____")
                if n is not None:
                    print(n.get_name(), end="  ")
                if n is None:
                    print(" ", end="    ")
                count += 1

    @property
    def game_board(self):
        return self._game_board

    @property
    def rg(self):
        return self._rg

    @property
    def bg(self):
        return self._bg

    @property
    def opposing_general(self):
        return self._opposing_general


class General:
    """
    The General class maintains the name and rules
    for the General piece. The class validates if a
    player made an authorized move with the General
    piece.
    """

    def __init__(self, color, position):
        self._name = color + "-G"
        self._position = position
        self._color = color

    def get_name(self):
        """
        getter function for piece's name, used for printing the board
        :return: name of the piece
        """
        return self._name

    def set_position(self, position):
        self._position = position

    def authorized_move(self, end_position, start_move_array, end_move_array):
        """
        Generals may only move and capture one point
        orthogonally and may not leave the palace. The exception is
        the "flying general rule" which would allow a general to move
        across the board to capture the opposing general, however creating
        the situation would put a player in check, thus is not allowed.
        :param end_position: the desired end position of the move in algebraic notation
        :param end_move_array: the end position in an array [string, number]
        :return: True is the move is authorized, False if the move is not authorized
        """
        red_moves_allowed = [
            "e1", "d1", "f1",
            "e2", "d2", "f2",
            "e3", "d3", "f3"
        ]

        black_moves_allowed = [
            "e10", "d10", "f10",
            "e9", "d9", "f9",
            "e8", "d8", "f8"
        ]

        red_move_options = {
            "e1": ["e2", "d1", "f1"],
            "d1": ["e1", "d2"],
            "f1": ["e1", "f2"],
            "e2": ["e3", "e1", "d2", "f2"],
            "d2": ["d1", "d3", "e2"],
            "f2": ["f1", "f3", "e2"],
            "e3": ["e2", "d3", "f3"],
            "d3": ["e3", "d2"],
            "f3": ["e3", "f2"]
        }

        black_move_options = {
            "e10": ["e9", "d10", "f10"],
            "d10": ["e10", "d9"],
            "f10": ["e10", "f9"],
            "e9": ["e8", "e10", "d9", "f9"],
            "d9": ["d10", "d8", "e9"],
            "f9": ["f10", "f8", "e9"],
            "e8": ["e9", "d8", "f8"],
            "d8": ["e8", "d9"],
            "f8": ["e8", "f9"]
        }

        if self._color == "R":
            if end_position in red_moves_allowed:
                if end_position in red_move_options.get(self._position):
                    self._position = end_position
                    return True
                else:
                    return False
            else:
                return False
        elif self._color == "B":
            if end_position in black_moves_allowed:
                if end_position in black_move_options.get(self._position):
                    self._position = end_position
                    return True
                else:
                    return False
            else:
                return False

    @property
    def position(self):
        return self._position

    @property
    def color(self):
        return self._color


class Advisor:
    """
    The Advisor class maintains the name and rules
    for the Advisor piece. The class validates if a
    player made an authorized move with the Advisor
    piece.
    """

    def __init__(self, color, position):
        self._name = color + "-A"
        self._color = color
        self._position = position

    def get_name(self):
        return self._name

    def set_position(self, position):
        self._position = position

    def authorized_move(self, end_position, start_move_array, end_move_array):
        """
        Advisors may only move and capture one point diagonally and may not
        leave the palace, which confines them to only five points on the board.
        :param end_position: the desired end position of the move in algebraic notation
        :param end_move_array: the end position in an array [string, number]
        :return: True is the move is authorized, False if the move is not authorized
        """
        red_moves_allowed = ["d1", "e2", "f1", "d3", "f3"]
        black_moves_allowed = ["d10", "e9", "f10", "d8", "f8"]

        red_move_options = {
            "d1": ["e2"],
            "e2": ["d3", "f3", "d1", "f1"],
            "f1": ["e2"],
            "d3": ["e2"],
            "f3": ["e2"]
        }

        black_move_options = {
            "d10": ["e9"],
            "e9": ["d10", "f10", "d8", "f8"],
            "f10": ["e9"],
            "d8": ["e9"],
            "f8": ["e9"]
        }

        if self._color == "R":
            if end_position in red_moves_allowed:
                if end_position in red_move_options.get(self._position):
                    self._position = end_position
                    return True
                else:
                    return False
            else:
                return False
        elif self._color == "B":
            if end_position in black_moves_allowed:
                if end_position in black_move_options.get(self._position):
                    self._position = end_position
                    return True
                else:
                    return False
            else:
                return False

    @property
    def color(self):
        return self._color


class Elephant:
    """
    The Elephant class maintains the name and rules
    for the Elephant piece. The class validates if a
    player made an authorized move with the Elephant
    piece.
    """

    def __init__(self, color, position):
        self._name = color + "-E"
        self._color = color
        self._position = position

    def get_name(self):
        return self._name

    def set_position(self, position):
        self._position = position

    def is_blocked_check(self, start_move_array, end_move_array):
        """
        This checks if the elephant is blocked
        :param start_move_array: a numeric board position array for the start position
        :param end_move_array: a numeric board position array for the end position
        :return: a numeric board position array for the place to check if it is blocked
        """
        piece_to_check = []
        if start_move_array[0] > end_move_array[0]:
            piece_to_check.append(end_move_array[0] + 1)
        else:
            piece_to_check.append(start_move_array[0] + 1)

        if start_move_array[1] > end_move_array[1]:
            piece_to_check.append(start_move_array[1] - 1)
        else:
            piece_to_check.append(start_move_array[1] + 1)

        return piece_to_check

    def authorized_move(self, end_position, start_move_array, end_move_array):
        """
        Elephants may move and capture exactly two points diagonally and may
        not jump over intervening pieces. Additionally, elephants may not
        cross the river, which leaves them only seven possible board positions
        :param end_position: the desired end position of the move in algebraic notation
        :param end_move_array: the end position in an array [string, number]
        :return: True is the move is authorized, False if the move is not authorized
        """
        red_moves_allowed = ["c1", "a3", "c5", "e3", "g5", "i3", "g1"]
        black_moves_allowed = ["c10", "a8", "c6", "e8", "g6", "i8", "g10"]

        red_move_options = {
            "c1": ["a3", "e3"],
            "a3": ["c1", "c5"],
            "c5": ["a3", "e3"],
            "e3": ["c5", "c1", "g5", "g1"],
            "g5": ["e3", "i3"],
            "i3": ["g5", "g1"],
            "g1": ["i3", "e3"]
        }

        black_move_options = {
            "c10": ["a8", "e8"],
            "a8": ["c10", "c6"],
            "c6": ["a8", "e8"],
            "e8": ["c6", "c10", "g6", "g10"],
            "g6": ["e8", "i8"],
            "i8": ["g6", "g10"],
            "g10": ["i8", "e8"]
        }

        if self._color == "R":
            if end_position in red_moves_allowed:
                if end_position in red_move_options.get(self._position):
                    self._position = end_position
                    return True
                else:
                    return False
            else:
                return False
        elif self._color == "B":
            if end_position in black_moves_allowed:
                if end_position in black_move_options.get(self._position):
                    self._position = end_position
                    return True
                else:
                    return False
            else:
                return False
        return True

    @property
    def color(self):
        return self._color


class Horse:
    """
    The Horse class maintains the name and rules
    for the Horse piece. The class validates if a
    player made an authorized move with the Horse
    piece.
    """

    def __init__(self, color, position):
        self._name = color + "-H"
        self._color = color
        self._position = position

    def get_name(self):
        return self._name

    def set_position(self, position):
        self._position = position

    def is_blocked_check(self, start_move_array, end_move_array):
        piece_to_check = []
        # if the horse is moving right one column
        if start_move_array[0] + 1 == end_move_array[0] - 1:
            piece_to_check.append(start_move_array[0] + 1)
            piece_to_check.append(start_move_array[1])
        # if the horse is moving left one column
        elif start_move_array[0] - 1 == end_move_array[0] + 1:
            piece_to_check.append(start_move_array[0] - 1)
            piece_to_check.append(start_move_array[1])
        # if the horse is moving up one row
        elif start_move_array[1] + 1 == end_move_array[1] - 1:
            piece_to_check.append(start_move_array[0])
            piece_to_check.append(start_move_array[1] + 1)
        # if the horse is moving down one row
        elif start_move_array[1] - 1 == end_move_array[1] + 1:
            piece_to_check.append(start_move_array[0])
            piece_to_check.append(start_move_array[1] - 1)

        return piece_to_check

    def authorized_move(self, end_position, start_move_array, end_move_array):
        """
        need to test if it is a valid move based on numeric array

        :param end_position: the desired end position of the move in algebraic notation
        :param end_move_array: the end position in an array [string, number]
        :return: True is the move is authorized, False if the move is not authorized
        """
        # horse attempting to move up one row
        if start_move_array[1] + 1 == end_move_array[1] - 1:
            # attempting to right up two rows
            if start_move_array[1] + 2 == end_move_array[1]:
                # attempting to move right one column
                if start_move_array[0] + 1 == end_move_array[0]:
                    return True
                # attempting to move left one column
                elif start_move_array[0] - 1 == end_move_array[0]:
                    return True
                else:
                    return False
            else:
                return False

        # horse attempting to move down one row
        if start_move_array[1] - 1 == end_move_array[1] + 1:
            # attempting to move down two rows
            if start_move_array[1] - 2 == end_move_array[1]:
                # attempting to move right one column
                if start_move_array[0] + 1 == end_move_array[0]:
                    return True
                # attempting to move left one column
                elif start_move_array[0] - 1 == end_move_array[0]:
                    return True
                else:
                    return False
            else:
                return False

        # horse attempting to move right one column
        if start_move_array[0] + 1 == end_move_array[0] - 1:
            # attempting to move right two columns
            if start_move_array[0] + 2 == end_move_array[0]:
                # attempting to move up one row
                if start_move_array[1] + 1 == end_move_array[1]:
                    return True
                # attempting to move down one row
                elif start_move_array[0] - 1 == end_move_array[1]:
                    return True
                else:
                    return False
            else:
                return False

        # horse attempting to move left one column
        if start_move_array[0] - 1 == end_move_array[0] + 1:
            # attempting to move right two columns
            if start_move_array[0] - 2 == end_move_array[0]:
                # attempting to move up one row
                if start_move_array[1] + 1 == end_move_array[1]:
                    return True
                # attempting to move down one row
                elif start_move_array[0] - 1 == end_move_array[1]:
                    return True
                else:
                    return False
            else:
                return False

        @property
        def color(self):
            return self._color


class Rook:
    """
    The Rook class maintains the name and rules
    for the Rook piece. The class validates if a
    player made an authorized move with the Rook
    piece.
    """

    def __init__(self, color, position):
        self._name = color + "-R"
        self._color = color
        self._position = position

    def get_name(self):
        return self._name

    def set_position(self, position):
        self._position = position

    def is_blocked_check(self, start_move_array, end_move_array):
        board_locations_to_check = []
        # check rook movement locations if moving down by row
        if start_move_array[0] == end_move_array[0] and start_move_array[1] > end_move_array[1]:
            spots = start_move_array[1] - (end_move_array[1] + 1)
            counter = start_move_array[1] - 1
            for i in range(spots):
                board_locations_to_check.append([counter, start_move_array[0]])
            counter -= 1
            return board_locations_to_check
        # check rook movement locations if moving up by row
        elif start_move_array[0] == end_move_array[0] and start_move_array[1] < end_move_array[1]:
            spots = end_move_array[1] - (start_move_array[1] + 1)
            counter = start_move_array[1] + 1
            for i in range(spots):
                board_locations_to_check.append([start_move_array[0], counter])
                counter += 1
            return board_locations_to_check
        # check rook movement locations if moving left by column
        elif start_move_array[1] == end_move_array[1] and start_move_array[0] > end_move_array[0]:
            spots = start_move_array[0] - (end_move_array[0] + 1)
            counter = start_move_array[0] - 1
            for i in range(spots):
                board_locations_to_check.append([counter, start_move_array[1]])
                counter -= 1
            return board_locations_to_check
        # check rook movement locations if moving right by column
        elif start_move_array[1] == end_move_array[1] and start_move_array[0] < end_move_array[0]:
            spots = end_move_array[0] - (start_move_array[0] + 1)
            counter = start_move_array[0] + 1
            for i in range(spots):
                board_locations_to_check.append([counter, start_move_array[1]])
                counter += 1
            return board_locations_to_check

    def authorized_move(self, end_position, start_move_array, end_move_array):
        """
        :param end_position: the desired end position of the move in algebraic notation
        :param end_move_array: the end position in an array [string, number]
        :return: True is the move is authorized, False if the move is not authorized
        """
        # Rook moves along column
        if start_move_array[0] == end_move_array[0]:
            return True
        # Rook moves along row
        elif start_move_array[1] == end_move_array[1]:
            return True
        # Rook is attemping an illegal move
        elif start_move_array[0] != end_move_array[0] and start_move_array[1] != end_move_array[1]:
            return False

    @property
    def color(self):
        return self._color

class Cannon:
    """
    The Cannon class maintains the name and rules
    for the Cannon piece. The class validates if a
    player made an authorized move with the Cannon
    piece.
    """

    def __init__(self, color, position):
        self._name = color + "-C"
        self._color = color
        self._position = position

    def get_name(self):
        return self._name

    def set_position(self, position):
        self._position = position

    def is_blocked_check(self, start_move_array, end_move_array):
        board_locations_to_check = []
        # check cannon movement locations if moving down by row
        if start_move_array[0] == end_move_array[0] and start_move_array[1] > end_move_array[1]:
            spots = start_move_array[1] - end_move_array[1]
            counter = start_move_array[1] - 1
            for i in range(spots):
                board_locations_to_check.append([start_move_array[0], counter])
                counter -= 1
            return board_locations_to_check
        # check cannon movement locations if moving up by row
        elif start_move_array[0] == end_move_array[0] and start_move_array[1] < end_move_array[1]:
            spots = end_move_array[1] - start_move_array[1]
            counter = start_move_array[1] + 1
            for i in range(spots):
                board_locations_to_check.append([start_move_array[0], counter])
                counter += 1
            return board_locations_to_check
        # check cannon movement locations if moving left by column
        elif start_move_array[1] == end_move_array[1] and start_move_array[0] > end_move_array[0]:
            spots = start_move_array[0] - end_move_array[0]
            counter = start_move_array[0] - 1
            for i in range(spots):
                board_locations_to_check.append([counter, start_move_array[1]])
                counter -= 1
                # print(board_locations_to_check)
            return board_locations_to_check
        # check cannon movement locations if moving right by column
        elif start_move_array[1] == end_move_array[1] and start_move_array[0] < end_move_array[0]:
            spots = end_move_array[0] - start_move_array[0]
            counter = start_move_array[0] + 1
            for i in range(spots):
                board_locations_to_check.append([counter, start_move_array[1]])
                counter += 1
            return board_locations_to_check

    def authorized_move(self, end_position, start_move_array, end_move_array):
        """
        :param end_position: the desired end position of the move in algebraic notation
        :param end_move_array: the end position in an array [string, number]
        :return: True is the move is authorized, False if the move is not authorized
        """
        # Cannon moves along a column
        if start_move_array[0] == end_move_array[0]:
            return True
        # Cannon moves along row
        elif start_move_array[1] == end_move_array[1]:
            return True
        # Cannon attemping an illegal move
        elif start_move_array[0] != end_move_array[0] and start_move_array[1] != end_move_array[1]:
            return False

    @property
    def color(self):
        return self._color


class Soldier:
    """
    The Soldier class maintains the name and rules
    for the Soldier piece. The class validates if a
    player made an authorized move with the Soldier
    piece.
    """

    def __init__(self, color, position):
        self._name = color + "-S"
        self._color = color
        self._position = position

    def get_name(self):
        return self._name

    def set_position(self, position):
        self._position = position

    def authorized_move(self, end_position, start_move_array, end_move_array):
        """

        :param end_position: the desired end position of the move in algebraic notation
        :param end_move_array: the end position in an array [string, number]
        :return: True is the move is authorized, False if the move is not authorized
        :param end_move:
        :return:
        """
        if self._color == "R":
            if start_move_array[1] < 6:
                if start_move_array[0] != end_move_array[0]:
                    return False
                elif start_move_array[1] + 1 == end_move_array[1]:
                    return True
                else:
                    return False
            elif start_move_array[1] > 5:
                if start_move_array[0] + 1 == end_move_array[0]:
                    return True
                elif start_move_array[0] - 1 == end_move_array[0]:
                    return True
                elif start_move_array[1] + 1 == end_move_array[1]:
                    return True
                else:
                    return False
        elif self._color == "B":
            if start_move_array[1] > 5:
                if start_move_array[0] != end_move_array[0]:
                    return False
                elif start_move_array[1] - 1 == end_move_array[1]:
                    return True
                else:
                    return False
            elif start_move_array[1] < 6:
                if start_move_array[0] + 1 == end_move_array[0]:
                    return True
                elif start_move_array[0] - 1 == end_move_array[0]:
                    return True
                elif start_move_array[1] - 1 == end_move_array[1]:
                    return True
                else:
                    return False

        @property
        def color(self):
            return self._color


def main():
    game = XiangqiGame()


if __name__ == "__main__":
    main()
