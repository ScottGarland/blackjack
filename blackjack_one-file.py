import os, pygame, random

pygame.init()
pygame.display.set_caption("Blackjack")

suits = ('H','D','C','S')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11}

gamegreen = (26,119,67)
black = (0,0,0)
display_height = 768
display_width = 1024
screen = pygame.display.set_mode((display_width,display_height))

#Placements for the cards in play
#most card image dimensions are 173x264
deck_placement = [(800,50)]
deal_placement = [(50,50),(105,50),(160,50),(215,50),(270,50),(325,50),(380,50),(435,50),(490,50),(545,50)]
play_placement = [(50,454),(105,454),(160,454),(215,454),(270,454),(325,454),(380,454),(435,454),(490,454),(545,454)]

#User input and coords for bet
user_string = ''
coord_x = 800
coord_y = 650

### Classes ###
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

### Functions ###
#creates text object
def text_object(text,font,colour):
    text_surface = font.render(text,True,colour)
    return text_surface, text_surface.get_rect()

#blits text object to screen
def message_display(screen,text,fontsize,colour,x,y):
    large_text = pygame.font.Font('freesansbold.ttf', fontsize)
    text_surface, text_rect = text_object(text, large_text, colour)
    text_rect.center = (x,y)
    screen.blit(text_surface, text_rect)

#takes the user's bet
def take_bet(chips,user_string):
    
    try:
        chips.bet = int(user_string)
    except:
        chips.bet = 0
    if chips.bet > chips.total:
        chips.bet = 0
        chips.total = chips.total

def hit(deck,hand,card):
    hand.add_card(card)
    hand.ace_adjustment()

def hit_or_stand(deck,hand,play):
    
    while True:
        ask_player = input('Would you like to hit or stand?')
        if ask_player[0].lower() == 'h':
            print('Player hits.')
            hit(deck,hand)
        elif ask_player[0].lower() == 's':
            print('Player stands.')
            play = False
        else:
            print('Please input "hit" ("h") or "stand" ("s")')
        break

#game outcomes
def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Tie! It's a push.")

#Title screen features
def title_screen():
    screen.fill(gamegreen)
    ace_of_spades = pygame.image.load('cards/AS.jpg').convert()
    king_of_hearts = pygame.image.load('cards/KH.jpg').convert()
    message_display(screen,'Welcome to Blackjack!',65,black,(display_width/2),(display_height/2)-300)
    message_display(screen,'spacebar = start/reset',50,black,(display_width/2),(display_height/2)-250)
    message_display(screen,'Order of play: deal, bet, hit/stand',50,black,(display_width/2),(display_height/2)-200)
    screen.blit(king_of_hearts,((display_width/2)-173,(display_height/2)-132))
    screen.blit(ace_of_spades,((display_width/2),(display_height/2-132)))
    message_display(screen,'type/backspace/DELETE bet, B = confirm',50,black,(display_width/2),(display_height/2)+200)
    message_display(screen,'D = deal  S = stand  H = hit',50,black,(display_width/2),(display_height/2)+250)
    message_display(screen,'T = return to title screen',50,black,(display_width/2),(display_height/2)+300)

#blits value of chips and current bet
def money():
    message_display(screen,'Bet: $'+user_string,50,black,coord_x,coord_y)
    message_display(screen, 'Chips: $'+str(chips.total),50,black,coord_x,coord_y+75)

count = 1
def play_counter():
    global count
    count = count + 1
    return count

back = Card('rank','suit').back_image
deck = Deck()
deck.shuffle()
chips = Chips()
player = Hand()
dealer = Hand()

title_screen()

game = True
play = True
begin = True

