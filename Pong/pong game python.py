import turtle
import random

# WINDOW
win = turtle.Screen()
win.title("Pong")
win.bgcolor("black")
win.setup(width=1000, height=600)
win.tracer(0)

# Create PADDLE A
paddlea = turtle.Turtle()
paddlea.speed(0)
paddlea.shape("square")
paddlea.color("blue")
paddlea.shapesize(stretch_wid=8, stretch_len=1)
paddlea.penup()
paddlea.goto(-450, 0)

# Create PADDLE B
paddleb = turtle.Turtle()
paddleb.speed(0)
paddleb.shape("square")
paddleb.color("blue")
paddleb.shapesize(stretch_wid=8, stretch_len=1)
paddleb.penup()
paddleb.goto(450, 0)

# Create BALL OBJECT
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0,0)
ball.dx = random.choice([-4,4])
ball.dy = random.choice([-4,4])

# SCORING
ascore = 0
bscore = 0
gameover = False
serving = True
servetimer = 0
WINSCORE = 5
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("0 - 0", align="center", font=("Arial", 24, "normal"))

# Print scoreboard in center of screen
def show_message(text): 
    pen.clear()
    pen.goto(0,0)
    pen.write(text, align="center", font=("Arial", 24, "bold"))

# Update score
def updatescore():
    pen.clear()
    pen.goto(0,250)
    pen.write(f"{ascore} - {bscore}", align="center", font=("Arial", 24, "normal"))

# Reset ball when a point is made
def resetball():
    ball.goto(0,0)
    ball.dx = random.choice([-4,4])
    ball.dy = random.choice([-4,4])
    
# Play again button / Reset scores
def playagain():
    pen.clear()
    global ascore, bscore, gameover, serving, servetimer
    ascore = 0
    bscore = 0
    servetimer = 0
    gameover = False
    serving = True

# Quit program
def quitgame():
    win.bye()

# CREATE PADDLE MOVEMENT
def paddlea_up():
    if paddlea.ycor() < 220:
        paddlea.sety(paddlea.ycor() + 80)
          
def paddlea_down():
    if paddlea.ycor() > -220:
        paddlea.sety(paddlea.ycor() - 80)
    
def paddleb_up():
    if paddleb.ycor() < 220:
        paddleb.sety(paddleb.ycor() + 80)
    
def paddleb_down():
    if paddleb.ycor() > -220:
        paddleb.sety(paddleb.ycor() - 80)
    
# Assign keystrokes
win.listen()
win.onkeypress(paddlea_up, "w")
win.onkeypress(paddlea_down, "s")
win.onkeypress(paddleb_up, "Up")
win.onkeypress(paddleb_down, "Down")
win.onkeypress(playagain, "y")
win.onkeypress(quitgame, "n")

# Game loop
try:
    while True:
        win.update()
        
        # 
        if serving:
            servetimer += 1
            if servetimer > 180:
                servetimer = 0
                serving = False
            continue
        
        if not gameover:
            # MOVE BALL
            ball.setx(ball.xcor() + ball.dx)
            ball.sety(ball.ycor() + ball.dy)
        
            # CREATE TOP & BOTTOM BORDERS FOR BALL
            if ball.ycor() > 290 or ball.ycor() < -290:
                ball.dy *= -1
            
            # RIGHT WALL SCORING
            if ball.xcor() > 490:
                ascore += 1
                updatescore()
                resetball()
                serving = True
            
            # LEFT WALL SCORING
            if ball.xcor() < -490:
                bscore += 1
                updatescore()
                resetball()
                serving = True
                
            # PADDLE A COLLISION WITH BALL
            if (-450 < ball.xcor() < -440 and
                paddlea.ycor() - 80 < ball.ycor() < paddlea.ycor() + 80):
                ball.setx(-440)
                ball.dx *= -1
                
            # PADDLE B COLLISION WITH BALL
            if (440 < ball.xcor() < 450 and
                paddleb.ycor() - 80 < ball.ycor() < paddleb.ycor() + 80):
                ball.setx(440)
                ball.dx *= -1
                
            # IF PLAYER REACHES WINSCORE, END THE GAME AND PRINT WINNER
            if ascore == WINSCORE or bscore == WINSCORE:
                gameover = True
                winnerplayer = "Player A" if ascore == WINSCORE else "Player B"
                show_message(f"Game Over!\n{winnerplayer} Wins!\n\nPlay Again? (Y/N)")
except turtle.Terminator:
    pass


            
            
        
        
        
            


            
        
        
    
        
        