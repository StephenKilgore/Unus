from deck import Deck, Color, CardType, Card
from data_structures import DoubleList


class Player(object):

    def __init__(self, name, is_human):
        self.name = name
        self.is_human = is_human
        self.hand = []

    def __str__(self):
        return self.name

    def check_hand(self, card_str):
        for card in self.hand:
            if card.name == card_str:
                return card
        return None

    def take_card(self, card):
        self.hand.remove(card)


class GameManager(object):

    def __init__(self):
        self.deck = Deck("Uno Deck")
        self.discard_pile = []
        self.player_list = None
        self.current_player = None
        self.current_card = None
        self.current_color = None
        self.current_value = None
        self.game_over = False
        self.direction_reversed = False

    def start(self):
        while not self.game_over:

            # get players, deal cards,  and flip over top card from deck
            if not self.player_list:
                self._set_players()
                self._deal()
                self._change_current_card(self._get_starting_card())
            else:
                self._start_turn()
                if self.current_player.is_human:
                    print(f"Your hand: {self.current_player.hand}")
                    played_card = self._play_card()
                    self.current_player.take_card(played_card)
                    self._change_current_card(played_card)
                    if played_card.card_type == CardType.WILD or played_card.card_type == CardType.WILD_DRAW_4:
                        self._pick_new_color()
                    self._end_turn()
                else:
                    self._end_turn()

    def _set_players(self):
        num_opponents = 0
        while num_opponents < 1:
            print("Welcome to Unus! How many AI opponents do you want? You must enter at least 1:")
            num_opponents = int(input("> "))
        print(f"Great! You've chosen to play with {num_opponents} {'opponents' if num_opponents > 1 else 'opponent'}.")

        players = []
        for i in range(0, num_opponents + 1):
            if i == 0:
                print("What is the human player's name?")
                player_name = input('> ')
                players.append(Player(player_name, True))
            else:
                players.append(Player(f"Computer_{i}", False))
        self.player_list = DoubleList.generate_linked_list(players)

    def get_players(self):
        current_node = self.player_list
        yield current_node.val
        current_node = current_node.next

        # we have processed the head node, traverse rest of list until we circle back to head
        while current_node.val != self.player_list.val:
            yield current_node.val
            current_node = current_node.next

    def _deal(self):
        player_node = self.player_list
        while True:
            if len(player_node.val.hand) != 0:
                break
            player_node.val.hand += self.deck.take_cards(7)
            player_node = player_node.next

    def _play_card(self):
        while True:
            choice = str(input('> ').upper())
            card = self.current_player.check_hand(choice)
            if not card:
                print(f"The card {choice} was not found in your hand. Please choose another.")
                print(self.current_player.hand)

            elif card.card_type != CardType.WILD and card.card_type != CardType.WILD_DRAW_4:
                if card.value != self.current_value and card.color != self.current_color:
                    print(f"Please choose a card with either "
                          f"the color {self.current_color.name} or the value {self.current_value}")
                else:
                    return card
            elif card.card_type == CardType.WILD or card.card_type == CardType.WILD_DRAW_4:
                return card

    def _get_starting_card(self):
        while True:
            starting_card = self.deck.take_cards(1)
            if starting_card.card_type != CardType.WILD_DRAW_4 \
                    and starting_card.card_type != CardType.WILD_DRAW_4:
                return starting_card
            else:
                self.deck.card_list += starting_card

    def _change_current_card(self, card):
        self.current_card = card
        self.current_color = card.color
        self.current_value = card.value

    def _pick_new_color(self):
        print("You have played a wild card, please pick a new color, red, blue, green, or yellow.")
        while True:
            choice = str(input('> ')).upper()
            if choice == Color.GREEN.name:
                self.current_color = Color.GREEN
                print(f"The current color is now {self.current_color.name}")
                break
            elif choice == Color.RED.name:
                self.current_color = Color.RED
                print(f"The current color is now {self.current_color.name}")
                break
            elif choice == Color.YELLOW.name:
                self.current_color = Color.YELLOW
                print(f"The current color is now {self.current_color.name}")
                break
            elif choice == Color.BLUE.name:
                self.current_color = Color.BLUE
                print(f"The current color is now {self.current_color.name}")
                break
            else:
                print(f"You have entered an invalid color: {choice}")

    def _handle_special_card(self):
        pass

    def _start_turn(self):
        self.current_player = self.player_list.val
        if self.current_card.card_type != CardType.NUMERICAL:
            self._handle_special_card()
        print(f"It is currently {self.current_player}'s turn.")
        print(f"The current color is: {self.current_color.name}.")
        print(f"The current card is: {self.current_card}.")

    def _end_turn(self):
        if not self.direction_reversed:
            self.player_list = self.player_list.next
            self.current_player = self.player_list.val
        else:
            self.player_list = self.player_list.prev
            self.current_player = self.player_list.val
