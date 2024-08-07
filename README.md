# Go Game Player
Go board game made in python and visualized using pygame, following japanese Go rules regarding Ko

## Rules of Go

Go isn't too hard of a game once you have played it, so for the rules I would recommmend:
1. Reading https://en.wikipedia.org/wiki/Go_(game)

or

2. Learning to play at https://online-go.com/ (I personally use this to play with friends)

## Description

This is a game of Go made with pygame. The game is played on the same board by two people, with alternating picks for moves. The engine is quite simple but follows all the rules of the game, including blocking a ko fight from occuring and blocking suicide. **NOTE**: This not a Go AI, any AI for this that I would develop would be on a different repository.

### Recognition

A lot of the base logic regarding the game came from this series by Chess Programming: https://www.youtube.com/watch?v=dHlan0bgr5U&list=PLmN0neTso3JzVlIQC3fwnP1qgIKp1x97X

## Requirements
Python since it's a python game and pygame which can be downloaded in command line with:

~~~
pip install pygame
~~~

## Known Problems

1. Komi (points in Go) are currently not counted, I will probably do this by using floodfill to find the surrounded area.

## (Probable) Future Development

- Ability to change the size of the board without changing directly in code, currently 13 is default.
- Graphics to show who's turn it is.
- Estimation of Komi.
- Development for web.
- LAN multiplayer.
- AI to play against
