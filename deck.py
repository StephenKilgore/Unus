from enum import Enum
import random


class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'
    BLACK = 'black'


class CardType(Enum):
    NUMERICAL = 'numerical'
    SKIP = 'skip'
    REVERSE = 'reverse'
    DRAW_2 = 'draw2'
    WILD = 'wild'
    WILD_DRAW_4 = 'wilddraw4'


class Deck(object):

    def __init__(self, name):
        self.name = name
        self.card_list = []
        self._generate_suite(Color.RED)
        self._generate_suite(Color.BLUE)
        self._generate_suite(Color.YELLOW)
        self._generate_suite(Color.GREEN)
        self._generate_wilds()
        random.shuffle(self.card_list)

    def _generate_wilds(self):
        for i in range(0, 4):
            self.card_list += [Card(Color.BLACK, "W", CardType.WILD)]
            self.card_list += [Card(Color.BLACK, "WD4", CardType.WILD_DRAW_4)]

    def _generate_suite(self, color):

        suite_list = []

        # generate regular face cards, two sets of 1-9
        for i in range(0, 2):
            suite_list += [Card(color, str(x), CardType.NUMERICAL) for x in range(1, 10)]

        # add one '0' card
        suite_list.append(Card(color, str(0), CardType.NUMERICAL))

        # generate special cards: two each of skip, reverse, draw 2
        for i in range(0, 2):
            suite_list += [Card(color, "S", CardType.SKIP)]
            suite_list += [Card(color, "R", CardType.REVERSE)]
            suite_list += [Card(color, "D2", CardType.DRAW_2)]

        self.card_list += suite_list

    def add_cards(self, card_list):
        self.card_list += card_list

    def take_cards(self, n):
        cards = [self.card_list.pop(x) for x in range(0, n)]
        return cards[0] if n == 1 else cards


class Card(object):
    def __init__(self, color, value, card_type):
        self.color = color
        self.value = str(value)
        self.card_type = card_type
        self.name = self.color.name[0] + self.value \
            if self.card_type != CardType.WILD and self.card_type != CardType.WILD_DRAW_4 else self.value

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name
