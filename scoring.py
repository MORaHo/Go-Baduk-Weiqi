import numpy 

#global variables
EMPTY = 0
BLACK = 1
WHITE = 2
MARKER = 4
OFFBOARD = 7
LIBERTY = 8

#count
liberties = []
block = []
size = 13
board_for_scoring = []
white_point = 0
black_point = 0
points = [0,black_point,white_point]
colours = [0,BLACK,WHITE]


def make_board():
    for x in range(1,size+1):
        for y in range(1,size+1):
            board_for_scoring.append(0)
                
    board_for_scoring = numpy.array(board_for_scoring).reshape(size,size)
    return board_for_scoring

check_board = make_board()

def count(x,y,colour):

    #initialize piece
    piece = board[y][x]
    #skip offboard squares
    if piece == OFFBOARD: return
    #if there's a stone at square
    if piece and piece & colour and (piece & MARKER) == 0:
        
        #save stone coords
        block.append((y,x))
        #mark the stone
        board[y][x] |= MARKER
        #look for neighbours recursively
        count(x,y-1,colour) #walk north
        count(x-1,y,colour) #walk east
        count(x,y+1,colour) #walk south
        count(x+1,y,colour) #walk west

    #if square is empty
    elif piece == EMPTY:

        #mark liberty
        board[y][x] = LIBERTY
        #save liberties
        liberties.append((y,x))

    return liberties    

#clear groups
def clear_groups():
    global liberties, block

    #clear block and liberties lisits
    block = []
    liberties = []

#restore board after counting stones and liberties


board = []

def captures():

    #loop over the board squares
    for y in range(len(board)):
        for x in range(len(board)):
            
            #init piece
            piece = board[y][x]

            #skip offboard
            if piece == OFFBOARD: continue

            #if stone belongs to given colour
            if not check_board[y][x]:
                
                color = piece
                #count liberties
                count(x,y,color)

                empty_poss = [pos for pos in liberties if board[pos[0]][pos[1]] == EMPTY]
                for pos in empty_poss:
                    count(pos[1],pos[0],color)
                    if len(liberties) == 0 and []:

                        index = BLACK*(WHITE == color) + WHITE*(BLACK == color)
                        points[index] += 1
                #if no liberties remove the stones
                if len(empty_poss) == 0: 
                    index = BLACK*(WHITE == piece) + WHITE*(BLACK == piece)
                    points[index] += len(block)


                if piece 