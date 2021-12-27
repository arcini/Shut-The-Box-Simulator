from random import randint
from abc import ABC, abstractmethod
import typing

#build lookup table
lookup_table = []


#courtesy of: https://www.geeksforgeeks.org/all-unique-combinations-whose-sum-equals-to-k/
def unique_combination(l, summ, K, A, outlist = [], local = []):
    # If a unique combination is found
    if (summ == K):
        outlist.append(local.copy())
 
    # For all other combinations
    for i in range(l, len(A), 1):
 
        # Check if the sum exceeds K
        if (summ + A[i] > K):
            continue
 
        # Check if it is repeated or not
        if (i > l and
                A[i] == A[i - 1]):
            continue
 
        # Take the element into the combination
        local.append(A[i])
 
        # Recursive call
        unique_combination(i + 1, summ + A[i],
                           K, A, outlist, local)
 
        # Remove element from the combination
        local.remove(local[len(local) - 1])

    return outlist
 
# Function to find all combination
# of the given elements
def Combination(A, K):
 
    # Sort the given elements
    A.sort(reverse=False)
 
    return unique_combination(0, 0, K, A, outlist=[], local=[])


def buildTable():
    for k in range(2,13):
        lookup_table.append(sorted(Combination(list(range(1, k+1)), k).copy(), key=lambda x: x[-1], reverse=True))
        
buildTable()

class Dice:
    
    def __init__(self):
        self.roll()

    def roll(self):
        self.state1 = randint(1,6)
        self.state2 = randint(1,6)
        
class Strategy:

    @abstractmethod
    def choice():
        pass

class Board:

    def __init__(self, strat:Strategy):
        self.dice = Dice()
        self.box = [False for x in range(12+1)] #ignore box[0] bc frick the fencepost errors
        self.box[0] = True
        self.strat = strat

    def playRound(self):
        self.dice.roll()
        choice = self.strat.choice(self)
        if choice[0] == False:
            return False
        else:
            for flap in choice[1]:
                self.box[flap] = True
            return True

    def checkWon(self):
        return all(x == True for x in self.box)

    def playGame(self):
        while True:
            roundResult = self.playRound()

            if self.checkWon() == True:
                self.box = [False for x in range(12+1)] #ignore box[0] bc frick the fencepost errors
                self.box[0] = True
                return True
            else:
                if roundResult == False:
                    self.box = [False for x in range(12+1)] #ignore box[0] bc frick the fencepost errors
                    self.box[0] = True
                    return False

    
        

class TopDown(Strategy):
    #Always pick the choice containing the highest number flap you can put down
    def choice(board: Board):
        diceSum = board.dice.state1 + board.dice.state2
        for triple in lookup_table[diceSum-2]:
            if all(board.box[x] == False for x in triple):
                return True, triple

        return False, []

class BottomUp(Strategy):
    #Reverse of TopDown
    def choice(board: Board):
        diceSum = board.dice.state1 + board.dice.state2
        for triple in reversed(lookup_table[diceSum-2]):
            if all(board.box[x] == False for x in triple):
                return True, triple

        return False, []
    
    

def simulate(strat: Strategy, strategyName):
    board = Board(strat)
    wincount = 0
    playcount = 500000
    for x in range(playcount):
        if board.playGame():
            wincount += 1

    print(strategyName, wincount, playcount, wincount/playcount)

simulate(TopDown, "top down")
        
        
    
    
