import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from pygame.locals import *
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

#gui variables
board = None
alt = 40
run = True
white = (255,255,255)
black = (10,10,10)
board_bg =  (171,144,88)
color = BLACK
pg_color = black
size = 19
colours  = [0,black,white]
width = size * alt + alt
height = size * alt + alt
seki_count = 0

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

#Board
vals=set_board_vals(size)
board = numpy.array(vals,dtype=int).reshape(size+2,size+2)

class Piece():

    def __init__(self,pos,color):
        
        super().__init__()
        self.show_color = color
        circle = pg.draw.circle(screen,color,(pos[0],pos[1]),20)

    def return_color(self):
        return self.show_color

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

    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] != OFFBOARD: board[y][x] = 0

def captures(color):
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
                    
                    clear_block()
                    check = True
                

                #restore the board
                restore_board()
    return check

def set_stone(y,x,color):
    #make move
    board[y][x] = int(color)

#initializing pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height),0,32)
pg.display.set_caption("Go")

def draw_board():
    screen.fill(board_bg)

    for i in range(1,size+1):
        pg.draw.line(screen,black,(alt*i,alt),(i*alt,width-alt),1)
        pg.draw.line(screen,black,(alt,i*alt),(height-alt,i*alt),1)
        pg.display.flip()

    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == 1 or board[y][x] == 2:
                try:
                    pos_x = ((x-1)*alt)+alt
                    pos_y = (y-1)*alt+alt
                    pos_s = (pos_x,pos_y)
                    #board has valies of 1 and 2 for black and white so we can associate this with list positions in the colours list
                    piece_colour = colours[board[y][x]]
                    piece_board[y-1][x-1] = Piece(pos_s,piece_colour)
                    pg.display.flip()
                except:
                    pass
    pg.display.flip()

def get_pos():
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
            mouse_pos = get_pos()
            pos_y = ((mouse_pos[0]-alt/2)//alt)*alt+alt
            pos_x = ((mouse_pos[1]-alt/2)//alt)*alt+alt
            pos_s = (pos_x,pos_y)
            if piece_board[int((pos_y//alt)-1),int((pos_x//alt)-1)] != None:
                continue
            else:
                set_stone(int((pos_y//alt)),int((pos_x//alt)),color)
                flag_counter = captures(3-color)
                if len(liberties) == 0 and flag_counter and seki_count == 0:
                    draw_board()
                    if pg_color == black: color = WHITE;pg_color = white
                    else: pg_color = black; color = BLACK
                    seki_count = 1
                    continue
                if len(liberties) == 0 and seki_count == 1:
                    seki_count = 0
                    seki_check = True
                    continue

                flag = captures(color)
                if len(liberties) == 0 and flag == True:
                    continue
                else:
                    seki_count = 0
                    piece_board[int((pos_y//alt)-1)][int((pos_x//alt)-1)] = Piece(pos_s,pg_color)

                    if color == BLACK: enter_color = WHITE
                    else: enter_color = BLACK

                    captures_have_been_had = captures(enter_color)
                    if captures_have_been_had: draw_board()

                    if pg_color == black: color = WHITE;pg_color = white
                    else: pg_color = black; color = BLACK

    pg.display.update()

pg.quit()
