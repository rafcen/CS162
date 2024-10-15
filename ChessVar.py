# Author: Rafael Cendejas
# GitHub username: rafcen
# Date: 03/17/2024
# Description: This is a variation of the game chess with modified rules and pieces. The game is played on a 8x8 grid.
# Each player also gets an additional Hunter and Falcon piece in their reserve

class ChessVar:
    """
    Represents a chess game.

    Attributes:
        _board (list): The chess board represented as a 2D list.
        _current_player (str): The current player ('WHITE' or 'BLACK').
        _white_reserve (dict): The reserve of white pieces.
        _black_reserve (dict): The reserve of black pieces.
        _game_state (str): The state of the game ('UNFINISHED', 'WHITE_WON', or 'BLACK_WON').
    """

    def __init__(self, _game_state="UNFINISHED"):
        """
        Initializes a new instance of the ChessVar class.

        Args:
            _game_state (str, optional): The initial state of the game. Defaults to "UNFINISHED".
        """
        self._board = [
            [Rook('WHITE', 'a', '0'), Knight('WHITE', 'b', '0'),
             Bishop('WHITE', 'c', '0'), Queen('WHITE', 'd', '0'),
             King('WHITE', 'e', '0'), Bishop('WHITE', 'f', '0'),
             Knight('WHITE', 'g', '0'), Rook('WHITE', 'h', '0')],
            [Pawn('WHITE', chr(97+i), '1') for i in range(8)],
            *[[None for _ in range(8)] for _ in range(4)],
            [Pawn('BLACK', chr(97+i), '6') for i in range(8)],
            [Rook('BLACK', 'a', '7'), Knight('BLACK', 'b', '7'),
             Bishop('BLACK', 'c', '7'), Queen('BLACK', 'd', '7'),
             King('BLACK', 'e', '7'), Bishop('BLACK', 'f', '7'),
             Knight('BLACK', 'g', '7'), Rook('BLACK', 'h', '7')],
        ]
        self._current_player = 'WHITE'
        self._white_reserve = {'F': True, 'H': True}
        self._black_reserve = {'f': True, 'h': True}
        self._game_state = _game_state

    def get_game_state(self):
        """
        Gets the current state of the game.

        Returns:
            str: The current state of the game.
        """
        return self._game_state

    def display_board(self):
        """
        Displays the current state of the chess board.
        """
        for i in range(8):
            print(i+1, end=' ')
            for j in range(8):
                piece = self._board[i][j]
                if piece is None:
                    print('.', end=' ')
                else:
                    print(piece.display_char, end=' ')
            print()
        print('  a b c d e f g h')

    def empty(self, x: int, y: int):
        """
        Checks if a specific position on the board is empty.

        Args:
            x (int): The x-coordinate of the position.
            y (int): The y-coordinate of the position.

        Returns:
            bool: True if the position is empty, False otherwise.
        """
        return self._board[y][x] is None

    def piece(self, x: int, y: int):
        """
        Gets the piece at a specific position on the board.

        Args:
            x (int): The x-coordinate of the position.
            y (int): The y-coordinate of the position.

        Returns:
            object: The piece at the specified position.
        """
        return self._board[y][x]

    @staticmethod
    def get_coordinates(pos: str):
        """
        Converts a position string to coordinates on the board.

        Args:
            pos (str): The position string (e.g., 'a1').

        Returns:
            tuple: The x and y coordinates on the board.
        """
        return int(pos[1]) - 1, ord(pos[0]) - ord('a')

    def update_game_state(self):
        """
        Updates the state of the game based on the current board configuration.
        """
        white_king_present = False
        black_king_present = False

        for i in range(8):
            for j in range(8):
                piece = self._board[i][j]
                if isinstance(piece, King) and piece.color == 'WHITE':
                    white_king_present = True
                elif isinstance(piece, King) and piece.color == 'BLACK':
                    black_king_present = True

        if not white_king_present:
            self._game_state = 'BLACK_WON'
        elif not black_king_present:
            self._game_state = 'WHITE_WON'
        else:
            self._game_state = 'UNFINISHED'

    def make_move(self, start_pos: str, end_pos: str):

        """
        Checks to see if the game is finished.
        """
        if self._game_state != 'UNFINISHED':
            return False

        """
        Makes a move on the chess board.

        Args:
            start_pos (str): The starting position of the piece (e.g., 'a2').
            end_pos (str): The ending position of the piece (e.g., 'a4').

        Returns:
            bool: True if the move is successful, False otherwise.
        """
        start_y, start_x = self.get_coordinates(start_pos)
        end_y, end_x = self.get_coordinates(end_pos)

        # Convert end_y to integer
        end_y = int(end_y)

        piece = self._board[start_y][start_x]
        if piece is None:
            return False
        if piece.color.lower() != self._current_player.lower():
            return False

        # check to see if move is legal
        if not piece.is_legal_move(end_x, end_y, self):
            return False

        # Update the board state
        self._board[start_y][start_x] = None
        piece.x = chr(97 + end_x)
        piece.y = str(end_y)
        self._board[end_y][end_x] = piece

        # Update the game state
        self.update_game_state()

        # Switch the current player
        self._current_player = 'WHITE' if self._current_player == 'BLACK' else 'BLACK'

        return True

    def enter_fairy_piece(self, piece: str, pos: str):
        """
        Enters a fairy piece onto the chess board.

        Args:
            piece (str): The fairy piece to enter.
            pos (str): The position to enter the piece (e.g., 'a2').

        Returns:
            bool: True if the piece is successfully entered, False otherwise.
        """
        x, y = self.get_coordinates(pos)
        if piece.islower():
            if self._black_reserve[piece]:
                self._board[x][y] = piece
                self._black_reserve[piece] = False
                self.update_game_state()
                return True
            return False
        if piece.isupper():
            if self._white_reserve[piece]:
                self._board[x][y] = piece
                self._white_reserve[piece] = False
                self.update_game_state()
                return True
            return False
        return False

    def switch_turn(self):
        """
        Switches the turn to the next player.
        """
        self._current_player = 'WHITE' if self._current_player == 'BLACK' else 'BLACK'


