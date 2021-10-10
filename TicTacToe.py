from typing import Dict
import pygame
from pygame.constants import K_r
from pygame.locals import K_DOWN, K_UP, K_LEFT, K_RIGHT, K_ESCAPE, \
    KEYDOWN, QUIT
import numpy as np
import random
from datetime import datetime, timedelta
import copy
import random


GAME_SIZE = 900
MARGIN = GAME_SIZE//14
SQUARE_SIZE = (GAME_SIZE-(2*MARGIN))//3
LINE_WIDTH = 2
DILUTE = GAME_SIZE//90
pygame.init()

window = pygame.display.set_mode((GAME_SIZE, GAME_SIZE))


def draw_board():
    window.fill((0, 0, 0))
    pygame.draw.line(window, (255,255,255), (MARGIN+SQUARE_SIZE-LINE_WIDTH, MARGIN), (MARGIN+SQUARE_SIZE-LINE_WIDTH, GAME_SIZE-MARGIN), LINE_WIDTH)
    pygame.draw.line(window, (255,255,255), (MARGIN+2*SQUARE_SIZE+LINE_WIDTH, MARGIN), (MARGIN+2*SQUARE_SIZE+LINE_WIDTH, GAME_SIZE-MARGIN), LINE_WIDTH)
    pygame.draw.line(window, (255,255,255), (MARGIN, MARGIN+SQUARE_SIZE-LINE_WIDTH), (GAME_SIZE-MARGIN, MARGIN+SQUARE_SIZE-LINE_WIDTH), LINE_WIDTH)
    pygame.draw.line(window, (255,255,255), (MARGIN, MARGIN+2*SQUARE_SIZE+LINE_WIDTH), (GAME_SIZE-MARGIN, MARGIN+2*SQUARE_SIZE+LINE_WIDTH), LINE_WIDTH)
    pygame.display.set_caption('TicTacToe')

draw_board()

x  = pygame.transform.scale(pygame.image.load('TicTacToeImages/X.png'), (SQUARE_SIZE-DILUTE,SQUARE_SIZE-DILUTE))
o  = pygame.transform.scale(pygame.image.load('TicTacToeImages/O.png'), (SQUARE_SIZE-DILUTE,SQUARE_SIZE-DILUTE))
greyO = pygame.transform.scale(pygame.image.load('TicTacToeImages/greyerO.png'), (SQUARE_SIZE-DILUTE,SQUARE_SIZE-DILUTE))
greyX = pygame.transform.scale(pygame.image.load('TicTacToeImages/greyerX.png'), (SQUARE_SIZE-DILUTE,SQUARE_SIZE-DILUTE))



class MonteCarlo:
    def __init__(self, board, player):
        self.root = Node(board, player)
        self.nodes = []
        self.root.generate_legal()


    def traverse(self):
        now = datetime.now()
        while datetime.now() <= now + timedelta(seconds = 1):
            best_node = self.root.select_best_node(self.root.game.player)
            best_node.expanded = True
            best_node.simulate()

        child_values = list(map(lambda x: x.calc_value(), self.root.children))
        return self.root.children[child_values.index(max(child_values))]



class Node:
    def __init__(self, state, player, parent=None):
        self.game = TicTacToe()
        self.game.board = state
        self.game.player = player
        self.children = []
        self.parent = parent
        self.value = 0
        self.visits = 0
        self.expanded = False

    def generate_legal(self):
        temp_board = TicTacToe()
        if len(self.children)==0:
            for i in range(3):
                for j in range(3):
                    template = np.array([[0,0,0],
                                        [0,0,0],
                                        [0,0,0]])
                    temp_board.board = self.game.board.copy()
                    temp_board.player = self.game.player
                    if self.game.board[i][j] == 0:
                        template[i][j] = 1
                        temp_board.place(template)
                        self.children.append(Node(temp_board.board, temp_board.player, self))
        
        self.game.checkWin()
        if (self.game.game_over):
            self.children = []

    def simulate(self):
        self.generate_legal()
      
        if self.game.game_over:
            self.value += self.game.winner
            self.visits+=1
            self.back_propogate(self.game.winner)
            self.game.winner = 0
            return self.value
        else:
            temp_node = self.rollout_policy()
            return temp_node.simulate()

    def calc_value(self):
        if(self.visits>0):
            return self.value/self.visits 
        return -100


    def rollout_policy(self):
        rand = random.choice(self.children)
        return rand

    def back_propogate(self, value):
        if self.parent is None:
            return None

        self.parent.value+=value
        self.parent.visits+=1
        return self.parent.back_propogate(value)
    
    def select_best_node(self, player):
        best_node = self
        best_node.generate_legal()
        while len(best_node.children)>0:
            best_node.generate_legal()
            temp_node = best_node.select_best_child(player) 
            temp_node.generate_legal()
            if len(temp_node.children)==0:
                return best_node
            else:
                best_node = temp_node

            if(best_node.expanded==False):
                break
        return best_node

    def select_best_child(self, player):
        ucb_array = []
        for child in self.children:
            ucb_array.append(child.get_ucb(player))
        return self.children[ucb_array.index(max(ucb_array))]

    def get_ucb(self, player):
        temp_value = self.value
        if self.expanded == False:
            return 1000
        else:
            if player == -1:
                temp_value = -self.value
            uct = temp_value/self.visits + (np.sqrt(2) * np.sqrt(np.log(self.parent.visits)/self.visits)) 
            return uct




            
            




