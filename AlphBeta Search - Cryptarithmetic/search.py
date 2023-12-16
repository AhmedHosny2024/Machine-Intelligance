from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    agent = game.get_turn(state)
    terminal, values = game.is_terminal(state)
    if terminal: 
        if agent == 0:
                return values[agent], None #if it is terminal return the value for the player
        else:
            return -values[agent], None 

    # if max depth
    if max_depth == 0:
        # if my turn i need to maximize  
        if agent==0:
            return heuristic(game, state, agent), None
        # my enemy tern i need to minimize
        else:
            return -heuristic(game, state, agent), None
    if agent == 0:  # Max node
        value, _, action = max((minimax(game, game.get_successor(state, action), heuristic, max_depth - 1)[0], -index, action) for index, action in enumerate(game.get_actions(state)))
    else:  # Min node
        value, _, action = min((minimax(game, game.get_successor(state, action), heuristic, max_depth - 1)[0], -index, action) for index, action in enumerate(game.get_actions(state)))

    return value, action
    # NotImplemented()

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def alphabetaRecursion(state: S, alpha,beta ,max_depth: int = -1) :
        agent = game.get_turn(state)
        terminal, values = game.is_terminal(state)
        if terminal: 
            if agent == 0:
                return values[agent], None #if it is terminal return the value for the player
            else:
                return -values[agent], None 
        # if max depth
        if max_depth == 0:
            # if my turn i need to maximize  
            if agent==0:
                return heuristic(game, state, agent), None
            # my enemy tern i need to minimize
            else:
                return -heuristic(game, state, agent), None
        if agent == 0:  # Max node
            val= float("-inf")
            best_action=None
            for action in game.get_actions(state):
                val = max(val, alphabetaRecursion(game.get_successor(state, action), alpha,beta, max_depth - 1)[0])
                if val > alpha:
                    alpha = val
                    best_action = action
                if alpha >= beta:
                    break
            return val, best_action
        else:  # Min node
            val= float("inf")
            best_action=None
            for action in game.get_actions(state):
                val = min(val, alphabetaRecursion(game.get_successor(state, action), alpha,beta, max_depth - 1)[0])
                if val < beta:
                    beta = val
                    best_action = action
                if alpha >= beta:
                    break
            return val, best_action
    return alphabetaRecursion(state, float("-inf"),float('inf'), max_depth)
    # NotImplemented()

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def recursion(state: S, alpha,beta ,max_depth: int = -1) :
        agent = game.get_turn(state)
        terminal, values = game.is_terminal(state)
        if terminal: 
            if agent == 0:
                return values[agent], None #if it is terminal return the value for the player
            else:
                return -values[agent], None 
        # if max depth
        if max_depth == 0:
            # if my turn i need to maximize  
            if agent==0:
                return heuristic(game, state, agent), None
            # my enemy tern i need to minimize
            else:
                return -heuristic(game, state, agent), None
        if agent == 0:  # Max node
            val= float("-inf")
            best_action=None
            actions = game.get_actions(state)
            actions.sort(key=lambda action: heuristic(game, game.get_successor(state, action), agent), reverse=True)
            for action in actions:
                val = max(val, recursion(game.get_successor(state, action), alpha,beta, max_depth - 1)[0])
                if val > alpha:
                    alpha = val
                    best_action = action
                if alpha >= beta:
                    break
            return val, best_action
        else:  # Min node
            val= float("inf")
            best_action=None
            actions = game.get_actions(state)
            actions.sort(key=lambda action: heuristic(game, game.get_successor(state, action), agent), reverse=True)
            for action in actions:
                val = min(val, recursion(game.get_successor(state, action), alpha,beta, max_depth - 1)[0])
                if val < beta:
                    beta = val
                    best_action = action
                if alpha >= beta:
                    break
            return val, best_action
    return recursion(state, float("-inf"),float('inf'), max_depth)
    # NotImplemented()

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    def recursion(state: S, max_depth: int = -1) :
        agent = game.get_turn(state)
        terminal, values = game.is_terminal(state)
        if terminal: 
            if agent == 0:
                return values[agent], None #if it is terminal return the value for the player
            else:
                return -values[agent], None 
        # if max depth
        if max_depth == 0:
            # if my turn i need to maximize  
            if agent==0:
                return heuristic(game, state, agent), None
            # my enemy tern i need to minimize
            else:
                return -heuristic(game, state, agent), None
        if agent == 0:  # Max node
            val= float("-inf")
            best_action=None
            for action in game.get_actions(state):
                newval =  recursion(game.get_successor(state, action), max_depth - 1)[0]
                # get the max value of all actions
                if (val < newval):
                    val = newval
                    # update the best action
                    best_action = action
            return val, best_action
        else:  # Min node
            val= 0
            actions = game.get_actions(state)
            for action in actions:
                # sum all actions values then divide by number of actions
                val += recursion(game.get_successor(state, action), max_depth - 1)[0]
            # all actions have the same probability so return any one of them
            return val/len(actions), action
    return recursion(state, max_depth)
    # NotImplemented()