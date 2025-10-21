"""
Classes:
    Square: Represents a single cell on the board and its marker.
    Board:  Stores and renders the 3x3 grid of Square objects.
    Player/Human/Computer: Players with associated markers.
    TTTGame: Orchestrates gameplay, moves, and win/tie detection.
"""

import random
import os

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def join_or(lst, delimiter=", ", conjunction="or"):
    """
    Format and print items from an iterable into a human-readable string.

    - For 2 items: joins them with 'or' (e.g., 'A or B').
    - For 3 or more items: joins with the given delimiter, and adds the conjunction
    before the last item (e.g., 'A, B, or C').
    - For 1 or 0 items: prints the item (or empty list) directly.

    Arguments:
    lst (iterable): The collection of items to format.
    delimiter (str): The string to use between items (default: ', ').
    conjunction (str): The word to use before the final item (default: 'or').
    """
    lst_str = [str(item) for item in lst]
    if len(lst_str) == 2:
        return " or ".join(lst_str)

    if len(lst_str) >= 3:
        return delimiter.join(lst_str[:-1]) + delimiter + conjunction + " " + lst_str[-1]

    if len(lst_str) <= 1:
        return "" if len(lst_str) == 0 else lst_str[0]

class Square:
    """A single board cell that holds a marker."""
    INITIAL_MARKER = " "
    HUMAN_MARKER = "X"
    COMPUTER_MARKER = "O"

    def __init__(self, marker=INITIAL_MARKER):
        self._marker = marker

    def __str__(self):
        return self.marker

    @property
    def marker(self):
        return self._marker

    @marker.setter
    def marker(self, marker):
        self._marker = marker

    def is_empty(self):
        """Return True if the square has no marker."""
        return self.marker == Square.INITIAL_MARKER

class Board:
    """3x3 Tic Tac Toe grid addressed by keys 1 to 9."""
    def __init__(self):
        self.reset()

    def reset(self):
        self.squares = {key: Square() for key in range(1, 10)}

    def display(self):
        print()
        print("   |   |")
        print(f" {self.squares[1]} | {self.squares[2]} | {self.squares[3]}")
        print("___|___|___")
        print("   |   |")
        print(f" {self.squares[4]} | {self.squares[5]} | {self.squares[6]}")
        print("___|___|___")
        print("   |   |")
        print(f" {self.squares[7]} | {self.squares[8]} | {self.squares[9]}")
        print("   |   |")
        print()

    def available_squares(self):
        """Return a list of keys for squares that are currently empty."""
        return [key for key, square in self.squares.items()
                            if square.is_empty()]

    def mark_square_at(self, key, marker):
        """Place a marker at a given board key"""
        self.squares[key].marker = marker

    def is_full(self):
        """Return True if there are no empty squares remaining."""
        return len(self.available_squares()) == 0

class Player:
    def __init__(self, marker, board):
        self.marker = marker
        self.board = board

class Human(Player):
    def __init__(self, board):
        super().__init__(Square.HUMAN_MARKER, board)
        self.score = 0

    def moves(self):
        """Ask the user to choose a square to mark. If the choice is
        not valid, error message will prompt.
        """

        while True:
            valid_choices = self.board.available_squares()
            human_choice = input(f"Please enter a number ({join_or(valid_choices)}) to "
                                    "mark a square. Square goes from left to right "
                                    "from the top to the bottom: ")
            try:
                human_choice = int(human_choice)
            except ValueError:
                print("Invalid Input. Please type a number.")
                continue

            if not 1 <= human_choice <= 9:
                print("Sorry, that's not a valid choice. Choose between 1 and 9")
            elif human_choice not in valid_choices:
                print("The square is already taken. Choose another square.")
            else:
                self.board.mark_square_at(human_choice, self.marker)
                break