class Position:
    """
    Represents a position on a chessboard.

    Attributes:
        x (int): The x-coordinate of the position.
        y (int): The y-coordinate of the position.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y


class PieceColor:
    """
    Represents the color of a chess piece.

    Attributes:
        NONE (int): Represents no color.
        WHITE (int): Represents the color white.
        BLACK (int): Represents the color black.
    """
    NONE = -1
    WHITE = 0
    BLACK = 1


class ChessPiece:
    """
    Represents a chess piece.

    Attributes:
        color (str): The color of the chess piece.
        x (int): The x-coordinate of the chess piece on the board.
        y (int): The y-coordinate of the chess piece on the board.
        has_moved (bool): Indicates whether the chess piece has moved.
        display_char (str): The character used to display the chess piece on the board.
    """

    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.has_moved = False
        self.display_char = ''

    def is_legal_move(self, end_x, end_y, board):
        """
        Checks if the move to the specified coordinates is legal.

        Args:
            end_x (int): The x-coordinate of the destination.
            end_y (int): The y-coordinate of the destination.
            board (list): The chess board.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        raise NotImplementedError("Subclass must implement this method")


class Pawn(ChessPiece):
    """
    Represents a pawn chess piece.

    Attributes:
        color (str): The color of the pawn ('WHITE' or 'BLACK').
        x (str): The x-coordinate of the pawn on the chessboard.
        y (int): The y-coordinate of the pawn on the chessboard.
        display_char (str): The character used to represent the pawn on the chessboard.

    Methods:
        is_legal_move(end_x: int, end_y: int, board) -> bool:
            Checks if the pawn can legally move to the specified coordinates on the chessboard.

    """

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.display_char = 'P' if self.color == 'WHITE' else 'p'

    def is_legal_move(self, end_x: int, end_y: int, board):
        """
        Checks if the pawn can legally move to the specified coordinates on the chessboard.

        Args:
            end_x (int): The x-coordinate of the destination.
            end_y (int): The y-coordinate of the destination.
            board (ChessBoard): The chessboard on which the pawn is placed.

        Returns:
            bool: True if the move is legal, False otherwise.

        """
        # The starting y-coordinate is already an integer
        start_y = int(self.y)
        start_x = ord(self.x) - ord('a')

        # Check if the destination is within the board boundaries
        if not (0 <= end_x < 8 and 0 <= end_y < 8):
            return False

        # Determine the direction of movement based on the pawn's color
        direction = 1 if self.color == 'WHITE' else -1

        # Check for capturing diagonally
        if abs(ord(self.x) - ord(chr(97 + end_x))) == 1 and end_y == start_y + direction:
            # Check if the destination contains an opponent's piece
            if board.piece(end_x, end_y) is not None and board.piece(end_x, end_y).color != self.color:
                return True

        # Check for regular pawn moves
        if start_y + direction == end_y and start_x == end_x and board.empty(end_x, end_y):
            return True

        # Check for the initial two-square move
        if (start_y + 2 * direction == end_y and start_x == end_x and not self.has_moved
                and board.empty(end_x, end_y) and board.empty(end_x, end_y - direction)):
            return True

        return False



