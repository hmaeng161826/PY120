import random
import os

def clear_screen():
    os.system('clear')

class Deck:
    def __init__(self):
        self.suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        self.values = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
        self.cards = [(suit, value) for suit in self.suits for value in self.values]

class Participants:
    def __init__(self):
        self.score = 0
        self.cards = []
        self.total_values = 0

    def hit(self, dealer):
        dealer.deals_a_card(self)
        print(f"Drawn card is {self.cards[-1]}.")

    def display_initial_values(self):

        for suit, value in self.cards:
            if value in ["Jack", "Queen", "King", "Ace"]:
                value = 10
                self.total_values += value
            elif value == 'Ace' and self.total_values + value > 21:
                value = 1
                self.total_values += value
            elif value == 'Ace' and self.total_values + value <= 21:
                value = 11
                self.total_values += value
            else:
                self.total_values += value
        print(f'You have {self.cards}.')
        print(f'Your current total value is {self.total_values}')

    def calculate_additional_value(self):
        suit, added_value = self.cards[-1]
        if added_value in ["Jack", "Queen", "King"]:
            added_value = 10
            self.total_values += added_value
        elif added_value == 'Ace' and self.total_values + added_value > 21:
            added_value = 1
            self.total_values += added_value
        elif added_value == 'Ace' and self.total_values + added_value <= 21:
            added_value = 11
            self.total_values += added_value
        else:
            self.total_values += added_value

        return self.total_values

    def stay(self):
        pass

    def busted(self):
        return self.total_values > 21

    def reset(self):
        self.cards = []
        self.total_values = 0

    # def reveal_values(self):

    #     print(f'Current total values is {self.total_values}.')



class Dealer(Participants):
    def __init__(self):
        super().__init__()
        self.deck = Deck()

    def shuffle_cards(self):
        random.shuffle(self.deck.cards)

    def initial_deals(self, player):
        player.cards = [self.deck.cards.pop(), self.deck.cards.pop()]
        self.cards = [self.deck.cards.pop(), self.deck.cards.pop()]

    def deals_a_card(self, participant):
        participant.cards.append(self.deck.cards.pop())

    def plays(self, dealer):
        while self.total_values <= 17:
            self.hit(dealer)
            self.calculate_additional_value()
            if self.busted():
                print('Dealer busted!')
                break

    def reveal_card(self):
        random_card = random.choice(self.cards)
        print(f'Dealer has {random_card}.')

class Player(Participants):
    def __init__(self):
        super().__init__()
        self.betting_money = 5

    def rich_or_poor(self):
        rich = 10
        poor = 0
        return self.betting_money in [rich, poor]

    def reset(self):
        super().reset()
        self.betting_money = 5

    def plays(self, dealer):
        while True:
            if self.busted():
                print('Oops! You busted!')
                break
            else:
                move = input("Choose `hit` or `stay`: ")
                if move == 'hit':
                    self.hit(dealer)
                    print(f'Your current total value is {self.calculate_additional_value()}')
                elif move == 'stay':
                    print(f'Your final total value is {self.total_values}')
                    break
                else:
                    print('Invalid Input. Type either hit or stay.')

class TwentyOneGame:
    def __init__(self):
        self.player = Player()
        self.dealer = Dealer()

    def start(self):
        self.display_welcome_message()
        self.player.reset()

        while True:
            self.player.reset()
            self.dealer.reset()
            self.play_one_game()
            if self.ask_another_game() == 'n' or self.player.rich_or_poor():
                break
            clear_screen()

        self.display_goodbye_message()

    def play_one_game(self):
        while True:
            self.dealer.shuffle_cards()
            self.dealer.initial_deals(self.player)
            self.dealer.reveal_card()
            self.player.display_initial_values()
            self.player.plays(self.dealer)
            if self.player.busted():
                break
            self.dealer.plays(self.dealer)
            if self.dealer.busted():
                break
            self.display_result()
            self.update_betting_money()

            break

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
        print(f'Final value is Player: {self.player.total_values} : Dealer: '
        f'{self.dealer.total_values}')
        if self.player.total_values > self.dealer.total_values:
            print("Congratulations! You won!")
        elif self.player.total_values < self.dealer.total_values:
            print("Sorry! Dealer won!")
        else:
            print("It's a tie!")

    def display_goodbye_message(self):
        print("Thanks for playing Twenty-One Game! Goodbye!")

game = TwentyOneGame()
game.start()
