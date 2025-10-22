import random

class Deck:
    def __init__(self):
        self.suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        self.values = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
        self.cards = [(suit, value) for suit in self.suits for value in self.values]

class Participants:
    def __init__(self):
        self.score = 0
        self.cards = []

    def plays(self):
        pass

class Dealer(Participants):
    def __init__(self):
        super().__init__()
        self.deck = Deck()

    def shuffle_cards(self):
        random.shuffle(self.deck.cards)

    def deals(self, player):
        #deals cards. two randon cards to the dealer and the player
       player.cards = [self.deck.cards.pop(), self.deck.cards.pop()]
       self.cards = [self.deck.cards.pop(), self.deck.cards.pop()]

    def plays(self):
        #hit or stay
        pass

class Player(Participants):
    def __init__(self):
        super().__init__()
        self.betting_money = 5

    def rich_or_poor(self):
        rich = 10
        poor = 0
        return self.betting_money in [rich, poor]

    def reset(self):
        self.betting_money = 5
        self.cards = None

    def plays(self):
        #hit or stay
        pass

class TwentyOneGame:
    def __init__(self):
        self.player = Player()
        self.dealer = Dealer()

    def start(self):
        self.display_welcome_message()
        self.player.reset()

        while True:
            self.play_one_game()
            if self.ask_another_game() == 'n' or self.player.rich_or_poor():
                break

        self.display_goodbye_message()

    def play_one_game(self):
        self.dealer.shuffle_cards()
        self.dealer.deals(self.player)
        self.player.plays()
        self.dealer.plays()
        self.display_result()
        self.update_betting_money()

    def update_betting_money(self):
        #self.player.betting_money += 1 or -= 1 depends on the result
        pass

    def ask_another_game(self):

        while True:
            response = input("Do you want to play another game? (y/n): ").lower()

            if response in ["y", "n"]:
                return response

            print("Invalid Input. Please enter either y or n.")

    def display_welcome_message(self):
        print("Welcome to Twenty-One Game!")
        print("You and the Dealer will each be dealt two random cards. \n"
        "You'll be able to see both of your cards and one of the Dealer's cards. \n"
        "Enter 'Hit' to draw additional card, or 'Stay' to keep your current hand. \n"
        "At the end of the round, the total values of your hand and the Dealer's hand "
        "will be compared - whoever is closer to 21 wins! \n"
        "You can Hit as many times as you'd like during your turn, but if your "
        "total exceeds 21, you bust and lose the round. \n"
        "You'll start with $5 in betting money. \n"
        "Each win earns you $1, and each loss costs you $1. \n"
        "each time you win. \nThat means, you will lose $1 each time you lose :(. \n"
        "The game ends when you either lose all your money or strike it rich "
        "with $10. \nOf course, you can quit anytime you want. \n"
        "Good luck and have fun! :) ")

    def display_result(self):
        pass

    def display_goodbye_message(self):
        pass
game = TwentyOneGame()
game.start()