class Knight(ChessPiece):
    """
    Represents a knight chess piece.

    Attributes:
        color (str): The color of the knight ('WHITE' or 'BLACK').
        x (str): The x-coordinate of the knight's position on the chessboard.
        y (str): The y-coordinate of the knight's position on the chessboard.
        display_char (str): The character used to represent the knight on the chessboard.

    Methods:
        is_legal_move(end_x, end_y, board): Checks if the move to the specified coordinates is legal.

    """

    def __init__(self, color, x, y):
        """
        Initializes a new instance of the Knight class.

        Args:
            color (str): The color of the knight ('WHITE' or 'BLACK').
            x (str): The x-coordinate of the knight's position on the chessboard.
            y (str): The y-coordinate of the knight's position on the chessboard.

        """
        super().__init__(color, x, y)
        self.display_char = 'N' if self.color == 'WHITE' else 'n'

    def is_legal_move(self, end_x, end_y, board):
        """
        Checks if the move to the specified coordinates is legal.

        Args:
            end_x (int): The x-coordinate of the destination position.
            end_y (int): The y-coordinate of the destination position.
            board (Board): The chessboard on which the move is being made.

        Returns:
            bool: True if the move is legal, False otherwise.

        """
        start_x = ord(self.x) - ord('a')
        start_y = int(self.y)
        end_y = int(end_y)
        if not (0 <= end_x < 8 and 0 <= end_y < 8):
            return False

        if ((abs(start_x - end_x) == 1 and abs(start_y - end_y) == 2) or
                (abs(start_x - end_x) == 2 and abs(start_y - end_y) == 1)):
            if board.empty(end_x, end_y) or board.piece(end_x, end_y).color != self.color:
                return True


