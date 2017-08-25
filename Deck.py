from random import shuffle


class Card(object):
    def __init__(self, color, num):
        self.card = (color, num)
        self.color = color
        self.number = num
        self.known_traits = []

    def __repr__(self):
        return self.color + ' ' + str(self.number), self.color


class Deck(object):
    def __init__(self, game):
        self.deck = []
        for color in game.colors:
            for num in range(0, 3):
                self.deck.append(Card(color, 1))
            for num in range(2, 5):
                self.deck.append(Card(color, num))
                self.deck.append(Card(color, num))
            self.deck.append(Card(color, 5))
        shuffle(self.deck)

    def len(self):
        return len(self.deck)

    def __repr__(self):
        return self.deck.__repr__()

    def deal(self):
        if self.deck:
            return self.deck.pop()