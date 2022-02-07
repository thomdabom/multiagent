# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.
    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.
        getAction chooses among the best options according to the evaluation function.
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        #print(legalMoves)

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # Retreives coordinates of remaining food
        remainingFood = successorGameState.getFood().asList()
        infinite = float('inf')
        
        # Loops through remaining food to find minimum distance to food
        for foodPos in remainingFood:
            infinite = min(infinite, manhattanDistance(newPos, foodPos))
        
        # Loops through locations of ghosts and if they are within a distance of 3 avoid moving that direction
        for ghostPos in successorGameState.getGhostPositions():
            if(manhattanDistance(newPos, ghostPos) < 3):
                return -float('inf')
        
        # Reciprocal so shortest distance is actually greatest
        return successorGameState.getScore() + 1.0/infinite
    
def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.
    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        
        Here are some method calls that might be useful when implementing minimax.
        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1
        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action
        gameState.getNumAgents():
        Returns the total number of agents in the game
        gameState.isWin():
        Returns whether or not the game state is a winning state
        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
    
        def miniMax(depth, gameState, agentIndex):
            if agentIndex == gameState.getNumAgents() :
                depth = depth + 1
                agentIndex = 0  
            
            if gameState.isWin() or gameState.isLose() or depth == (self.depth):
                return (None, self.evaluationFunction(gameState))

            bestAction = None
            if agentIndex == 0 :
                value = -float('inf')
            else :
                value = float('inf')
            
            for action in gameState.getLegalActions(agentIndex):
                # print("action")
                successorAction, successorVal = miniMax(depth, gameState.generateSuccessor(agentIndex, action), agentIndex + 1)
                if agentIndex == 0 and value < successorVal :
                    bestAction = action
                    value = successorVal
                elif agentIndex != 0 and value > successorVal :
                    bestAction = action
                    value = successorVal
            return (bestAction, value)

        action, value = miniMax(0, gameState, 0)
        
        return action
        
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction
        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        def expectiMax(depth, gameState, agentIndex):
            
            if agentIndex == gameState.getNumAgents() :
                depth = depth + 1
                agentIndex = 0  
            
            if gameState.isWin() or gameState.isLose() or depth == (self.depth):
                return (None, self.evaluationFunction(gameState))

            bestAction = None
            legalActions = gameState.getLegalActions(agentIndex)

            if agentIndex == 0 :
                value = -float('inf')
            else :
                probability = 1.0 / float(len(legalActions))
                value = 0.0
            
            for action in gameState.getLegalActions(agentIndex):
                # print("action")
                successorAction, successorVal = expectiMax(depth, gameState.generateSuccessor(agentIndex, action), agentIndex + 1)
                if agentIndex == 0 and value < successorVal :
                    bestAction = action
                    value = successorVal
                elif agentIndex != 0 :
                    value += probability * successorVal
                    bestAction = action
            
            return (bestAction, value)

        action, value = expectiMax(0, gameState, 0)
        
        return action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    DESCRIPTION: get the closest food and add it to the current game score.
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    remainingFood = currentGameState.getFood().asList()
    foodVal = float('inf')
        
    # Loops through remaining food to find minimum distance to food
    for foodPos in remainingFood:
        foodVal = min(foodVal, manhattanDistance(newPos, foodPos))
    
    # Reciprocal so shortest distance is actually greatest
    return currentGameState.getScore() + 1.0/foodVal

# Abbreviation
better = betterEvaluationFunction