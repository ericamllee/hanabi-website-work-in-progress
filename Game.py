from Deck import Deck
from Player import Player
from Board import Board
from Deck import Card


class Game(object):
    def __init__(self):
        self.colors = ['red', 'green', 'blue', 'yellow', 'white']
        self.deck = Deck(self)
        self.player_names = []
        self.get_names()
        self.players = [Player(name) for name in self.player_names]
        self.hints = 8
        self.max_hints = 8
        self.fuses = 3
        self.board = Board(self.colors)
        self.deal_cards()
        self.turns_left = len(self.players)

        self.next_players = {}
        self.current = self.players[0]
        self.make_next_player_names()

        self.journal = {}
        for player in self.player_names:
            self.journal[player] = []

        self.play()

    # def get_names(self):
    #     while True:
    #         if len(self.player_names) >= 5:
    #             break
    #         value = raw_input("Enter a player's name. If all player names have been entered, type done.\n")
    #         if value == 'exit':
    #             os._exit(1)
    #         elif value == "done":
    #             if len(self.player_names) < 2:
    #                 print("There must be at least 2 players.")
    #                 continue
    #             break
    #         elif value in self.player_names:
    #             print("Each name must be unique. Try again.")
    #             continue
    #         else:
    #             self.player_names.append(value)

    def make_next_player_names(self):
        g = iter(list(range(1, len(self.player_names))))
        for player in self.players:
            try:
                self.next_players[player.name] = self.players[next(g)]
            except StopIteration:
                self.next_players[player.name] = self.players[0]

    def get_player(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

    def deal_cards(self):
        for each in self.players:
            if len(self.players) <= 3:
                while len(each.hand) < 5:
                    each.hand.append(self.deck.deal())
            else:
                while len(each.hand) < 4:
                    each.hand.append(self.deck.deal())

    def play(self):
        possible_actions = ['empty', 'discard_card', 'play_card', 'give_hint']

        while self.turns_left > 0:
            self.print_board()

            if self.deck.len() == 0:
                self.turns_left -= 1
                print("\n There are no more cards to draw. This is your last turn.")

            if self.hints == 0:
                action = self.get_valid_string(
                    "\nPlayer {0}, choose an action: \n  [1] Discard \n  [2] Place a card. \n  There are no more hints left. \n \n".format(
                        self.current.name), ['1', '2'])

            if self.hints > 0:
                action = self.get_valid_string(
                    "\nPlayer {0}, choose an action: \n  [1] Discard \n  [2] Place a card \n  [3] Give a hint. \n \n".format(
                        self.current.name), ['1', '2', '3'])

            getattr(self.current, possible_actions[int(action)])(self)

            self.journal[self.current.name] = []
            self.current = self.next_players[self.current.name]
            print("Your turn is over.")
            self.clear_screen()
            print("Pass the computer to {0}. Tell me when you're ready.".format(self.current.name))
            self.clear_screen()

        final_score = sum([card.number for card in self.board.displayed.values()])
        # print("Game over. Your final score is {0}.".format(final_score))
        # os._exit(1)
    #
    # def get_valid_string(self, prompt, valid_answers):
    #     while True:
    #         value = raw_input(prompt)
    #         if value == 'exit':
    #             os._exit(1)
    #         if value not in valid_answers:
    #             self.invalid_answers(value, valid_answers)
    #             continue
    #         else:
    #             break
    #     return value

    # def invalid_answers(self, value, valid_answers):
    #     os.system('clear')
    #     self.print_board()
    #     print(
    #         "\n{0} is not a valid response. Please try: {1}.\n".format(value, pretty_list_or(map(str, valid_answers))))

    def print_board(self):
        if self.journal[self.current.name]:
            print("\nSince you last played: ")
            for line in self.journal[self.current.name]:
                print(line)
        print("\n" + self.board.__repr__())
        print("Hints available: " + str(self.hints))
        print("Fuses left: {0}\n".format(str(self.fuses)))
        if self.board.no_more:
            print("There are no more [{0}] cards. \n".format("] [".join(map(Card.__repr__, self.board.no_more))))

        self.current.my_cards()
        other_player = self.next_players[self.current.name]
        while other_player != self.current:
            print(other_player.__repr__())
            other_player = self.next_players[other_player.name]

    # def clear_screen(self):
    #     g = raw_input("Press Enter to continue...")
    #     if g == 'exit':
    #         os._exit(1)
    #     else:
    #         os.system('clear')
    #         pass


def pretty_list_or(valid_answers):
  return ", ".join(valid_answers[:-2] + [" or ".join(valid_answers[-2:])])

def pretty_list_and(valid_answers):
  return ", ".join(valid_answers[:-2] + [" and ".join(valid_answers[-2:])])