class TicTacToe:
    def __init__(self):
        self.player = 1
        self.board = np.array([[0,0,0],
                      [0,0,0],
                      [0,0,0]])
        self.game_over = False
        self.winner = 0
    
    def place(self, square):
        desired_location = np.nonzero(square)
        row = desired_location[0][0]
        col = desired_location[1][0]
        if self.board[row][col] == 0:
            self.board[row][col] = self.player
            self.player = -self.player
        self.checkWin()

    def checkWin(self):
        tempBoard = self.board
        for i in range(3):
            if sum(tempBoard[i]) == 3 or sum(tempBoard[i]) == -3:
                self.game_over = True

        tempBoard = np.transpose(self.board)

        for i in range(3):
            if sum(tempBoard[i]) == 3 or sum(tempBoard[i]) == -3:
                self.game_over = True

        if (self.board[0][0] == 1 and self.board[1][1] == 1 and self.board[2][2] == 1) or (self.board[0][0] == -1 and self.board[1][1] == -1 and self.board[2][2] == -1):
            self.game_over = True
        
        if (self.board[2][0] == 1 and self.board[1][1] == 1 and self.board[0][2] == 1) or (self.board[2][0] == -1 and self.board[1][1] == -1 and self.board[0][2] == -1):
            self.game_over = True
        
        result = np.all((self.board != 0))
       
        if self.game_over == True:
            self.winner = -self.player
            return self.winner
        if(result):
            self.game_over = True
            return self.winner



        
KeepPlaying=True

while KeepPlaying:
        

    board = TicTacToe()
    draw_board()
    pygame.display.update()



    while not board.game_over:
        pygame.event.pump()
        template = np.array([[0,0,0],
                        [0,0,0],
                        [0,0,0]])
        if board.player == 1:
            mc = MonteCarlo(board.board, board.player)
            pos = mc.traverse()
            board.board = pos.game.board
            board.player = -board.player
            board.checkWin()
            if board.game_over:
                break

        for event in pygame.event.get():
            if event.type == QUIT:
                board.game_over = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    board.game_over=True
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = (pos[0]-MARGIN)//(SQUARE_SIZE)
                row = (pos[1]-MARGIN)//(SQUARE_SIZE)
                if col>=3:
                    col=2
                if row>=3:
                    row=2
                template[row][col] = 1
                board.place(template)
                board.checkWin()
                

            for i in range(3):
                for j in range(3):
                    if(board.board[i][j]!=0):
                        if(board.board[i][j]==1):
                            window.blit(x, (SQUARE_SIZE*j+MARGIN+DILUTE//2, SQUARE_SIZE*i+MARGIN+DILUTE//2))
                        else:
                            window.blit(o, (SQUARE_SIZE*j+MARGIN+DILUTE//2, SQUARE_SIZE*i+MARGIN+DILUTE//2))
            
        


        pygame.display.update()
    
    newDispX = x
    newDispO = o
    if board.winner == 1:
        newDispO = greyO
    elif board.winner == -1:
        newDispX = greyX
    else:
        newDispO = greyO
        newDispX = greyX


    for i in range(3):
                for j in range(3):
                    if(board.board[i][j]!=0):
                        if(board.board[i][j]==1):
                            window.blit(newDispX, (SQUARE_SIZE*j+MARGIN+DILUTE//2, SQUARE_SIZE*i+MARGIN+DILUTE//2))
                        else:
                            window.blit(newDispO, (SQUARE_SIZE*j+MARGIN+DILUTE//2, SQUARE_SIZE*i+MARGIN+DILUTE//2))
    pygame.display.update()
    pygame.event.pump()
    inquiring = True
    while inquiring:
        for event in pygame.event.get():
                if event.type == QUIT:
                    board.game_over = True
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        KeepPlaying=True
                        inquiring=False
                    if event.key == K_ESCAPE:
                        KeepPlaying = False
                        inquiring = False