while game:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.unicode == '1' or event.unicode == '2' or event.unicode == '3' or event.unicode == '4' or \
            event.unicode == '5' or event.unicode == '6' or event.unicode == '7' or event.unicode == '8' or \
            event.unicode == '9' or event.unicode == '0':
                user_string += event.unicode
                #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
                pygame.draw.rect(screen,gamegreen,(512,384,512,384))
                screen.blit(back,deck_placement[0])
                money()

            if event.key == pygame.K_BACKSPACE:
                user_string = user_string[:-1]
                pygame.draw.rect(screen,gamegreen,(512,384,512,384))
                screen.blit(back,deck_placement[0])
                money()
            
            if event.key == pygame.K_DELETE:
                user_string = ''
                pygame.draw.rect(screen,gamegreen,(512,384,512,384))
                screen.blit(back,deck_placement[0])
                money()

            if event.key == pygame.K_ESCAPE:
                game = False

            if event.key == pygame.K_SPACE:
                screen.fill(gamegreen)
                screen.blit(back,deck_placement[0])
                message_display(screen,'Deal the cards! (D)',40,black,coord_x,coord_y-170)
                user_string = ''
                deck = Deck()
                deck.shuffle()
                chips = Chips()
                player = Hand()
                dealer = Hand()
                money()

            if event.key == pygame.K_d:
                screen.fill(gamegreen)
                screen.blit(back,deck_placement[0])
                screen.blit(back,deal_placement[0])
                screen.blit(back,deal_placement[1])
                screen.blit(back,play_placement[0])
                screen.blit(back,play_placement[1])
                message_display(screen,'Place your bet! (B)',40,black,coord_x,coord_y-170)
                money()
                dealer.hands_cards = []
                dealer.hand_value = 0
                player.hand_cards = []
                player.hand_value = 0

            if event.key == pygame.K_b:
                count = 1
                screen.fill(gamegreen)
                screen.blit(back,deck_placement[0])
                take_bet(chips,user_string)
                pygame.draw.rect(screen,gamegreen,(512,384,512,384))

                if chips.bet == 0:
                    message_display(screen,'Invalid bet in play',40,black,coord_x,coord_y-130)
                    message_display(screen,'Re-deal or no-bet play',40,black,coord_x,coord_y-90)
                    message_display(screen,'Hit (H) or Stand (S)',40,black,coord_x,coord_y-50)
                else:
                    message_display(screen,'Hit (H) or Stand (S)',40,black,coord_x,coord_y-90)
                    message_display(screen,'Bet confirmed',40,black,coord_x,coord_y-50)

                money()
                screen.blit(back,deal_placement[0])

                dealt_1 = deck.deal()
                dealt_2 = deck.deal()
                dealt_3 = deck.deal()

                try:
                    screen.blit(deck.deck_images[dealt_1.image_key],deal_placement[1])
                    #pygame.draw.rect(screen,gamegreen,(0,384,512,384))
                    screen.blit(deck.deck_images[dealt_2.image_key],play_placement[0])
                    screen.blit(deck.deck_images[dealt_3.image_key],play_placement[1])
                except:
                    screen.fill(gamegreen)
                    empty = pygame.image.load('misc/empty.jpg').convert()
                    screen.blit(empty,deck_placement[0])
                    message_display(screen,'Empty deck! Spacebar to reset',50,black,(display_width/2),(display_height/2))

                try:
                    hit(deck,dealer,dealt_1)
                    hit(deck,player,dealt_2)
                    hit(deck,player,dealt_3)
                except:
                    screen.fill(gamegreen)
                    empty = pygame.image.load('misc/empty.jpg').convert()
                    screen.blit(empty,deck_placement[0])
                    message_display(screen,'Empty deck! Spacebar to reset',50,black,(display_width/2),(display_height/2))

            if event.key == pygame.K_h:
                i = play_counter()
                hit_card = deck.deal()

                try:
                    hit(deck,player,hit_card)
                    screen.blit(deck.deck_images[hit_card.image_key],play_placement[i])
                except:
                    screen.fill(gamegreen)
                    empty = pygame.image.load('misc/empty.jpg').convert()
                    screen.blit(empty,deck_placement[0])
                    message_display(screen,'Empty deck! Spacebar to reset',50,black,(display_width/2),(display_height/2))

                if player.hand_value > 21:
                    message_display(screen,'Player Busts! Press S to check for push!',40,black,(display_width/2),(display_height/2))

            if event.key == pygame.K_s:
                pygame.draw.rect(screen,gamegreen,(0,340,1024,75))
                try:
                    if player.hand_value == 0:
                        hit(deck,player,dealt_2)
                        hit(deck,player,dealt_3)
                except:
                    screen.fill(gamegreen)
                    empty = pygame.image.load('misc/empty.jpg').convert()
                    screen.blit(empty,deck_placement[0])
                    message_display(screen,'Empty deck! Spacebar to reset',50,black,(display_width/2),(display_height/2))

                j = 0
                try:
                    while dealer.hand_value < 17:
                        hit(deck,dealer,deck.deal())
                except:
                    screen.fill(gamegreen)
                    empty = pygame.image.load('misc/empty.jpg').convert()
                    screen.blit(empty,deck_placement[0])
                    message_display(screen,'Empty deck! Spacebar to reset',50,black,(display_width/2),(display_height/2))

                try:
                    for item in dealer.hands_cards:
                        screen.blit(deck.deck_images[item.image_key],deal_placement[j])
                        j = j + 1
                except:
                    screen.fill(gamegreen)
                    message_display(screen,'Error! Spacebar to reset',50,black,(display_width/2),(display_height/2)-100)

                if player.hand_value > 21 and dealer.hand_value > 21:
                    push(player,dealer)
                    message_display(screen,'Both bust! Push!',65,black,(display_width/2),(display_height/2))
                    message_display(screen,'Dealer: '+str(dealer.hand_value),25,black,(display_width/2),(display_height/2)+50)
                    message_display(screen,'Player: '+str(player.hand_value),25,black,(display_width/2),(display_height/2)+75)
                    message_display(screen,'Re-deal to update chips (D)',25,black,(display_width/2),(display_height/2)+100)

                elif dealer.hand_value > 21:
                    dealer_busts(player,dealer,chips)
                    message_display(screen,'Dealer Busts!',65,black,(display_width/2),(display_height/2))
                    message_display(screen,'Dealer: '+str(dealer.hand_value),25,black,(display_width/2),(display_height/2)+50)
                    message_display(screen,'Player: '+str(player.hand_value),25,black,(display_width/2),(display_height/2)+75)
                    message_display(screen,'Re-deal to update chips (D)',25,black,(display_width/2),(display_height/2)+100)

                elif dealer.hand_value > player.hand_value:
                    dealer_wins(player,dealer,chips)
                    message_display(screen,'Dealer Wins!',65,black,(display_width/2),(display_height/2))
                    message_display(screen,'Dealer: '+str(dealer.hand_value),25,black,(display_width/2),(display_height/2)+50)
                    message_display(screen,'Player: '+str(player.hand_value),25,black,(display_width/2),(display_height/2)+75)
                    message_display(screen,'Re-deal to update chips (D)',25,black,(display_width/2),(display_height/2)+100)

                elif player.hand_value > 21:
                    player_busts(player,dealer,chips)
                    message_display(screen,'Player Busts!',65,black,(display_width/2),(display_height/2))
                    message_display(screen,'Dealer: '+str(dealer.hand_value),25,black,(display_width/2),(display_height/2)+50)
                    message_display(screen,'Player: '+str(player.hand_value),25,black,(display_width/2),(display_height/2)+75)
                    message_display(screen,'Re-deal to update chips (D)',25,black,(display_width/2),(display_height/2)+100)

                elif dealer.hand_value == player.hand_value:
                    push(player,dealer)
                    message_display(screen,'Push!',65,black,(display_width/2),(display_height/2))
                    message_display(screen,'Dealer: '+str(dealer.hand_value),25,black,(display_width/2),(display_height/2)+50)
                    message_display(screen,'Player: '+str(player.hand_value),25,black,(display_width/2),(display_height/2)+75)
                    message_display(screen,'Re-deal to update chips (D)',25,black,(display_width/2),(display_height/2)+100)

                elif dealer.hand_value < player.hand_value and player.hand_value < 21:
                    player_wins(player,dealer,chips)
                    message_display(screen,'Player Wins!',65,black,(display_width/2),(display_height/2))
                    message_display(screen,'Dealer: '+str(dealer.hand_value),25,black,(display_width/2),(display_height/2)+50)
                    message_display(screen,'Player: '+str(player.hand_value),25,black,(display_width/2),(display_height/2)+75)
                    message_display(screen,'Re-deal to update chips (D)',25,black,(display_width/2),(display_height/2)+100)

                elif player.hand_value == 21 and dealer.hand_value != 21:
                    player_wins(player,dealer,chips)
                    message_display(screen,'Player Wins!',65,black,(display_width/2),(display_height/2))
                    message_display(screen,'Dealer: '+str(dealer.hand_value),25,black,(display_width/2),(display_height/2)+50)
                    message_display(screen,'Player: '+str(player.hand_value),25,black,(display_width/2),(display_height/2)+75)
                    message_display(screen,'Re-deal to update chips (D)',25,black,(display_width/2),(display_height/2)+100)
                
                dealer.hands_cards = []
                dealer.hand_value = 0
                player.hand_cards = []
                player.hand_value = 0

            if event.key == pygame.K_t:
                title_screen()
            
        #print(event)

    pygame.display.update()
pygame.quit()
