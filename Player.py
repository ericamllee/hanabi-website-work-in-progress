from Deck import *
from Game import pretty_list_and


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []

    def my_cards(self):
        k = 0
        cards = []
        while k < len(self.hand):
            card_traits = self.hand[k].known_traits
            print_traits = ": " + ", ".join(card_traits)

            cards.append("Card {0}{1}".format(k + 1, print_traits if card_traits else ''))
            k += 1
        print("My cards: [{0}]\n".format("] [".join(cards) + "]"))

    def __repr__(self):
        return "{0}'s hand is [{1}]".format(self.name, "] [".join(map(Card.__repr__, self.hand)))

    def draw_a_new_card(self, game, card):
        self.hand.remove(card)
        self.hand.append(game.deck.deal())

    def play_card(self, game):
        index = game.get_valid_string(
            'Which card do you want to play? Choose a card number between 1 and {0}.\n'.format(len(self.hand)),
            map(str, range(1, len(self.hand) + 1)))
        card = self.hand[int(index) - 1]
        self.draw_a_new_card(game, card)

        if game.board.displayed[card.color].number == card.number - 1:
            game.board.displayed[card.color] = card
            message1 = "{0} played a {1} on the board.\n".format(self.name, card.__repr__())
            self.message_to_journal(game, message1)

            game.board.important_discards = [x for x in game.board.important_discards if
                                             x.color != card.color or x.number > card.number]

            if card.number == 5:
                if self.check_win(game):
                    print("\n Congratulations! You have set off all the fireworks.")
                    os._exit(1)
                game.hints += 1
                message2 = "{0} completed the {1} firework.".format(self.name, card.color)
                self.message_to_journal(game, message2)
        else:
            game.fuses -= 1

            if game.fuses > 0:
                message = "{0} played a {1}, which cannot be placed on the board. You have {2} more fuse{3}".format(
                    self.name, card.__repr__(), str(game.fuses), "s." if game.fuses > 1 else ".")
                self.message_to_journal(game, message)
            elif game.fuses == 0:
                print("The fireworks exploded in your face. You lose.")
                os._exit(1)
            game.board.add_to_discard_pile(self, game, card)

    def discard_card(self, game):
        index = game.get_valid_string(
            'Which card do you want to discard? Choose a number between 1 and {0}.\n'.format(len(self.hand)),
            map(str, range(1, len(self.hand) + 1)))
        card = self.hand[int(index) - 1]
        self.draw_a_new_card(game, card)
        game.hints = min(game.hints + 1, game.max_hints)

        message = "{0} discarded a {1}.".format(self.name, card.__repr__())
        self.message_to_journal(game, message)

        game.board.add_to_discard_pile(self, game, card)

    def give_hint(self, game):
        receiving_player_name = game.get_valid_string(
            'Which player would you like to give a hint to, {0}?\n'.format(self.name),
            [x for x in game.player_names if x != self.name])

        receiving_player = game.get_player(receiving_player_name)

        hint = game.get_valid_string(
            "Type in a color or a number to tell {0} about their cards.\n".format(receiving_player_name),
            game.colors + map(str, range(1, 6)))

        index = 1
        lst_of_cards = []
        game.hints -= 1

        if hint in game.colors:
            for card in receiving_player.hand:
                if card.color == hint:
                    lst_of_cards.append(index)
                index += 1
        else:
            for card in receiving_player.hand:
                if card.number == int(hint):
                    lst_of_cards.append(index)
                index += 1

        if len(lst_of_cards) == 0:
            message = "There are no {0} cards in {1}'s hand.".format(hint, receiving_player_name)
        else:
            message = "{0}'s card{1} in location{1} {2} {3} {4}.".format(
                receiving_player_name,
                's' if len(lst_of_cards) > 1 else '',
                pretty_list_and(map(str, lst_of_cards)),
                'is' if len(lst_of_cards) == 1 else 'are',
                hint)

        self.message_to_journal(game, "{0} gave a hint: {1}".format(self.name, message))

        for each_card in lst_of_cards:
            if hint not in receiving_player.hand[each_card - 1].known_traits:
                receiving_player.hand[each_card - 1].known_traits.append(hint)

    def message_to_journal(self, game, message):
        print(message)
        for x in game.journal:
            if x != self.name:
                game.journal[x].append(message)

    def check_win(self, game):
        for card in game.board.displayed.values():
            if card.number < 5:
                return False
        return True
