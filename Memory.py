# implementation of card game - Memory

import simplegui
import random
W = 50				# width of each card in pixels
H = 100				# height of card and canvas in pixels
newGame = {}		# dictionary data structure that models the board
exposed = []		# boolean list where True = card is turned over

# helper function
def init():			# initialize variables and create the game
    global exposed, newGame, count, state
    count = 0
    state = 0
    exposed = [False for i in range(0, 16)]
    newGame = getNewGame()
    move.set_text("Moves = " + str(count))

def getNewGame() :			# create a new instance of the game
    cards = range(0,8)
    game = {}				# the game is modeled by a dictionary (hash map)
    cards = cards[: 8] * 2
    random.shuffle(cards)	# shuffled deck of 16 cards
    for i in range(0, 16):
        game [i] = cards[i]	# keys correspond to card positions and values correspond to the actual cards
    return game

# define event handlers
def mouseclick(pos):
    global state, exposed, firstCard, secondCard, count
    if state == 0:
        firstCard = pos[0] // W
        exposed[firstCard] = True
        state = 1							# at this point the player has selected one card
    elif state == 1:
        if not exposed[pos[0] // W] :		# check if the next card selected is facing down
            secondCard = pos[0] // W
            exposed[secondCard] = True
            state = 2
            count += 1
            move.set_text("Moves = " + str(count)) # at this point the player has selected two cards
    else:
        if not exposed[pos[0] // W] :						# check if the next card selected is facing down   
            if newGame[secondCard] != newGame[firstCard] :	# check if previous cards match
                exposed[secondCard] = False
                exposed[firstCard] = False
            firstCard = pos[0] // W 						
            exposed[firstCard] = True						# face the next card up
            state = 1
        else :
            exposed[secondCard] = True
            exposed[firstCard] = True
                          
# cards are logically 50x100 pixels in size    
def draw(canvas):    
    for c in range(0,16) :
        if exposed[c] :				# draw the numbers of cards facing up		
            canvas.draw_text(str(newGame[c]), (c * W + 10, 75), 50, "Red")		# draw the card number stored at that key
        else :						# draw the cards facing down
            canvas.draw_polygon([(c * W, 0), (c * W + W, 0), (c * W + W, H), (c * W, H)], 2, "Black", "Lime")

frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
move = frame.add_label("")
init()
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
frame.start()
