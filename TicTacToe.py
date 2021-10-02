import pygame
from pygame.locals import K_DOWN, K_UP, K_LEFT, K_RIGHT, K_ESCAPE, \
    KEYDOWN, QUIT
import numpy as np
import random

pygame.init()

window = pygame.display.set_mode((300, 300))
window.fill((255, 255, 255))
running = True
SQUARE_SIZE = 100

pygame.draw.line(window, (0,0,0), (100, 25), (100, 275), 1)
pygame.draw.line(window, (0,0,0), (200, 25), (200, 275), 1)
pygame.draw.line(window, (0,0,0), (25, 100), (275, 100), 1)
pygame.draw.line(window, (0,0,0), (25, 200), (275, 200), 1)


class Node:
    def __init__(self, state, player, parent=None):
        self.game = TicTacToe()
        self.game.board = state
        self.game.player = player
        self.children = []
        self.parent = parent
        self.value = 0
        self.visits = 0

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
                        print('i', i, "j", j)
                        template[i][j] = 1
                        temp_board.place(template)
                        self.children.append(Node(temp_board.board, temp_board.player, self))
                

    def simulate(self):
        self.generate_legal()
        temp_value = self.game.checkWin()
        if self.game.game_over:
            self.value = temp_value
            print('SIM OVER', self.value)
            #self.back_propogate(self.value)
            return self.value
        else:
            temp_node = self.rollout_policy()
            #print('NEW PLAYER', temp_node.game.currentplayer)
            print('RANDOM CHILD', temp_node.game.board)
            return temp_node.simulate()

    def calc_value(self):
        pass
    def rollout_policy(self):
        rand = random.choice(self.children)
        print("Choice", rand.game.board)
        return rand
    def back_propogate(self):
        pass




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
        #print(self.board)

    def checkWin(self):
        tempBoard = self.board
        for i in range(3):
            if sum(tempBoard[i]) == 3 or sum(tempBoard[i]) == -3:
                print('The winner is', -self.player)
                self.winner = -self.player
                self.game_over = True

        tempBoard = np.transpose(self.board)

        for i in range(3):
            if sum(tempBoard[i]) == 3 or sum(tempBoard[i]) == -3:
                print('The winner is', -self.player)
                self.game_over = True
                self.winner = -self.player

        if (self.board[0][0] == self.board[1][1] == self.board[2][2] == 1 or self.board[0][0] == self.board[1][1] == self.board[2][2] == -1):
            print('The winner is', -self.player)
            self.winner = -self.player
            self.game_over = True
        
        if self.board[2][0] == self.board[1][1] == self.board[0][2] == 1 or self.board[2][0] == self.board[1][1] == self.board[0][2] == -1:
            print('The winner is', -self.player)
            self.game_over = True
            self.winner = -self.player
        


        
        

board = TicTacToe()

while not board.game_over:
    pygame.event.pump()
    template = np.array([[0,0,0],
                      [0,0,0],
                      [0,0,0]])
    for event in pygame.event.get():
        if event.type == QUIT:
            board.game_over = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                board.game_over=True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            col = pos[0]//SQUARE_SIZE
            row = pos[1]//SQUARE_SIZE
            template[row][col] = 1
            board.place(template)
            board.checkWin()
            node = Node(board.board, board.player)
            node.generate_legal()
            node.simulate()
            print('GAME BOARD', board.board)
            for i in range(3):
                for j in range(3):
                    if(board.board[i][j]!=0):
                        if(board.board[i][j]==1):
                            pygame.draw.circle(window, (150,0,0), (100*j+50, 100*i+50), 10, 199)
                        else:
                            pygame.draw.circle(window, (0,0,150), (100*j+50, 100*i+50), 10, 199)
            


    pygame.display.update()
               


