import os
import random
from model import TicTacToeModel
from modelEasy import TicTacToeModel_Easy
from modelHard import TicTacToeModel_Hard
import copy
import keras
import tensorflow as tf
from keras.models import load_model, model_from_json


PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '
PLAYER_X_VAL = -1
PLAYER_O_VAL = 1
EMPTY_VAL = 0
HORIZONTAL_SEPARATOR = ' | '
VERTICAL_SEPARATOR = '---------------'
GAME_STATE_X = -1
GAME_STATE_O = 1
GAME_STATE_DRAW = 0
GAME_STATE_NOT_ENDED = 2
[0, 0, 0]

class Game:

    def canWin(self, player):
        cpBoard = copy.deepcopy(self.board)
        for i in range(0,2):
            for j in range(0,2):
                if cpBoard == 0:
                    cpBoard[i][j] = player
                    if(self.getGameResult(cpBoard)!=GAME_STATE_NOT_ENDED):
                        return [i, j]
                

    # def pickMove(self, playerToMove):
    #     if playerToMove == PLAYER_X_VAL:
    #         canWin = self.canWin(PLAYER_X_VAL)
    #         if canWin != None:
    #             return canWin
    #     else:
    #         canWin = self.canWin(PLAYER_O_VAL)
    #         if canWin != None:
    #             return canWin

    #     #check if corners are free
    #     for i in [0,2]:
    #         for j in [0,2]:
    #             if self.board[i][j] == 0:
    #                 return [i, j]
        
    #     if self.board[1][1] == 0:
    #                 return [1, 1]

    #     for i in [0,2]:
    #         if self.board[i][1] == 0:
    #                 return [i, 1]
    #     for j in [0,2]:
    #         if self.board[1][j] == 0:
    #             return [1, j]

    def pickMove(self, playerToMove):
        if playerToMove == PLAYER_X_VAL:
            canWin = self.canWin(PLAYER_X_VAL)
            if canWin != None:
                return canWin
            else :
                canWin = self.canWin(PLAYER_O_VAL)
                if canWin != None:
                    return canWin
        else:
            canWin = self.canWin(PLAYER_O_VAL)
            if canWin != None:
                return canWin
            else :
                canWin = self.canWin(PLAYER_O_VAL)
                if canWin != None:
                    return canWin

        #check if corners are free
        for i in [0,2]:
            for j in [0,2]:
                if self.board[i][j] == 0:
                    return [i, j]
        
        if self.board[1][1] == 0:
                    return [1, 1]

        for i in [0,2]:
            if self.board[i][1] == 0:
                    return [i, 1]
        for j in [0,2]:
            if self.board[1][j] == 0:
                return [1, j]

    def __init__(self):
        self.resetBoard()
        self.trainingHistory = []

    def resetBoard(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.boardHistory = []

    def printBoard(self):
        print(VERTICAL_SEPARATOR)
        for i in range(len(self.board)):
            print(' ', end='')
            for j in range(len(self.board[i])):
                if PLAYER_X_VAL == self.board[i][j]:
                    print(PLAYER_X, end='')
                elif PLAYER_O_VAL == self.board[i][j]:
                    print(PLAYER_O, end='')
                elif EMPTY_VAL == self.board[i][j]:
                    print(EMPTY, end='')
                print(HORIZONTAL_SEPARATOR, end='')
            print(os.linesep)
            print(VERTICAL_SEPARATOR)

    def getGameResult(self, board):
        # Rows
        for i in range(len(board)):
            candidate = board[i][0]
            for j in range(len(board[i])):
                if candidate != board[i][j]:
                    candidate = 0
            if candidate != 0:
                return candidate

        # Columns
        for i in range(len(board)):
            candidate = board[0][i]
            for j in range(len(board[i])):
                if candidate != board[j][i]:
                    candidate = 0
            if candidate != 0:
                return candidate

        # First diagonal
        candidate = board[0][0]
        for i in range(len(board)):
            if candidate != board[i][i]:
                candidate = 0
        if candidate != 0:
            return candidate

        # Second diagonal
        candidate = board[0][2]
        for i in range(len(board)):
            if candidate != board[i][len(board[i]) - i - 1]:
                candidate = 0
        if candidate != 0:
            return candidate

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == EMPTY_VAL:
                    return GAME_STATE_NOT_ENDED

        return GAME_STATE_DRAW


    def getAvailableMoves(self):
        availableMoves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (self.board[i][j]) == EMPTY_VAL:
                    availableMoves.append([i, j])
        return availableMoves

    def addToHistory(self, board):
        self.boardHistory.append(board)

    def printHistory(self):
        print(self.boardHistory)

    def move(self, position, player):
        availableMoves = self.getAvailableMoves()
        for i in range(len(availableMoves)):
            if position[0] == availableMoves[i][0] and position[1] == availableMoves[i][1]:
                self.board[position[0]][position[1]] = player
                self.addToHistory(copy.deepcopy(self.board))


    def simulate(self, playerToMove):
        while (self.getGameResult(self.board) == GAME_STATE_NOT_ENDED):
            if(playerToMove == PLAYER_X_VAL):
                availableMoves = self.getAvailableMoves()
                selectedMove = availableMoves[random.randrange(0, len(availableMoves))]
                self.move(selectedMove, playerToMove)
                if playerToMove == PLAYER_X_VAL:
                    playerToMove = PLAYER_O_VAL
                else:
                    playerToMove = PLAYER_X_VAL
            elif(playerToMove == PLAYER_O_VAL):
                selectedMove = self.pickMove(playerToMove)
                self.move(selectedMove, playerToMove)
                if playerToMove == PLAYER_X_VAL:
                    playerToMove = PLAYER_O_VAL
                else:
                    playerToMove = PLAYER_X_VAL
        for historyItem in self.boardHistory:
            self.trainingHistory.append((self.getGameResult(self.board), copy.deepcopy(historyItem)))

    def simulateNeuralNetwork(self, nnPlayer, model):
        playerToMove = PLAYER_X_VAL
        while (self.getGameResult(self.board) == GAME_STATE_NOT_ENDED):
            availableMoves = self.getAvailableMoves()
            if playerToMove == nnPlayer:
                maxValue = 0
                bestMove = availableMoves[0]
                for availableMove in availableMoves:
                    # get a copy of a board
                    boardCopy = copy.deepcopy(self.board)
                    boardCopy[availableMove[0]][availableMove[1]] = nnPlayer
                    if nnPlayer == PLAYER_X_VAL:
                        value = model.predict(boardCopy, 0)
                    else:
                        value = model.predict(boardCopy, 2)
                    if value > maxValue:
                        maxValue = value
                        bestMove = availableMove
                selectedMove = bestMove
            else:
                #selectedMove = None
                selectedMove = availableMoves[random.randrange(0, len(availableMoves))]
                #selectedMove = self.pickMove(playerToMove)
                #while(selectedMove == None):
                #    self.printBoard()
                #    x = input("X-Koordinate (1-3)")
                    #y = input("Y-Koordinate (1-3)")
                    # if (x != 0 or x != 1 or x != 2) or (y != 0 or y != 1 or y != 2):
                    #     selectedMove == None
                    #     return
                    # if (availableMoves.__contains__([int(x),int(y)])):
                    #     selectedMove =  [int(x), int(y)]
                    # if(self.getGameResult(self.board) != GAME_STATE_NOT_ENDED):
                    #     return
            self.move(selectedMove, playerToMove)
            if playerToMove == PLAYER_X_VAL:
                playerToMove = PLAYER_O_VAL
            else:
                playerToMove = PLAYER_X_VAL

    def simulateNeuralNetworkWithHumanPlayer(self, nnPlayer, model):
        playerToMove = PLAYER_X_VAL
        while (self.getGameResult(self.board) == GAME_STATE_NOT_ENDED):
            availableMoves = self.getAvailableMoves()
            if playerToMove == nnPlayer:
                maxValue = 0
                bestMove = availableMoves[0]
                for availableMove in availableMoves:
                    # get a copy of a board
                    boardCopy = copy.deepcopy(self.board)
                    boardCopy[availableMove[0]][availableMove[1]] = nnPlayer
                    if nnPlayer == PLAYER_X_VAL:
                        value = model.predict(boardCopy, 0)
                    else:
                        value = model.predict(boardCopy, 2)
                    if value > maxValue:
                        maxValue = value
                        bestMove = availableMove
                selectedMove = bestMove
            else:
                selectedMove = None
                #selectedMove = availableMoves[random.randrange(0, len(availableMoves))]
                selectedMove = self.pickMove(playerToMove)
                while(selectedMove == None):
                    self.printBoard()
                    x = input("X-Koordinate (1-3)")
                    y = input("Y-Koordinate (1-3)")
                    if (x != 0 or x != 1 or x != 2) or (y != 0 or y != 1 or y != 2):
                        selectedMove == None
                        return
                    if (availableMoves.__contains__([int(x),int(y)])):
                        selectedMove =  [int(x), int(y)]
                    if(self.getGameResult(self.board) != GAME_STATE_NOT_ENDED):
                        return
            self.move(selectedMove, playerToMove)
            if playerToMove == PLAYER_X_VAL:
                playerToMove = PLAYER_O_VAL
            else:
                playerToMove = PLAYER_X_VAL
        
    def getTrainingHistory(self):
        return self.trainingHistory

    def simulateManyGames(self, playerToMove, numberOfGames):
        playerXWins = 0
        playerOWins = 0
        draws = 0
        for i in range(numberOfGames):
            self.resetBoard()
            self.simulate(playerToMove)
            if self.getGameResult(self.board) == PLAYER_X_VAL:
                playerXWins = playerXWins + 1
            elif self.getGameResult(self.board) == PLAYER_O_VAL:
                playerOWins = playerOWins + 1
            else: draws = draws + 1
        totalWins = playerXWins + playerOWins + draws
        print ('X Wins: ' + str(int(playerXWins * 100/totalWins)) + '%')
        print('O Wins: ' + str(int(playerOWins * 100 / totalWins)) + '%')
        print('Draws: ' + str(int(draws * 100 / totalWins)) + '%')


    def simulateManyNeuralNetworkGames(self, nnPlayer, numberOfGames, model):
        nnPlayerWins = 0
        randomPlayerWins = 0
        draws = 0
        print ("NN player")
        print (nnPlayer)
        for i in range(numberOfGames):
            self.resetBoard()
            self.simulateNeuralNetwork(nnPlayer, model)
            if self.getGameResult(self.board) == nnPlayer:
                nnPlayerWins = nnPlayerWins + 1
            elif self.getGameResult(self.board) == GAME_STATE_DRAW:
                draws = draws + 1
            else: randomPlayerWins = randomPlayerWins + 1
        totalWins = nnPlayerWins + randomPlayerWins + draws
        print ('X Wins: ' + str(int(nnPlayerWins * 100/totalWins)) + '%')
        print('O Wins: ' + str(int(randomPlayerWins * 100 / totalWins)) + '%')
        print('Draws: ' + str(int(draws * 100 / totalWins)) + '%')

if __name__ == "__main__":
    game = Game()
    game.simulateManyGames(1, 5000)
    ticTacToeModelHard = TicTacToeModel_Hard(9, 3, 100, 32)
    ticTacToeModelEasy = TicTacToeModel_Easy(9, 3, 100, 32)

    
    ticTacToeModelHard.train(game.getTrainingHistory())
    ticTacToeModelEasy.train(game.getTrainingHistory())
    
    print("Simulating with Neural Network as O Player:")
    game.simulateManyNeuralNetworkGames(PLAYER_X_VAL, 100, ticTacToeModelHard)
    print ("Simulating with Neural Network as X Player:")
    game.simulateManyNeuralNetworkGames(PLAYER_X_VAL, 100, ticTacToeModelEasy)

    game.simulateNeuralNetworkWithHumanPlayer(PLAYER_O_VAL, 5, ticTacToeModelEasy)
    game.simulateNeuralNetworkWithHumanPlayer(PLAYER_O_VAL, 5, ticTacToeModelHard)

    game.simulateNeuralNetworkWithHumanPlayer(PLAYER_X_VAL, 5, ticTacToeModelEasy)
    game.simulateNeuralNetworkWithHumanPlayer(PLAYER_X_VAL, 5, ticTacToeModelEasy)



    
