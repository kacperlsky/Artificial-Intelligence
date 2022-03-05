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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        # Pick randomly among the best

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
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        ###this is what variables I can work with and I am going to combine them
        #GOAL: for the Pacman to reach the highest score possible
        #printing all the variables to check how they behave based on the Pacman movements
        #print("Previous Food :", prevFood)
        #print("SuccessorGameState :", successorGameState.asList())
        #print("newPos :", newPos)
        #print("newFood :", newFood)
        #print("newGhostStates :", newGhostStates)
        #print("newScaredTimes :", newScaredTimes)
        #print("succ.getScore() :", successorGameState.getScore())
        #code 
        minFoodPosDistance = 100
        ghostPosSum = -1
        for foodPos in newFood.asList():
          foodPosDistance = manhattanDistance(foodPos, newPos)
          if foodPosDistance <= minFoodPosDistance:
            minFoodPosDistance = foodPosDistance
          print("minimum Food Position Distance :", minFoodPosDistance) 
        #value 3 in this case means that the Pacman will have enough time to rescue himslef in the case of both of them move into the same direction.
        #gpsum is marginal so it just hold the -1 value(in fact will be equal to 1)
        if newScaredTimes[0] > 3:
          ghostPosSum = -1
        else:
          for ghostPosition in successorGameState.getGhostPositions():
            ghostPosDistance = manhattanDistance(ghostPosition, newPos)
            ghostPosSum += ghostPosDistance
            if(ghostPosDistance < 3):
              return -500
            print("ghost position distance :", ghostPosDistance)

        """Combination of the above calculated metrics."""
        return successorGameState.getScore() + (1 / float(minFoodPosDistance)) - (1 / float(ghostPosSum))
        

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
        #in this task based on how the minmax algorithm is built both: maximer and minizer were implemented
        def minimizer(state, depth, agentIndex):
          legalActions = state.getLegalActions(agentIndex)
          numAgents = state.getNumAgents()
          #very high value to make sure that it will not be exceeded
          initValue = 10000
          if depth==self.depth or (state.isWin() or state.isLose()):
            return self.evaluationFunction(state)
          
          if agentIndex+1!=numAgents:
            for legalAction in legalActions:
              newAgentIndex = agentIndex + 1
              initValue = min(initValue, minimizer(state.generateSuccessor(agentIndex, legalAction), depth, newAgentIndex))
          else:
            for legalAction in legalActions:
              newDepth = depth + 1
              initValue = min(initValue, maximizer(state.generateSuccessor(agentIndex, legalAction), newDepth))
          return initValue
        def maximizer(state, depth):
          #very low value to make sure that it will be exceeded
          initValue = -10000
          legalActions = state.getLegalActions()
          if depth==self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
      
          for legalAction in legalActions:
            initValue = max(initValue, minimizer(state.generateSuccessor(0, legalAction), depth,1))
            score = initValue
          return score
        
        legalActions = gameState.getLegalActions()
        initValue = -10000
        dirSelect = Directions.STOP
        for legalAction in legalActions:
          actionSucc = minimizer(gameState.generateSuccessor(0, legalAction),0,1)
          if actionSucc > initValue:
            dirSelect = legalAction
            initValue = actionSucc
        return dirSelect

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maximizer(state, depth, alpha, beta):
          legalActions = state.getLegalActions()
          initValue = float(-1000)
          #numAgent = state.getNumAgents()
          if depth==self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
          
          for legalAction in legalActions:
            initValue = max(initValue, minimizer(state.generateSuccessor(0, legalAction), depth,1, alpha, beta))
            if initValue > beta:
              return initValue
            alpha = max(alpha, initValue)
          return initValue

        def minimizer(state, depth, agentIndex, alpha, beta):
          numAgent = state.getNumAgents()
          legalActions = state.getLegalActions(agentIndex)
          initValue = float(1000)
          if depth==self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
          if agentIndex+1!= numAgent:
            for legalAction in legalActions:
              newagentIndex = agentIndex + 1
              initValue = min(initValue, minimizer(state.generateSuccessor(agentIndex, legalAction), depth, newagentIndex, alpha, beta))
              if initValue < alpha:
                return initValue
              beta = min(beta, initValue)
          else:
            for legalAction in legalActions:
              
              newDepth = depth + 1
              initValue = min(initValue, maximizer(state.generateSuccessor(agentIndex, legalAction), newDepth, alpha, beta))
              if initValue < alpha:
                return initValue
              beta = min(beta, initValue)
          return initValue
        legalActions = gameState.getLegalActions()
        dirSelect = Directions.STOP
        initValue = float(-1000)
        alpha = float(-1000)
        beta = float(1000)
        for legalAction in legalActions:
          temp = minimizer(gameState.generateSuccessor(0, legalAction),0,1, alpha, beta)
          if temp > initValue:
            initValue = temp
            dirSelect= legalAction
          alpha = max(alpha, initValue)
        return dirSelect
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
        def maximizer(state, depth):
          initValue = float(-1000)
          legalActions = state.getLegalActions()
          if depth==self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
          
          for legalAction in legalActions:
            initValue = max(initValue, expecter(state.generateSuccessor(0, legalAction), depth,1))
          return initValue
        def expecter(state, depth, agentIndex):
          numAgent = state.getNumAgents()
          legalActions = state.getLegalActions(agentIndex)
          initValue = 0
          if depth ==self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
          
          
          if agentIndex+1!= numAgent:
            for legalAction in legalActions:
              newagentIndex = agentIndex + 1
              initValue += expecter(state.generateSuccessor(agentIndex, legalAction), depth, newagentIndex)
          else:
            for legalAction in legalActions:
              newDepth = depth +1
              initValue += maximizer(state.generateSuccessor(agentIndex, legalAction), newDepth)
          return initValue/len(legalActions)
        legalActions = gameState.getLegalActions()
        dirSelect = Directions.STOP
        initValue = float(-1000)
        for legalAction in legalActions:
          temp = expecter(gameState.generateSuccessor(0, legalAction),0,1)
          if temp > initValue:
            initValue = temp
            dirSelect = legalAction
        return dirSelect

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    currentPos = currentGameState.getPacmanPosition()
    currenFood = currentGameState.getFood()
    capsulePos = currentGameState.getCapsules()
    #layout = currentGameState.getWalls()
    #maxlength = layout.height - 2 + layout.width -2
    x = currentGameState.getPacmanPosition()[0]
    y = currentGameState.getPacmanPosition()[1]
    fooddistance = list()
    capsuledistance = list()
    
    score = 0
    
    for ghostState in currentGameState.getGhostStates():
      GhostDistance = manhattanDistance(currentPos, ghostState.configuration.getPosition())
      if GhostDistance < 2:
        newGhostDistance = GhostDistance + 1
        if ghostState.scaredTimer == 0: 
          score -= float(950)/(newGhostDistance)
        else:
          score += float(950)/(newGhostDistance)
    for foodPosition in currenFood.asList():
      fooddistance.append(manhattanDistance(currentPos, foodPosition))
    for capsulePosition in capsulePos:
      capsuledistance.append(manhattanDistance(capsulePosition, currentPos))
    if min(capsuledistance+[float(100)])<5:
      score += 500.0/(min(capsuledistance))
    for capsule in capsulePos:
      if(capsule[0]==currentPos[0])&(capsule[1]==currentPos[1]):
        score += 600.0
    minfooddistance = min(fooddistance+[100.0])
    return score + 1/float(minfooddistance) - len(fooddistance)

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

