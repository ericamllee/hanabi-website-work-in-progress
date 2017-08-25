from Deck import Card


class Board(object):
    def __init__(self):
        self.displayed = {'red': Card('red', 0),
                          'green': Card('green', 0),
                          'blue': Card('blue', 0),
                          'yellow': Card('yellow', 0),
                          'white': Card('white', 0)}
        self.important_discards = []
        self.no_more = []

    def __repr__(self):
        return "Board: [{0}] \nDiscards: [{1}]".format("] [".join(map(Card.__repr__, self.displayed.values())), "] [".join(map(Card.__repr__, self.important_discards)))

    def add_to_discard_pile(self, person, game, card):
        if card.number != 1 and game.board.displayed[card.color].number < card.number:
            for important_discard in game.board.important_discards:
                if (card.color == important_discard.color
                    and card.number == important_discard.number) \
                        or card.number == 5:
                    message = "There are no more {0}s available in the game. " \
                              "It is now impossible to complete the {1} firework.".format(card.__repr__(), card.color)
                    self.no_more.append(card)
                    person.message_to_journal(game, message)
                    self.important_discards.remove(important_discard)
                    return None
        self.important_discards.append(card)