class Bishop(ChessPiece):
    """
    Represents a bishop chess piece.

    Attributes:
        color (str): The color of the bishop ('WHITE' or 'BLACK').
        x (str): The x-coordinate of the bishop's position on the chessboard.
        y (str): The y-coordinate of the bishop's position on the chessboard.
        display_char (str): The character used to represent the bishop on the chessboard.

    Methods:
        is_legal_move(end_x, end_y, board): Checks if the bishop can legally move to the specified position on the chessboard.
    """

    def __init__(self, color, x, y):
        """
        Initializes a new instance of the Bishop class.

        Args:
            color (str): The color of the bishop ('WHITE' or 'BLACK').
            x (str): The x-coordinate of the bishop's position on the chessboard.
            y (str): The y-coordinate of the bishop's position on the chessboard.
        """
        super().__init__(color, x, y)
        self.display_char = 'B' if self.color == 'WHITE' else 'b'

    def is_legal_move(self, end_x, end_y, board):
        """
        Checks if the bishop can legally move to the specified position on the chessboard.

        Args:
            end_x (int): The x-coordinate of the destination position.
            end_y (int): The y-coordinate of the destination position.
            board (Board): The chessboard on which the bishop is placed.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        start_x = ord(self.x) - ord('a')
        start_y = int(self.y)
        end_y = int(end_y)

        # Check if the destination is within the board boundaries
        if not (0 <= end_x < 8 and 0 <= end_y < 8):
            return False

        # Check if the move is diagonal
        if abs(start_x - end_x) == abs(start_y - end_y):
            step_x = 1 if start_x < end_x else -1
            step_y = 1 if start_y < end_y else -1
            x, y = start_x + step_x, start_y + step_y
            while x != end_x and y != end_y:
                if not board.empty(x, y):
                    return False
                x += step_x
                y += step_y

            # Check if the destination is empty or contains an opponent's piece
            if board.empty(end_x, end_y) or board.piece(end_x, end_y).color != self.color:
                return True

        return False


class Rook(ChessPiece):
    """
    Represents a rook chess piece.

    Attributes:
        color (str): The color of the rook ('WHITE' or 'BLACK').
        x (str): The x-coordinate of the rook on the chessboard.
        y (int): The y-coordinate of the rook on the chessboard.
        display_char (str): The character used to represent the rook on the chessboard.

    Methods:
        is_legal_move(end_x, end_y, board): Checks if a move to the specified coordinates is a legal move for the rook.

    """
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.display_char = 'R' if self.color == 'WHITE' else 'r'

    def is_legal_move(self, end_x, end_y, board):
        start_x = ord(self.x) - ord('a')
        start_y = int(self.y)

        # Check if the destination is within the board boundaries
        if not (0 <= end_x < 8 and 0 <= end_y < 8):
            return False

        # Check if the move is along a rank or file
        if (start_x == end_x and start_y != end_y) or (start_x != end_x and start_y == end_y):
            step_x = 1 if start_x < end_x else -1 if start_x > end_x else 0
            step_y = 1 if start_y < end_y else -1 if start_y > end_y else 0

            # Check for obstructions along the rank or file
            if step_x != 0:  # Moving along the file
                x = start_x + step_x
                while x != end_x:
                    if not board.empty(x, start_y):
                        return False
                    x += step_x
            else:  # Moving along the rank
                y = start_y + step_y
                while y != end_y:
                    if not board.empty(start_x, y):
                        return False
                    y += step_y

            # Check if the destination is empty or contains an opponent's piece
            destination_piece = board.piece(end_x, end_y)
            if destination_piece is None or destination_piece.color != self.color:
                return True

        return False



class Queen(ChessPiece):
    """
    Represents a queen chess piece.

    Attributes:
        color (str): The color of the queen ('WHITE' or 'BLACK').
        x (str): The x-coordinate of the queen on the chessboard.
        y (int): The y-coordinate of the queen on the chessboard.
        display_char (str): The character used to represent the queen on the chessboard.

    Methods:
        is_legal_move(end_x: int, end_y: int, board) -> bool:
            Checks if the queen can legally move to the specified coordinates on the chessboard.

    """

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.display_char = 'Q' if self.color == 'WHITE' else 'q'

    def is_legal_move(self, end_x: int, end_y: int, board):
        """
        Checks if the queen can legally move to the specified coordinates on the chessboard.

        Args:
            end_x (int): The x-coordinate of the destination.
            end_y (int): The y-coordinate of the destination.
            board (ChessBoard): The chessboard on which the queen is placed.

        Returns:
            bool: True if the move is legal, False otherwise.

        """
        # The starting y-coordinate is already an integer
        start_y = int(self.y)
        start_x = ord(self.x) - ord('a')

        # Check if the destination is within the board boundaries
        if not (0 <= end_x < 8 and 0 <= end_y < 8):
            return False

        # Check if the move is along a rank, file, or diagonal
        if (start_x == end_x and start_y != end_y) or (start_x != end_x and start_y == end_y) or \
                abs(start_x - end_x) == abs(start_y - end_y):
            step_x = 1 if start_x < end_x else -1 if start_x > end_x else 0
            step_y = 1 if start_y < end_y else -1 if start_y > end_y else 0

            # Check for obstructions along the rank, file, or diagonal
            x, y = start_x + step_x, start_y + step_y
            while x != end_x or y != end_y:
                if not board.empty(x, y):
                    return False
                x, y = x + step_x, y + step_y

            # Check if the destination is empty or contains an opponent's piece
            destination_piece = board.piece(end_x, end_y)
            if destination_piece is None or destination_piece.color != self.color:
                return True

        return False



class King(ChessPiece):
    def __init__(self, color, x, y):
        """
        Initializes a King object.

        Args:
            color (str): The color of the King ('WHITE' or 'BLACK').
            x (str): The x-coordinate of the King's position on the chessboard.
            y (str): The y-coordinate of the King's position on the chessboard.
        """
        super().__init__(color, x, y)
        self.display_char = 'K' if self.color == 'WHITE' else 'k'

    def is_legal_move(self, end_x, end_y, board):
        """
        Checks if the move from the current position to the specified position is a legal move for the King.

        Args:
            end_x (int): The x-coordinate of the destination position on the chessboard.
            end_y (int): The y-coordinate of the destination position on the chessboard.
            board (Board): The chessboard object.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        start_x = ord(self.x) - ord('a')
        start_y = int(self.y)
        end_y = int(end_y)
        # Check if the destination is within the board boundaries
        if not (0 <= end_x < 8 and 0 <= end_y < 8):
            return False

        # Check if the move is to an adjacent square
        if abs(start_x - end_x) <= 1 and abs(start_y - end_y) <= 1:
            # Check if the destination is empty or contains an opponent's piece
            if board.empty(end_x, end_y) or board.piece(end_x, end_y).color != self.color:
                return True

        return False


