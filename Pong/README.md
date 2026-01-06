# Pong

## This project is a simple pong game using pythons turtle graphics library. In this game two players go head-to-head by controlling the y cordinate of paddles to bounce a ball back and forth until a point is scored, similar to air hockey.

## Controls
*Player A*
* Move Up: 'W'
* Move Down: 'S'

*Player B*
* Move Up: 'Up Arrow'
* Move Down: 'Down Arrow'

## Features
* Two-player controls
* Score tracking
* Ball serving delay
* Replay or quit options
* Ball collision with paddle
* Boundries for paddles to prevent leaving screen
* Press 'n' anytime to quit program

## How It Works
* Continuous game loop updating the screen
* Move ball using values 'dx' and 'dy'
* Resets ball to middle with a serve delay after a point is made
* Ends the game when a player reaches WINSCORE which is hardcoded to 5
* After 5 Points 'Y' to Play Again and 'N' to Quit Program

## Requirements
* Python 3.9+

