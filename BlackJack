# Blackjack the game. No pushing and no splitting cards
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back_loc = (CARD_BACK_CENTER[0],CARD_BACK_CENTER[1])
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# global variables
in_play = False				# flag that is set when the player is no longer hitting
outcome = ""				# outcome of the game drawn on the canvas
message = ""				# message instruction drawn on the canvas
score = 0					# keeps score of the game
PLAYER_LOSES, PLAYER_BUSTS, DEALER_LOSES, DEALER_BUSTS  = 1, 2, 3, 4 	# outcome flags

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit, self.rank = suit, rank
        else:
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit
    
    def get_rank(self):			
        return self.rank
    
    def getSoftCard(self):			# Aces are the only cards with a soft value, which is 11
        if self.rank == 'A':		
            return 11
        else:
            return VALUES[self.rank]	
    
    def getHardCard(self):
        return VALUES[self.rank]	# A card's hard value is it's face value, for an Ace its 1

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + 
                          CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

class Hand:
    def __init__(self):
        self.cards = []
        self.softDelta = 0	# this variable is set only once when the first Ace is added to hand
    
    def __str__(self): 
        return str([str(c) for c in self.cards])
    
    def add_card(self, card):
        self.cards.append(card)        
        if card.getHardCard() != card.getSoftCard() and self.softDelta == 0: # set softDelta to 10 when the first Ace is added
            self.softDelta = card.getSoftCard() - card.getHardCard()
            
    def get_value(self):
        points = 0
        for c in self.cards:
            points += c.getHardCard() 		# for the cards in a hand add up all the card hard values
        
        if (points + self.softDelta) <= 21: # if Aces are present and won't bust the hand then add 10 
            return points + self.softDelta
        else:
            return points					# otherwise return the sum of the hard values
                
    def busted(self):						
        if self.get_value() > 21:			# returns true if the hand is busted and false otherwise
            return True
        else :
            return False
    
    def draw(self, canvas, p):
        for c in self.cards:				# call the draw method in the card class for each card object in the hand
            c.draw(canvas, p)
            p[0]+=78

class Deck:					# deck class contains all the shuffled cards 
    def __init__(self):
        self.cards = []
        self.cards = ([Card(suit, rank) for suit in SUITS for rank in RANKS])
    
    def shuffle(self):		# calling this method shuffles the card
        random.shuffle(self.cards)
    
    def deal_card(self):	# calling this method returns the top card in the list
        return self.cards.pop(0)
 
    def __str__(self):
        return str([str(c) for c in self.cards])

#define event handlers for buttons
def deal():
    global in_play, player_hand, dealer_hand, new_deck, message, outcome, score    
    if not in_play:
        in_play = True
        message = "Hit or Stand?"
        outcome = ""
        new_deck = Deck()							# create instance of deck and shuffle it
        new_deck.shuffle()
    
        player_hand = Hand()						# create instance of hand to be used for the player
        dealer_hand = Hand()						# create instance of hand to be used for the dealer
    
        player_hand.add_card(new_deck.deal_card())	# add a card to the player's hand
        player_hand.add_card(new_deck.deal_card())
  
        dealer_hand.add_card(new_deck.deal_card())	# add a card to the dealer's hand
        dealer_hand.add_card(new_deck.deal_card())
    else:
        printResult(PLAYER_LOSES)					# if the player hits deal in the middle of a round they lose
        score -= 1
        in_play = False

def hit():		# add a card to the players hand everytime the hit button is pressed
    global in_play, player_hand, score
    if in_play and not player_hand.busted():
        player_hand.add_card(new_deck.deal_card())
        if player_hand.busted(): 		# check if player busts 
            printResult(PLAYER_BUSTS)
            score -= 1
            in_play = False
    
def stand():	# if stand is pressed then the dealer hits until they bust or has value 17 or more 
    global in_play, dealer_hand, new_deck, score
    if in_play :
        in_play = False
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(new_deck.deal_card())
       
        if dealer_hand.get_value() >= player_hand.get_value() and not dealer_hand.busted():                
            printResult(PLAYER_LOSES)
            score -= 1
        elif dealer_hand.busted():
            printResult(DEALER_BUSTS)
            score += 1
        else :
            printResult(DEALER_LOSES)
            score += 1

def printResult(flag):	# this method prints the outcome depending on the value that is paased in
    global message, outcome
    if flag == 1:
        outcome = "You Lose, House Wins!"
    elif flag == 2:
        outcome = "You Bust, House Wins!"
    elif flag == 3:
        outcome = "Dealer Loses, You Win!"
    else :
        outcome = "Dealer Busts, You Win!"
    message = "New Deal?"
    return

# draw handler    
def draw(canvas):
    global message, score
    canvas.draw_text("BLACK JACK", (180, 250), 40, "Black")
    canvas.draw_text("PLAYER", (10, 450), 25, "Navy")
    canvas.draw_text("DEALER", (10, 170), 25, "Maroon")
    canvas.draw_text("Score " + str(score), (450, 450), 25, "Navy")
    canvas.draw_line([0, 300], [600, 300], 5, "White")
    canvas.draw_text(message, (225, 285), 25, "Silver")
    canvas.draw_text(outcome, (150, 350), 25, "Silver")
    player_hand.draw(canvas, [5, 475])
    if in_play:		# if player is still in play keep one card faced down
        canvas.draw_image(card_back, card_back_loc, CARD_BACK_SIZE, [CARD_BACK_CENTER[0] + 5, CARD_BACK_CENTER[1] + 26], CARD_BACK_SIZE)
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(dealer_hand.cards[1].get_rank()), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(dealer_hand.cards[1].get_suit()))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [115, 74], CARD_SIZE)
    else:			# otherwise display all cards in dealer's hand
        dealer_hand.draw(canvas, [5, 25])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deal()

# get things rolling
frame.start()
