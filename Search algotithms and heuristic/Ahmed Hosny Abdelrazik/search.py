from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE

    #initial state is the goal
    if(problem.is_goal(initial_state)):return [initial_state]

    # we make frontier list of tuples (state , path)  like queue first in first out
    frontier = [(initial_state,[])]

    # create explored set
    explored=set()
    # loop on all nodes in frontier
    while frontier:
        # get the first element from the frontier
        nodeState,path=frontier.pop(0)
        if(nodeState not in explored):
            # add nodeState to explored set
            explored.add(nodeState)
            # loop on all actions to get the child node
            for action in problem.get_actions(nodeState):
                child = problem.get_successor(nodeState, action)
                if( (child not in explored) and (child not in frontier)):
                    # check if the child is goal if goal return path else add to frontier
                    if(problem.is_goal(child)):
                        return path+[action]
                    frontier.append((child,path+[action]))
                    # frontierPath.append(newPath)
    return None

    # NotImplemented()

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE

    #initial state is the goal
    if(problem.is_goal(initial_state)):return [initial_state]
    # we make frontier list of tuples (state , path) like stack last in first out
    frontier = [(initial_state,[])]
    # create explored set
    explored=set()
    # loop on all nodes in frontier
    while frontier:
        # get the last element from the frontier last element inserted to list is the first element poped
        nodeState,path=frontier.pop()
        if(nodeState not in explored):
            # check if node is goal then return path
            if(problem.is_goal(nodeState)):
                return path
            # add nodeState to explored set
            explored.add(nodeState)
            # loop on all actions to get the child node
            for action in problem.get_actions(nodeState):
                child = problem.get_successor(nodeState, action)
                if( (child not in explored) and (child not in frontier)):                    
                    frontier.append((child,path+[action]))
    return None
    # NotImplemented()
    
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE

    #initial state is the goal
    if(problem.is_goal(initial_state)):
        return [initial_state]

    index : int =0
    # each one add to node as tuple of (cost , node , path)
    cost: float =0.0
    # we make frontier list of tuples (cost , index , state , path) periority queue with the cost then index if the cost is equal so no need for check and replace if better cost
    # we but index so if cost is equal insert the node in the last not first 
    frontier = [(cost,(index,initial_state),[])]
    heapq.heapify(frontier)
    # create explored set
    explored=set()
    # loop on all nodes in frontier
    while frontier:
        # get the firest element from the frontier
        newCost,(_,nodeState),path=heapq.heappop(frontier)
        #check if expolred before or not
        if(nodeState not in explored):
            # check if goal
            if(problem.is_goal(nodeState)):
                return path
            # add nodeState to explored set
            explored.add(nodeState)
            # loop on all actions to get the child node
            for action in problem.get_actions(nodeState):
                child = problem.get_successor(nodeState, action)
                index+=1
                # the cost is the cumulative cost of the path 
                cost2 = newCost + problem.get_cost(nodeState,action)
                # check if node in the explored set or in frontier
                if( (child not in explored) and (child not in frontier)):            
                    heapq.heappush(frontier,(cost2,(index,child), path+[action] )) 
    return None
    # NotImplemented()


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction):
    node = initial_state
    index=0
    # we make frontier list of tuples (cost , index , state , path) periority queue with the cost then index if the cost is equal to compare with it instead of graph node
    frontier = [(0,index, node,[])]
    # create the explored set
    explored = set()
    # we need this dic to optimize the search in frontier complexity
    optimize_Search_In_Forintier={node}
    # loop in the frontier
    while frontier:
        # pop the node with least cost
        cost,_,node,path = heapq.heappop(frontier)
        optimize_Search_In_Forintier.remove(node)
        if(node not in explored):
            # check if goal
            if problem.is_goal(node):
                return path
            explored.add(node)
            # get all actions from this node
            for action in problem.get_actions(node):
                # get the child node
                child = problem.get_successor(node, action)
                # the cost is the cumulative cost of the path + the heuristic value
                # We removed the heuristic value of the parent as heuristic can't be summed up
                cost2 = cost-heuristic(problem,node) + problem.get_cost(node,action) + heuristic(problem,child)
                # increast the index
                index+=1
                # check if node in the explored set or in frontier
                if child not in explored and child not in optimize_Search_In_Forintier:
                    heapq.heappush(frontier, (cost2, index,child, path+[action]))
                    optimize_Search_In_Forintier.add(child)
                # check if the node in frontier with higher cost then replace it with the new cost and path
                elif child in frontier:
                    if cost2 < frontier[child]:
                        del frontier[child]
                        heapq.heappush(frontier, (cost2, child, path+[action]))
    return None

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
        #TODO: ADD YOUR CODE HERE
    node = initial_state
    index :int=0
    # we make frontier list of tuples (cost , index , state , path) periority queue with the cost then index if the cost is equal to compare with it instead of graph node
    frontier = [(0,index, node,[])]
    # create the explored set
    explored = set()
    # we need this dic to optimize the search in frontier complexity
    optimize_Search_In_Forintier={node}
    # loop in the frontier
    while frontier:
        # pop the node with least cost
        cost,_,node,path = heapq.heappop(frontier)
        optimize_Search_In_Forintier.remove(node)
        if(node not in explored):
            # check if goal
            if problem.is_goal(node):
                return path
            explored.add(node)
            # get all actions from this node
            for action in problem.get_actions(node):
                # get the child node
                child = problem.get_successor(node, action)
                # the cost is the heuristic value
                cost2 = cost-heuristic(problem,node) + heuristic(problem,child)
                # increast the index
                index+=1
                # check if node in the explored set or in frontier
                if child not in explored and child not in optimize_Search_In_Forintier:
                    heapq.heappush(frontier, (cost2, index,child, path+[action]))
                    optimize_Search_In_Forintier.add(child)
    return None