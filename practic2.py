import random

class Player:
    CHOICES = ('rock', 'paper', 'scissors')

    def __init__(self):
        self.move = None
        self.score = 0

class Computer(Player):
    def __init__(self):
        super().__init__()

    def choose(self):
        self.move = random.choice(Player.CHOICES)

class Human(Player):
    def __init__(self):
        super().__init__()

    def _human_choice(self):
        while True:
            human_choice = (input(f'Please choose your move from {Player.CHOICES}: ')).lower()
            if human_choice in Player.CHOICES:
                return human_choice
            else:
                print("Invalid Input. Please choose one from 'rock', 'paper', or 'scissors'")

    def choose(self):
        self.move = self._human_choice()

class RPSGame:
    def __init__(self):
        self._human = Human()
        self._computer = Computer()

    def _display_welcome_message(self):
        print('Welcome to Rock Paper Scissors!')

    def _display_goodbye_message(self):
        print('Thanks for playing Rock Paper Scissors. Goodbye!')

    def _human_wins(self):
        human_move = self._human.move
        computer_move = self._computer.move
        return ((human_move == 'rock' and computer_move == 'scissors') or
        (human_move == 'paper' and computer_move == 'rock') or
        (human_move == 'scissors' and computer_move == 'paper'))
    
    def _computer_wins(self):
        human_move = self._human.move
        computer_move = self._computer.move
        return ((computer_move == 'rock' and human_move == 'scissors') or
        (computer_move == 'paper' and human_move == 'rock') or
        (computer_move == 'scissors' and human_move == 'paper'))

    def _determine_winner(self):
        if self._human_wins():
            print('You win!')
            self._human.score += 1
        elif self._computer_wins():
            print('Computer wins!')
            self._computer.score += 1
        else:
            print("It's a tie!")

    def _display_current_score(self):
        print(f'Current Score - You: {self._human.score} : Computer: {self._computer.score}')

    def _display_winner(self):
        print(f'You chose: {self._human.move}')
        print(f'The computer chose: {self._computer.move}')
        self._determine_winner()

    def _grand_winner_determined(self):
        return self._human.score == 5 or self._computer.score == 5


    def _display_grand_winner(self):
        if self._human.score == 5:
            print('The grand winner is you!')
        elif self._computer.score == 5:
            print('The grand winner is computer!')
    

    def _play_again(self):
        response = input('Do you want to play another game? (Y/N): ')
        return response.strip().upper()
        
    def reset_score(self):
        self._human.score = 0
        self._computer.score = 0

    def play(self):
        self._display_welcome_message()
        while True:
            self.reset_score()
            while not self._grand_winner_determined():
                self._human.choose()
                self._computer.choose()
                self._display_winner()
                self._display_current_score()
            self._display_grand_winner()    
            if not self._play_again():
                break
        self._display_goodbye_message()

RPSGame().play()
