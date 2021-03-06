import random
import eval
import reflex
import util
import numpy

class RandomAgent():
    def __init__(self):
        pass

    def getAction(self, gameState, index, validActions):
        actions = gameState.getLegalActions(index, validActions)
        return None if len(actions) == 0 else random.choice(actions)

class UpDownAgent():
    def __init__(self):
        self.upMove, self.downMove = 0, 2
        self.lastMove = self.upMove

    def getAction(self, gameState, index, validActions):
        if gameState.isLose():
            return None
        if index == 0: # human player
            if self.lastMove == self.upMove:
                self.lastMove = self.downMove
            else:
                self.lastMove = self.upMove
            return self.lastMove
        else:
            actions = gameState.getLegalActions(index, validActions)
            return None if len(actions) == 0 else random.choice(actions)

class UpLeftAgent():
    def __init__(self):
        self.upMove, self.leftMove = 0, 3
        self.lastMove = self.upMove

    def getAction(self, gameState, index, validActions):
        if gameState.isLose():
            return None
        if index == 0: # human player
            if self.lastMove == self.upMove:
                self.lastMove = self.leftMove
            else:
                self.lastMove = self.upMove
            return self.lastMove
        else:
            actions = gameState.getLegalActions(index, validActions)
            return None if len(actions) == 0 else random.choice(actions)

class ExpectimaxAgent():
    def __init__(self, depth=2, evalFn=eval.eval_snake):
        self.depth = depth
        self.evalFn = evalFn

    def getAction(self, gameState, index, validActions):
        # Return (minimax value Vopt(state), random number, optimal action pi_opt(state))
        def recurse(gameState, index, depth):
            if gameState.isLose():
                return gameState.getScore(), random.random(), None
            if depth == 0:
                return self.evalFn(gameState), random.random(), None

            if index == 0: # human
                return max([(recurse(gameState.generateSuccessor(index, action), 1, depth)[0], random.random(), action) for action in gameState.getLegalActions(index, validActions)])
            elif index == 1: # computer
                return sum([recurse(gameState.generateSuccessor(index, action), 0, depth - 1)[0] for action in gameState.getLegalActions(index, validActions)]) / len(gameState.getLegalActions(index, validActions)), random.random(), random.choice(gameState.getLegalActions(index, validActions))
        utility, rand, action = recurse(gameState, index, self.depth)
        return action

    def getComputerAction(self, gameState, validActions):
        actions = gameState.getLegalActions(1, validActions)
        return None if len(actions) == 0 else random.choice(actions)

class MinimaxAgent():
    def __init__(self, depth=3, evalFn=eval.eval_snake):
        self.depth = depth
        self.evalFn = evalFn

    def getAction(self, gameState, index, validActions):
        # Return (minimax value Vopt(state), random number, optimal action pi_opt(state))
        def recurse(gameState, index, depth):
            if gameState.isLose():
                return gameState.getScore(), random.random(), None
            if depth == 0:
                return self.evalFn(gameState), random.random(), None

            if index == 0: # humam
                return max([(recurse(gameState.generateSuccessor(index, action), 1, depth)[0], random.random(), action) for action in gameState.getLegalActions(index, validActions)])
            elif index == 1: # computer
                return min([(recurse(gameState.generateSuccessor(index, action), 0, depth - 1)[0], random.random(), action) for action in gameState.getLegalActions(index, validActions)])
        utility, rand, action = recurse(gameState, index, self.depth)
        return action

class AlphaBetaAgent():
    def __init__(self, depth=3, evalFn=eval.eval_snake):
        self.depth = depth
        self.evalFn = evalFn

    def getAction(self, gameState, index, validActions):
        def recurse(gameState, index, depth, alpha, beta):
            if gameState.isLose():
                return gameState.getScore(), random.random(), None
            if depth == 0:
                return self.evalFn(gameState), random.random(), None
            if index == 0: # human
                maximum = (float('-inf'), random.random(), None)
                for action in gameState.getLegalActions(index, validActions):
                    maximum = max(maximum, (recurse(gameState.generateSuccessor(index, action), 1, depth, alpha, beta)[0], random.random(), action))
                    alpha = max(alpha, maximum[0]) # maximum[0] is the max utility
                    if beta <= alpha:
                        break
                return maximum
            elif index == 1: # computer
                minimum = (float('inf'), random.random(), None)
                for action in gameState.getLegalActions(index, validActions):
                    minimum = min(minimum, (recurse(gameState.generateSuccessor(index, action), 0, depth - 1, alpha, beta)[0], random.random(), action))
                    beta = min(beta, minimum[0]) # minimum[0] is the min utility
                    if beta <= alpha:
                        break
                return minimum

        utility, rand, action = recurse(gameState, index, self.depth, float('-inf'), float('inf'))
        return action

class LogisticAgent():
    def __init__(self, feature_transform):
        self.feature_transform = feature_transform
        self.predict = reflex.train(feature_transform)

    def getAction(self, gameState, index, validActions):
        if gameState.isLose():
            return None
        actions = gameState.getLegalActions(index, validActions)
        if index == 0: # human player
            unrolled = util.unroll_board(gameState.board)
            x = numpy.asarray(unrolled)
            x = x.reshape(1, x.shape[0])
            if self.feature_transform:
                x = numpy.log2(x)
            predictions = [(self.predict[move](x), move) for move in range(4)]
            predictions.sort(reverse=True)
            if predictions[0][1] in validActions:
                return predictions[0][1]
            else:
                print('Falling back to second choice since {} was last moved'.format(predictions[0][1]))
                return predictions[1][1]
        else:
            return None if len(actions) == 0 else random.choice(actions)