class Falcon(ChessPiece):
    """
    Represents a Falcon chess piece.

    Attributes:
        color (str): The color of the Falcon ('WHITE' or 'BLACK').
        x (int): The x-coordinate of the Falcon on the chessboard.
        y (int): The y-coordinate of the Falcon on the chessboard.
        display_char (str): The character used to represent the Falcon on the chessboard.

    Methods:
        is_legal_move(end_x, end_y, board): Checks if the move to the specified coordinates is a legal move for the Falcon.
    """

    def __init__(self, color, x, y):
        """
        Initializes a new instance of the Falcon class.

        Args:
            color (str): The color of the Falcon ('WHITE' or 'BLACK').
            x (int): The x-coordinate of the Falcon on the chessboard.
            y (int): The y-coordinate of the Falcon on the chessboard.
        """
        super().__init__(color, x, y)
        self.display_char = 'F' if self.color == 'WHITE' else 'f'

    def is_legal_move(self, end_x, end_y, board):
        """
        Checks if the move to the specified coordinates is a legal move for the Falcon.

        Args:
            end_x (int): The x-coordinate of the destination.
            end_y (int): The y-coordinate of the destination.
            board (ChessBoard): The chessboard on which the move is being made.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        # Check if the move is forward like a bishop
        if abs(self.x - end_x) == abs(self.y - end_y):
            step_x = 1 if self.x < end_x else -1
            step_y = 1 if self.y < end_y else -1
            x, y = self.x + step_x, self.y + step_y
            while x != end_x and y != end_y:
                if not board.empty(x, y):
                    return False  # Diagonal obstruction
                x += step_x
                y += step_y
            # Check if the destination contains an opponent's piece
            if not board.empty(end_x, end_y) and board.piece(end_x, end_y).color != self.color:
                return True

        # Check if the move is backward like a rook
        if (self.x == end_x and abs(self.y - end_y) > 0) or (self.y == end_y and abs(self.x - end_x) > 0):
            step = 1 if self.x < end_x or self.y < end_y else -1
            if self.x == end_x:
                y = self.y + step
                while y != end_y:
                    if not board.empty(self.x, y):
                        return False  # Vertical obstruction
                    y += step
            else:
                x = self.x + step
                while x != end_x:
                    if not board.empty(x, self.y):
                        return False  # Horizontal obstruction
                    x += step
            # Check if the destination contains an opponent's piece
            if not board.empty(end_x, end_y) and board.piece(end_x, end_y).color != self.color:
                return True

        return False


class Hunter(ChessPiece):
    def __init__(self, color, x, y):
        """
        Initializes a Hunter object.

        Args:
            color (str): The color of the Hunter ('WHITE' or 'BLACK').
            x (int): The x-coordinate of the Hunter on the chessboard.
            y (int): The y-coordinate of the Hunter on the chessboard.
        """
        super().__init__(color, x, y)
        self.display_char = 'H' if self.color == 'WHITE' else 'h'

    def is_legal_move(self, end_x, end_y, board):
        """
        Checks if a move is legal for the Hunter.

        Args:
            end_x (int): The x-coordinate of the destination position.
            end_y (int): The y-coordinate of the destination position.
            board (Board): The chessboard object.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        # Check if the move is like a knight
        if (abs(self.x - end_x) == 2 and abs(self.y - end_y) == 1) or (
                abs(self.x - end_x) == 1 and abs(self.y - end_y) == 2):
            # Check if the destination contains an opponent's piece
            if not board.empty(end_x, end_y) and board.piece(end_x, end_y).color != self.color:
                return True

        # Check if the move is along a rank or file
        if self.x == end_x or self.y == end_y:
            step = 1 if self.x < end_x or self.y < end_y else -1

            # Check for obstructions along the rank or file
            if self.x == end_x:
                y = self.y + step
                while y != end_y:
                    if not board.empty(self.x, y):
                        return False
                    y += step
            else:
                x = self.x + step
                while x != end_x:
                    if not board.empty(x, self.y):
                        return False
                    x += step

            # Check if the destination contains an opponent's piece
            if not board.empty(end_x, end_y) and board.piece(end_x, end_y).color != self.color:
                return True

        return False

