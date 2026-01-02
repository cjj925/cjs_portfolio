import turtle
import random

## WINDOW
win = turtle.Screen()
win.title("Pong")
win.bgcolor("black")
win.setup(width=1000, height=600)
win.tracer(0)

## PADDLE Aa
paddlea = turtle.Turtle()
paddlea.speed(0)
paddlea.shape("square")
paddlea.color("blue")
paddlea.shapesize(stretch_wid=8, stretch_len=1)
paddlea.penup()
paddlea.goto(-450, 0)

## PADDLE B
paddleb = turtle.Turtle()
paddleb.speed(0)
paddleb.shape("square")
paddleb.color("blue")
paddleb.shapesize(stretch_wid=8, stretch_len=1)
paddleb.penup()
paddleb.goto(450, 0)

# BALL OBJECT
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0,0)
ball.dx = 2
ball.dy = 2

## SCORE
ascore = 0
bscore = 0
gameover = False
serving = True
servetimer = 0
WINSCORE = 2
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("0 - 0", align="center", font=("Arial", 24, "normal"))

def show_message(text):
    pen.clear()
    pen.goto(0,0)
    pen.write(text, align="center", font=("Arial", 24, "bold"))

def updatescore():
    pen.clear()
    pen.goto(0,250)
    pen.write(f"{ascore} - {bscore}", align="center", font=("Arial", 24, "normal"))

def resetball():
    ball.goto(0,0)
    ball.dx = random.choice([-4,4])
    ball.dy = random.choice([-4,4])
    
def playagain():
    pen.clear()
    global ascore, bscore, gameover, serving, servetimer
    ascore = 0
    bscore = 0
    servetimer = 0
    gameover = False
    serving = True

def quitgame():
    win.bye()

## PADDLE MOVEMENT
def paddlea_up():
    paddlea.sety(paddlea.ycor() + 40)
    
def paddlea_down():
    paddlea.sety(paddlea.ycor() - 40)
    
def paddleb_up():
    paddleb.sety(paddleb.ycor() + 40)
    
def paddleb_down():
    paddleb.sety(paddleb.ycor() - 40)
    
win.listen()
win.onkeypress(paddlea_up, "w")
win.onkeypress(paddlea_down, "s")
win.onkeypress(paddleb_up, "Up")
win.onkeypress(paddleb_down, "Down")
win.onkeypress(playagain, "y")
win.onkeypress(quitgame, "n")

try:
    while True:
        win.update()
        
        if serving:
            servetimer += 1
            if servetimer > 180:
                servetimer = 0
                serving = False
            continue
        
        if not gameover:
            ## MOVE BALL
            ball.setx(ball.xcor() + ball.dx)
            ball.sety(ball.ycor() + ball.dy)
        
            ## TOP & BOTTOM COLLISION
            if ball.ycor() > 290 or ball.ycor() < -290:
                ball.dy *= -1
            
            ## RIGHT WALL SCORING
            if ball.xcor() > 490:
                ascore += 1
                updatescore()
                resetball()
                serving = True
            
            ## LEFT WALL SCORING
            if ball.xcor() < -490:
                bscore += 1
                updatescore()
                resetball()
                serving = True
                
            ## PADDLE COLLISION
            
            ## PADDLE A
            if (-450 < ball.xcor() < -440 and
                paddlea.ycor() - 80 < ball.ycor() < paddlea.ycor() + 80):
                ball.dx *= -1
                
            ## PADDLE B
            if (440 < ball.xcor() < 450 and
                paddleb.ycor() - 80 < ball.ycor() < paddleb.ycor() + 80):
                ball.dx *= -1
                
            if ascore == WINSCORE or bscore == WINSCORE:
                gameover = True
                winnerplayer = "Player A" if ascore == WINSCORE else "Player B"
                show_message(f"Game Over!\n{winnerplayer} Wins!\n\nPlay Again? (Y/N)")
except turtle.Terminator:
    pass


            
            
        
        
        
            


            
        
        
    
        
        
