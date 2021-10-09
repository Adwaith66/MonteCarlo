import pygame
from pygame.locals import K_DOWN, K_UP, K_LEFT, K_RIGHT, K_ESCAPE, \
    KEYDOWN, QUIT
import numpy as np
import random
from datetime import datetime, timedelta
import copy
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

class MonteCarlo:
    def __init__(self, board, player):
        self.root = Node(board, player)
        self.nodes = []
        self.root.generate_legal()


    def traverse(self):
        now = datetime.now()
        """while datetime.now() <= now + timedelta(seconds = 1):
            best_node = self.root.select_best_node(self.root.game.player)
            best_node.expanded = True
            best_node.simulate()
            print('BOOLEAN' , bool(best_node is a for a in self.root.children))
            print("NEW VALUE OF BEST NODE", best_node.value, "VISITS", best_node.visits)
            print(list(map(lambda x: x.calc_value(), self.root.children)))   
        child_values = list(map(lambda x: x.calc_value(), self.root.children))
        for i in self.root.children:
            print('child board', i.game.board)"""
        for i in range(20):
            self.root.children[3].simulate()
            #print("OG", self.root.children[3].value)

        num2 = self.root.children[3].select_best_node(self.root.children[3].game.player)
        print("SAME", num2.parent is self.root.children[3])
        print("SAME", num2.parent.game.board is self.root.children[3].game.board)

       # print("OG BOARD", num2.game.board)
        for i in range (20):
           # print("VALUE RN", num2.value)
            num2.simulate()
            print('Original', self.root.children[3].value, 'Copy', num2.value)
            #print("COpy Winner", num2.game.winner, num2.game.player)
        print(self.root.children[3].calc_value())


        
        #print(child_values)
        #return self.root.children[child_values.index(max(child_values))]



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
        self.game.checkWin()
        if self.game.game_over:
            #self.game.winner=-self.game.winner
            self.value += self.game.winner
            #print(self.game.winner, "is being backpropogated")
            self.visits+=1
            self.back_propogate(self.game.winner)
            return self.value
        else:
            temp_node = self.rollout_policy()
            #print('NEW PLAYER', temp_node.game.currentplayer)
            #print('RANDOM CHILD', temp_node.game.board)
            return temp_node.simulate()

    def calc_value(self):
        #print('visits:', self.visits, 'value', self.value)
        if(self.visits>0):
            return self.value/self.visits 
        return -100


    def rollout_policy(self):
        rand = random.choice(self.children)
        #print("Choice", rand.game.board)
        return rand

    def back_propogate(self, value):
        if self.parent is None:

            #print(self.game.board, "HAS NO PARENT")
            return None
        #print("PARENT:", self.parent.game.board)
        self.parent.value+=value
        #print('VALUE', self.parent.value)
        self.parent.visits+=1
        return self.parent.back_propogate(value)
    
    def select_best_node(self, player):
        best_node = self
        best_node.generate_legal()
        while len(best_node.children)>0:
            best_node.generate_legal()
            temp_node = best_node.select_best_child(player) 
            temp_node.generate_legal()
            #print("OPTONS", len(temp_node.children))
            if len(temp_node.children)==0:
                #print("BEST NODE ", best_node.game.board)
                return best_node
            else:
                best_node = 5
                best_node = temp_node

            if(best_node.expanded==False):
                break
        #print("BEST NODE ", best_node.game.board)
        return best_node

    def select_best_child(self, player):
        ucb_array = []
        for child in self.children:
            ucb_array.append(child.get_ucb(player))
            #print('UCB', child.get_ucb())
        return self.children[ucb_array.index(max(ucb_array))]

    def get_ucb(self, player):
        temp_value = self.value
        if self.expanded == False:
            return 1000
        else:
            #print('Value', self.value, 'Visits', self.visits, 'Parent Value', self.parent.value, 'Parent Visits', self.parent.visits)
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
        #print(self.board)

    def checkWin(self):
        tempBoard = self.board
        for i in range(3):
            if sum(tempBoard[i]) == 3 or sum(tempBoard[i]) == -3:
                #print('The winner is', -self.player)
                self.game_over = True

        tempBoard = np.transpose(self.board)

        for i in range(3):
            if sum(tempBoard[i]) == 3 or sum(tempBoard[i]) == -3:
                #print('The winner is', -self.player)
                self.game_over = True

        if (self.board[0][0] == 1 and self.board[1][1] == 1 and self.board[2][2] == 1) or (self.board[0][0] == -1 and self.board[1][1] == -1 and self.board[2][2] == -1):
            #print('The winner is', -self.player)
            self.game_over = True
        
        if (self.board[2][0] == 1 and self.board[1][1] == 1 and self.board[0][2] == 1) or (self.board[2][0] == -1 and self.board[1][1] == -1 and self.board[0][2] == -1):
            #print('The winner is', -self.player)
            self.game_over = True
        
        result = np.all((self.board != 0))


       
        if self.game_over == True:
            self.winner = -self.player
            return self.winner
        if(result):
            self.game_over = True
            return self.winner

        


        
        

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
            elif event.key == K_RIGHT:
                mc = MonteCarlo(board.board, board.player)
                pos = mc.traverse()
               # board.board = pos.game.board
               # board.player = -board.player
               # board.checkWin()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            col = pos[0]//SQUARE_SIZE
            row = pos[1]//SQUARE_SIZE
            template[row][col] = 1
            board.place(template)
            board.checkWin()
            

            #print('GAME BOARD', board.board)
        for i in range(3):
            for j in range(3):
                if(board.board[i][j]!=0):
                    if(board.board[i][j]==1):
                        pygame.draw.circle(window, (150,0,0), (100*j+50, 100*i+50), 10, 199)
                    else:
                        pygame.draw.circle(window, (0,0,150), (100*j+50, 100*i+50), 10, 199)
        
            


    pygame.display.update()
               
clearConsole = lambda: print('\n' * 150)

clearConsole()

print("WINNER", board.winner)