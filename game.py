# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 15:06:21 2021

@author: robertivtcd
"""

######################################################################################
# Import Libraries
######################################################################################


import pygame, sys
from numpy import *
import numpy
import random
    
######################################################################################
# Initialise Variables
######################################################################################

#possible coordinates
ROWCOLUMNS = [0,1,2,3]

#possible numbers to be added to game
NUMBERS = [2,2,2,2,2,2,2,2,2,4] #one in ten chance of a 4 being selected

#board 
board = array([[0,0,0,0],[0,0,0,0],
   [0,0,0,0],[0,0,0,0]])

#score initialisation
total_score = 0

#######################################################################################
# Functions
#######################################################################################

#insert new number to matrix
def random_insert(board):  #puts a new number onto the board 
    fits = False
    while fits == False:
        identify_cell = array([random.choice(ROWCOLUMNS), random.choice(ROWCOLUMNS)])
        if board[identify_cell[0], identify_cell[1]] == 0:
            board[identify_cell[0], identify_cell[1]] = random.choice(NUMBERS)
            fits = True
          
def initiate(): #starts the game with two random inserts           
    #insert two numbers to initiate the game
    for i in range(2):
        random_insert(board)
    numbers_on_board(board, font)
    

def stack(board): # stacking function
    for column in ROWCOLUMNS[::-1]:         
        for repeat in range(3): #loop twice to scan twice
            for row in ROWCOLUMNS[::-1][:3][::-1]: #remove zeros and stack everything down
                if board[row, column] == 0:
                    board[row, column] = board[row -1, column]
                    board[row -1, column] = 0

def movement(board, rotations): #stacks board, doubles, zeros a cell, stacks again, repeat
    score = 0
    if valid_move(board) == True:
        stack(board)
        for column in ROWCOLUMNS[::-1]:        
            for row in ROWCOLUMNS[::-1][:3]: #doubling function
                if board[row, column] == board[row -1, column]:
                    board[row, column] += board[row, column] #doubles value
                    score += board[row, column] #update scoreboard 
                    board[row -1, column] = 0
                    stack(board)
        random_insert(board)
    board = numpy.rot90(board, k=rotations) #rotates board back to starting position
    return score
             
                
def valid_move(board): #move must be valid if there is (1) an empty space below a number, (2) a possible stackable number
    valid_move = False
    for column in ROWCOLUMNS[::-1]:        
        for row in ROWCOLUMNS[:3]:
            if (board[row, column] != 0 and board[row +1, column] == 0) or (board[row, column] != 0 and board[row +1, column] == board[row, column]):
                valid_move = True
    if valid_move == False:
        pass
    return valid_move

def game_over(board): #game over condition 
    game_over = False
    #considers valid moves across the four possible directions
    if 0 not in board and valid_move(board) == False and valid_move(numpy.rot90(board, k=2)) == False and valid_move(numpy.rot90(board, k=1)) == False and valid_move(numpy.rot90(board, k=3)) == False:
        game_over = True
    return game_over


def play(board, move): 
    current_score = 0
    if game_over(board) == False:
        #move = player_input
        if move == "s": #down
            current_score = movement(board, 0)
        elif move == "w": #up
            updated_board = numpy.rot90(board, k=2)
            current_score = movement(updated_board, 2 )
        elif move == "a": #left
            updated_board = numpy.rot90(board, k=1)
            current_score = movement(updated_board, 3 )
        elif move == "d": #right
            updated_board = numpy.rot90(board, k=3)
            current_score = movement(updated_board, 1 )
        else:
            current_score = 0
        return current_score
    if game_over(board) == True:
        pass   #need to make this do something 
    
    return current_score


#################################################################################################
# PYGAME
# INTEGRATION
################################################################################################                                                  

pygame.init()
    
WIDTH = 800
HEIGHT = 985
LINE_WIDTH = 30

# colours for each tile number
COLOURS = {0: (204, 192, 179), 2: (242, 219, 191),
           4: (230, 198, 161), 8: (237, 175, 109),
           16: (247, 159, 96), 32: (252, 103, 53),
           64: (224, 75, 25), 128: (255, 251, 135), 
           256: (247, 242, 92), 512: (255, 249, 69), 
           1024: (255, 248, 38), 2048: (255, 247, 0),}

LINE_COLOUR = (161, 147, 130)
GREY = (212, 207, 201)
RED_DARK = (232, 16, 16)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
screen.fill(COLOURS[0])

#structure the board
def draw_lines():
    #horizontal
    pygame.draw.line(screen, LINE_COLOUR, (0,0), (800,0), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, (0,200), (800,200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, (0,400), (800,400), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, (0,600), (800,600), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, (0,800), (800,800), LINE_WIDTH)
    #down lines
    pygame.draw.line(screen, LINE_COLOUR, (0,0), (0,800), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, (200,0), (200,800), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, (400,0), (400,800), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, (600,0), (600,800), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, (800,0), (800,800), LINE_WIDTH)

#font
font = pygame.font.SysFont('calibri', 40, bold=True)

#draw score tile
def display_score(score):
    pygame.draw.rect(screen, GREY, (16, 850, 300, 100 ))
    score_text = "Score: " + str(score)
    text_surface = font.render((score_text), True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(168, 900))
    screen.blit(text_surface, (text_rect))


def display_game_over():
    pygame.draw.rect(screen, GREY, (250, 250, 300, 300 ))
    text_surface = font.render(("Game Over"), True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(400, 400))
    screen.blit(text_surface, (text_rect))

#display tiles with number
def display_tiles(board, colour, row_counter, column_counter, row, column):
    pygame.draw.rect(screen, colour, (16+(200*row_counter), 16+(200*column_counter), 170, 170))
    if board[row, column] != 0:
        text_surface = font.render(str(board[row, column]), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(100+(200*row_counter), 100+(200*column_counter)))
        screen.blit(text_surface, (text_rect))

# print the text onto their tiles
def numbers_on_board(board, font):
    column_counter = 0
    for row in ROWCOLUMNS: #iterate through columns      
        row_counter = 0
        for column in ROWCOLUMNS: #iterate through rows
            if board[row, column] in COLOURS:
                display_tiles(board, COLOURS[board[row, column]], row_counter, column_counter, row, column)
            else:
                display_tiles(board, RED_DARK, row_counter, column_counter, row, column) #all values greater than 2048
            row_counter += 1
        column_counter += 1
        

##############################################################################################     
# Main Loop
##############################################################################################


def main():
    draw_lines()
    initiate()
    total_score = 0
    running = True
    while running == True:
        numbers_on_board(board, font)
        pygame.display.update()
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            elif game_over(board) == True:
                display_game_over()
                pygame.display.update()
                running = False
            elif pressed_keys[pygame.K_LEFT]:
                current_score = play(board, "a" )
            elif pressed_keys[pygame.K_RIGHT]:
                current_score = play(board, "d" )
            elif pressed_keys[pygame.K_UP]:
                current_score = play(board, "w" )
            elif pressed_keys[pygame.K_DOWN]:
                current_score = play(board, "s" )
            else:
                current_score = 0
            
            if running == True: 
                total_score += current_score
                numbers_on_board(board, font)
                display_score(total_score)
                pygame.display.update()    
    pygame.quit()
 
main()       
       
