import os, pygame, random

suits = ('H','D','C','S')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11}

class Card():

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.back_image = pygame.image.load('misc/back.jpg').convert()
        self.image_key = self.rank + self.suit
    
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck():
    
    def __init__(self):
        self.deck = []
        self.deck_images = {}
        self.image_keys = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank,suit))
                self.image_keys.append(Card(rank,suit).image_key)

        for filename in os.listdir('cards'):
            if filename.endswith('.jpg'):
                path = os.path.join('cards', filename)
                filename_key = filename[:-4]
                self.deck_images[filename_key] = pygame.image.load(path).convert()
    
    def __str__(self):
        deck_total = ''
        for card in self.deck:
            deck_total = deck_total + '\n' + card.__str__()
        return 'The deck contains ' + str(len(self.deck)) + ' cards:'+ deck_total

    def shuffle(self):
        random.shuffle(self.deck)
        random.shuffle(self.image_keys)
        
    def deal(self):
        try:
            dealt_card = self.deck.pop()
        except:
            dealt_card = pygame.image.load('misc/empty.jpg').convert()

        try:
            dealt_key = dealt_card.image_key
            self.image_keys.remove(dealt_key)
        except:
            dealt_card = pygame.image.load('misc/empty.jpg').convert()
            dealt_key = dealt_card
        return dealt_card

class Hand():

    def __init__(self):
        self.hands_cards = []
        self.hand_value = 0
        self.aces = 0
    
    def add_card(self, card):
        self.hands_cards.append(card)
        self.hand_value += values[card.rank]

        if card.rank == 'A':
            self.aces += 1

    def ace_adjustment(self):
        while self.hand_value > 21 and self.aces > 0:
            self.hand_value -= 10
            self.aces -= 1

class Chips():

    def __init__(self, total = 200):
        self.total = total
        self.bet = 0
        if self.total <= 0:
            self.total = 0

    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
