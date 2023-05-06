# Go-Baduk-Weiqi
Go board game made in python and visualized using pygame

## Rules of Go

Go isn't too hard of a game once you have played it, so for the rules I would recommmend:
1. Reading https://en.wikipedia.org/wiki/Go_(game)

or

2. Learning to play at https://online-go.com/ (I personally use this to play with friends)

## Known Problems

1. Currently accepts inputs outside of technically legal board bounds
2. Algorithm for checking if a move is legal or not is too slow, so if there the board it clicked to quickly a technically illegal move can be played.
3. Ko (points in Go) are currently not counted, I will probably do this by using floodfill to find the surrounded area.
