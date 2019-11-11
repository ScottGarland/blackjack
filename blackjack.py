import pygame
from bjclass import *
from bjfuncs import *

pygame.init()
pygame.display.set_caption("Blackjack")

gamegreen = (26,119,67)
black = (0,0,0)
display_height = 768
display_width = 1024
screen = pygame.display.set_mode((display_width,display_height))

#Placements for the cards in play
#most card image dimensions are 173x264 86x132
deck_placement = [(800,50)]
deal_placement = [(50,50),(105,50),(160,50),(215,50),(270,50),(325,50),(380,50),(435,50),(490,50),(545,50)]
play_placement = [(50,454),(105,454),(160,454),(215,454),(270,454),(325,454),(380,454),(435,454),(490,454),(545,454)]
back = Card('rank','suit').back_image

#User input and coords for bet
user_string = ''
coord_x = 800
coord_y = 650

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
