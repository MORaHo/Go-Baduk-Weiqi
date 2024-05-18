import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from pygame.locals import *
import numpy

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

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
seki_count = 0
seki_liberties = []
run = True
board = None

#gui variables
alt = 40
#white = (255,243,0)
white = (255,255,255)
#black = (0,116,255)
black = (0,0,0)
line_black = (0,0,0)
board_bg =  (171,144,88)
color = BLACK
pg_color = black
size = 13
colours  = [0,black,white]
width = size * alt + alt
height = size * alt + alt
pre_board = None
post_board = None

#initializing pygame window
pg.init()
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height),0,32)
pg.display.set_caption("Go")
pygame_icon = pg.image.load(os.path.join(__location__, 'app_icon.png'))
pg.display.set_icon(pygame_icon)

def set_board_vals(size):
    vals = []
    for a in range(size+2):
        for b in range(size+2):
            if a == 0 or b == 0 or b == size+1 or a == size+1: val = 7
            else: val = 0
            vals.append(val)
    return vals

#Piece board
null_vals = []
val = [None]
for a in range(size):
    for b in range(size):
        null_vals.append(val)
piece_board = numpy.array(null_vals,dtype=object).reshape(size,size)

#Text Board
vals=set_board_vals(size)
board = numpy.array(vals,dtype=int).reshape(size+2,size+2)

class Piece():

    def __init__(self,pos,color):

        super().__init__()
        self.show_color = color
        pg.draw.circle(screen,color,(pos[0],pos[1]),20)

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

#remove captured stones
def clear_block():

    #clears the elements in the block of elements which is captured
    for i in range(len(block)): 
        y = block[i][0]
        x = block[i][1]
        placed_piece = piece_board[y-1][x-1]
        del placed_piece
        piece_board[y-1][x-1] = None
        board[y][x] = EMPTY

#clear groups
def clear_groups():
    global liberties, block

    #clear block and liberties lisits
    block = []
    liberties = []

#restore board after counting stones and liberties
def restore_board():
    #clear groups
    clear_groups()

    #unmark stones
    for y in range(len(board)):
        for x in range(len(board)):

            #if square is on board
            if board[y][x] != OFFBOARD:
                #restore piece
                val = board[y][x]
                new_val = val & 3
                board[y][x] = new_val

#clear board
def clear_board():
    #clear groups
    clear_groups()

    #clears the board
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] != OFFBOARD: board[y][x] = 0

def draw_board() -> None:

    screen.fill(board_bg)

    for i in range(1,size+1):
        #horizontal lines
        pg.draw.line(screen,line_black,(alt*i,alt),(i*alt,width-alt),1)
        #vertical lines
        pg.draw.line(screen,line_black,(alt,i*alt),(height-alt,i*alt),1)

    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == 1 or board[y][x] == 2:
                try:
                    pos_x = ((x-1)*alt)+alt
                    pos_y = (y-1)*alt+alt
                    pos_s = (pos_x,pos_y)
                    #board has values of 1 and 2 for black and white so we can associate this with list positions in the colours list
                    piece_colour = colours[board[y][x]]
                    piece_board[y-1][x-1] = Piece(pos_s,piece_colour)
                except:
                    pass
    pg.display.flip()

def captures(color,pg_color):

    global check
    global seki_count
    check = False

    #loop over the board squares
    for y in range(len(board)):
        for x in range(len(board)):
            
            #init piece
            piece = board[y][x]

            #skip offboard
            if piece == OFFBOARD: continue

            #if stone belongs to given colour
            if piece & color:
                
                #count liberties
                count(x,y,color)

                #if no liberties remove the stones
                if len(liberties) == 0: 
                    
                    #clear block
                    clear_block()

                    #if the move is a "ko" move but causes the capture of stones, then it is not allowed, unless it is the second move, in which case it is dealt afterwards
                    if seki_count == 0:
                        #print("here")
                        draw_board()
                        #switching colours for the next move
                        if pg_color == black: color = WHITE;pg_color = white
                        else: pg_color = black; color = BLACK

                        #returns False, which means that the move has caused a capture (the logic worked out that way in the initial development and i'm not sure what it would affect if it is changed)
                        check = True
                        seki_count = 1
                        continue

                #restore the board
                restore_board()

    return check

def set_stone(y,x,color):

    #making move on the board
    board[y][x] = int(color)

def get_pos():

    #getting mouse position and returning it
    pos = pg.mouse.get_pos()
    x = pos[0]
    y = pos[1]
    return y,x

draw_board()

while run:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run =False

        if event.type == pg.MOUSEBUTTONDOWN:

            #getting the position of the mouse click and converting it relative pixels on the screen
            mouse_pos = get_pos()
            pos_y = ((mouse_pos[0]-alt/2)//alt)*alt+alt 
            pos_x = ((mouse_pos[1]-alt/2)//alt)*alt+alt
            pos_s = (pos_x,pos_y)
            #checking is the click is within the limits of the board
            if int((pos_y//alt)-1) < 0 or int((pos_x//alt)-1) < 0: continue
            if int((pos_y//alt)-1) > size-1 or int((pos_x//alt)-1) > size-1: continue
            #checking if the move place is filled or not
            if piece_board[int((pos_y//alt)-1),int((pos_x//alt)-1)] != None:
                continue

            else:
                #checking if the move is part of is the secondary move to a ko fight
                pre_board = numpy.copy(board)
                set_stone(int((pos_y//alt)),int((pos_x//alt)),color)
                if seki_count == 1:
                    #print("or here")
                    captures(color,pg_color)
                    post_board = numpy.copy(board)
                    #if it is continue until the ko fight is not initiated
                    if (pre_board == post_board).all():
                        continue
                    #if not secondary move to the ko fight, then place the stone
                    else:
                        if pg_color == black: color = WHITE;pg_color = white
                        else: pg_color = black; color = BLACK
                        draw_board()
                        seki_count = 0
                        #continue

                #any move that doesn't fall within the rules for a ko fight
                else:
                    seki_count = 0
                    if captures(3-color,pg_color) == False and captures(color,pg_color) == True:
                        continue

                    captures_have_been_had = captures(3-color,pg_color)
                    #placing stone
                    piece_board[int((pos_y//alt)-1)][int((pos_x//alt)-1)] = Piece(pos_s,pg_color)
                    #checking if there is a capture due to the move, if so redraw the board (cannot just delete since they are drawn, so you have to redraw)
                    if captures_have_been_had and seki_count == 0: draw_board()
                    #switching colours for the next move
                    if pg_color == black: color = WHITE;pg_color = white
                    else: pg_color = black; color = BLACK

    pg.display.update()

pg.quit()