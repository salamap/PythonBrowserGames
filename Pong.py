# Implementation of classic arcade game Pong
import simplegui
import random
import math

# initialize globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

# function spawning thge ball moving towards the left or the right 
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel		# these are vectors stored as lists, vel variable will be used to update pos variable
    ball_pos = [WIDTH / 2, HEIGHT / 2]    
    if right:						
        ball_vel = [(random.randrange(120, 240) // 60), - (random.randrange(60, 180) // 60)]
    else:
        ball_vel = [-(random.randrange(120, 240) // 60), - (random.randrange(60, 180) // 60)]
    
# event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # float variables storing paddle position and velocity
    global score1, score2		# variables to report game score
    paddle1_pos = HEIGHT / 2 	# left paddle starting position
    paddle2_pos = HEIGHT / 2	# right paddle starting position
    paddle1_vel = 0.0			# left paddle starting velocity
    paddle2_vel = 0.0			# right paddle starting velocity
    score1 = 0
    score2 = 0   
    ball_init(random.randrange(0, 2))		# randomly pick between 0 or 1, 0 is False and 1 is True, pass to ball_init() 	

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    # update each paddle's vertical position, while keeping paddle on the screen
    if (paddle1_pos > PAD_HEIGHT / 2) and (paddle1_pos + PAD_HEIGHT / 2 < HEIGHT):
        paddle1_pos += paddle1_vel
    elif (paddle1_pos <= PAD_HEIGHT /2) and (paddle1_vel > 0):
        paddle1_pos += paddle1_vel
    elif (paddle1_pos + PAD_HEIGHT / 2 >= HEIGHT) and (paddle1_vel < 0):
        paddle1_pos += paddle1_vel
    if (paddle2_pos > PAD_HEIGHT / 2) and (paddle2_pos + PAD_HEIGHT / 2 < HEIGHT):
        paddle2_pos += paddle2_vel
    elif (paddle2_pos <= PAD_HEIGHT /2) and (paddle2_vel > 0):
        paddle2_pos += paddle2_vel
    elif (paddle2_pos + PAD_HEIGHT / 2 >= HEIGHT) and (paddle2_vel < 0):
        paddle2_pos += paddle2_vel
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")  
    # draw paddles
    c.draw_polygon([(0, paddle1_pos - PAD_HEIGHT / 2),(PAD_WIDTH, paddle1_pos - PAD_HEIGHT / 2), (PAD_WIDTH, paddle1_pos + PAD_HEIGHT / 2), (0, paddle1_pos + PAD_HEIGHT / 2)], 1, "white", "white")
    c.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos - PAD_HEIGHT / 2),(WIDTH, paddle2_pos - PAD_HEIGHT / 2), (WIDTH, paddle2_pos + PAD_HEIGHT / 2), (WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT / 2)], 1, "red", "red")
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[0] - PAD_WIDTH <= BALL_RADIUS :
        if math.fabs(ball_pos[1] - paddle1_pos) < PAD_HEIGHT / 1.75:	# if the left paddle is hit the ball reflects,  
            ball_vel[0] = - ball_vel[0]									# dividing by 1.75 is for the purpose of catching the paddle edge
            ball_vel[0] = (ball_vel[0] * 1.1)
            ball_vel[1] = (ball_vel[1] * 1.1)
        else :															# if the paddle is not hit, right player scores
            ball_init(True)
            score2 += 1
    if WIDTH - PAD_WIDTH - ball_pos[0] <= BALL_RADIUS :
        if math.fabs(ball_pos[1] - paddle2_pos) < PAD_HEIGHT / 1.75 :	# if the right paddle is hit the ball reflects
            ball_vel[0] = - ball_vel[0]									# dividing by 1.75 is for the purpose of catching the paddle edge
            ball_vel[0] = (ball_vel[0] * 110) // 100
            ball_vel[1] = (ball_vel[1] * 110) // 100
        else :															# if the paddle is not hit, left player scores
            ball_init(False)
            score1 += 1
    if ball_pos[1] <= BALL_RADIUS :		  								# reflect off top edge
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS :						# reflect off bottom edge
        ball_vel[1] = - ball_vel[1]     
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 0.01, "lime", "lime")
    c.draw_text(str(score1), (140, 50), 30, "white")
    c.draw_text(str(score2), (440, 50), 30, "red")
    
def keydown(key):						# when player pushes key, paddle velocity is updated by variable acc
    global paddle1_vel, paddle2_vel		# vel variable will updated paddle pos variable
    acc = 10
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc

def keyup(key):							# when player releases key, paddle velocity becomes zero
    global paddle1_vel, paddle2_vel		# vel variable will updated paddle pos variable
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0 
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)

# start frame
init()
frame.start()
