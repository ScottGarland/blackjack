import pygame

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