class Computer(Player):
    def __init__(self, board, winning_rows):
        super().__init__(Square.COMPUTER_MARKER, board)
        self.score = 0
        self.winning_rows = winning_rows

    def moves(self, opponent_marker):
        """When the human has 2 squares in a row with an unused square
        in the 3rd position of that row, Computer will choose the unused square.
        Otherwise, Computer choose a random empty square."""

        valid_choices = self.board.available_squares()

        if self.smart_choices(opponent_marker) is not None:
            computer_choice = self.smart_choices(opponent_marker)
        else:
            computer_choice = random.choice(valid_choices)

        self.board.mark_square_at(computer_choice, self.marker)

    def smart_choices(self, opponent_marker):
        """
        Determine the most strategic move for the computer.

        The computer first checks for a winning move for itself and selects
        that square.
        If none exists, it checks for a potential winning move by the human
        player and chooses that square to block. If neither case applies,
        it returns None.
        """

        if self.find_winning_square(self.marker) is not None:
            return self.find_winning_square(self.marker)

        if self.find_winning_square(opponent_marker) is not None:
            return self.find_winning_square(opponent_marker)

        return None

    def find_winning_square(self, marker):

        for a, b, c in self.winning_rows:
            m_a = self.board.squares[a].marker
            m_b = self.board.squares[b].marker
            m_c = self.board.squares[c].marker

            if m_a == m_b == marker and m_c == Square.INITIAL_MARKER:
                return c
            if m_b == m_c == marker and m_a == Square.INITIAL_MARKER:
                return a
            if m_a == m_c == marker and m_b == Square.INITIAL_MARKER:
                return b

        return None

class TTTGame:
    """Orchestrates Tic Tac Toe game."""

    WINNING_ROWS = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8 ,9),
        (1, 5, 9),
        (3, 5, 7),
        (1, 4, 7),
        (2, 5, 8),
        (3, 6, 9),
    )

    def __init__(self):
        self.board = Board()
        self.human = Human(self.board)
        self.computer = Computer(self.board, TTTGame.WINNING_ROWS)
        self.player_going_first = 'human'

    def play(self):
        """Run the main game until someone wins or the borad is full."""
        self.display_welcome_message()

        while True:
            self.play_one_game()

            if self.grand_winner_determined() is not None:
                self.display_grand_winner()
                self.display_goodbye_message()
                break

    def play_one_game(self):
        self.board.reset()
        current_player = self.player_going_first

        while True:

            clear_screen()
            self.display_current_score()
            self.board.display()

            if current_player == 'human':

                self.human.moves()
                current_player = 'computer'

            elif current_player == 'computer':

                self.computer.moves(self.human.marker)
                current_player = 'human'

            if self.is_game_over():
                break

        clear_screen()
        self.board.display()
        self.display_results()
        self.update_current_score()
        self.update_player_going_first()

    def is_game_over(self):
        return self.board.is_full() or self.someone_won()

    def someone_won(self):
        """Return True if someone is determined as a winner."""

        return self.winning_marker() is not None

    def winning_marker(self):
        """
        Return the winning marker("X" or "O")
        if any winning row has three idential non-empty markers
        """

        for a, b, c in TTTGame.WINNING_ROWS:
            m_a = self.board.squares[a].marker
            m_b = self.board.squares[b].marker
            m_c = self.board.squares[c].marker
            if m_a != Square.INITIAL_MARKER and (m_a == m_b == m_c):
                return m_a

        return None

    def determine_winner(self):
        winner_marker = self.winning_marker()
        if winner_marker == self.human.marker:
            return 'human'
        if winner_marker == self.computer.marker:
            return 'computer'
        if self.board.is_full():
            return 'tie'

        return None

    def grand_winner_determined(self):
        if self.human.score == 3:
            return 'human'
        if self.computer.score == 3:
            return 'computer'

        return None

    def update_current_score(self):
        winner = self.determine_winner()
        if winner == 'human':
            self.human.score += 1
        elif winner == 'computer':
            self.computer.score += 1

    def update_player_going_first(self):
        self.player_going_first = ('computer' if self.player_going_first == 'human'
        else 'human')

    def display_current_score(self):
        print(f'human: {self.human.score} = computer: {self.computer.score}')

    def display_grand_winner(self):
        if self.grand_winner_determined() == 'human':
            print('Congratulations! The grand winner is you!')
        elif self.grand_winner_determined() == 'computer':
            print('Sorry! The grand winner is computer!')

    def display_welcome_message(self):
        print("Welcome to Tic Tac Toe!")

    def display_goodbye_message(self):
        print("Thanks for playing Tic Tac Toe! Goodbye!")

    def display_results(self):
        if self.determine_winner() == 'human':
            print("You won! Congratulations!")
        elif self.determine_winner() == 'computer':
            print("Computer won!")
        elif self.determine_winner() == 'tie':
            print("It's a tie!")

    # @staticmethod
    # def ask_play_again():
    #     while True:
    #         response = input("Do you want to play another game? (y/n) ").lower()

    #         if response in ["y", "n"]:
    #             return response

    #         print("Invalid input. Please enter y or n.")

game = TTTGame()
game.play()
