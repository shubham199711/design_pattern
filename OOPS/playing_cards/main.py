from enum import Enum, auto

from typing import List

class Card:
    @property
    def card_value(self) -> int:
        raise NotImplementedError()
    
    def __lt__(self, other) -> bool:
        return self.card_value < other.card_value
    
class Suit(Enum):
    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()
    SPADES = auto()

class JokerColor(Enum):
    RED = auto()
    BLACK = auto()

class JokerCard(Card):
    COLORS = {
        "Red": JokerColor.RED,
        "Black": JokerColor.BLACK,
    }
    COLOR_NAMES = {e: n for n, e in COLORS.items()}

    def __init__(self, color: str):
        super().__init__()
        self.__color = self.COLORS[color]
        self.__value = 14 # more then other cards
    
    @property
    def card_value(self):
        return self.__value
    
    def __str__(self):
        return f"{self.COLOR_NAMES[self.__color]} Joker"

    
class PlayingCard(Card): # single card
    SUITS = {
        'Clubs' : Suit.CLUBS,
        'Diamonds': Suit.DIAMONDS,
        'Hearts' : Suit.HEARTS,
        'Spades': Suit.SPADES
    }
    SUIT_NAMES = { e: n for n, e in SUITS.items()}
    VALUES = {
        'A': 1,
        **{str(x): x for x in range(2, 11)},
        'J': 11,
        'Q': 12,
        'K': 13
    }
    VALUE_NAMES = {v:k for k, v in VALUES.items()}
    def __init__(self, suit: str, value: str):
        super().__init__()
        self.__suit = self.SUITS[suit]
        self.__value = self.VALUES[value]
    
    @property
    def card_value(self):
        return self.__value
    
    def __str__(self) -> str:
        return f"{self.VALUE_NAMES[self.__value]} of {self.SUIT_NAMES[self.__suit]}"
    


class Hand(Card):
    def __init__(self, cards: List[Card]):
        super().__init__()
        self.card = cards
    
    def __str__(self):
        return ", ".join(str(_str) for _str in self.card)
    
    def __lt__(self, other):
        for i, j in zip(sorted(self.card, reverse=True), sorted(other.card, reverse=True)):
            if i < j:
                return True
            elif i > j:
                return False
        return False


class Game:
    def __init__(self):
        self.__card: List[Card] = []
        self.__hand: list[Hand] = []

    def add_card(self, suit: str, value: str) -> None:
        self.__card.append(PlayingCard(suit=suit, value=value))

    def card_string(self, card: int) -> str:
        return str(self.__card[card])

    def card_beats(self, card_a: int, card_b: int) -> bool:
        return self.__card[card_a] > self.__card[card_b]

    def add_joker(self, color: str) -> None:
        self.__card.append(JokerCard(color=color))

    def add_hand(self, card_indices: List[int]) -> None:
       self.__hand.append(Hand(cards=[self.__card[x] for x in card_indices]))

    def hand_string(self, hand: int) -> str:
        return str(self.__hand[hand])

    def hand_beats(self, hand_a: int, hand_b: int) -> bool:
        return self.__hand[hand_a] > self.__hand[hand_b]

if __name__ == "__main__":
    game = Game()
    suit, value = input().split()
    game.add_card(suit, value)
    print(game.card_string(0))
    suit, value = input().split()
    game.add_card(suit, value)
    print(game.card_string(1))
    print("true" if game.card_beats(0, 1) else "false")