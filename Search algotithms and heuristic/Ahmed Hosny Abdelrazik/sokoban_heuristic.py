from sokoban import SokobanLayout, SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented

from typing import Dict,Tuple,FrozenSet

# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use

# Heuristic 1: Manhattan distance between player and nearest crate
def heuristic_1(state: SokobanState) -> int:
    # Heuristic 1: Manhattan distance between player and nearest crate
    min_distance = float('inf')
    for crate in state.crates:
        distance = abs(state.player.x - crate.x) + abs(state.player.y - crate.y)
        min_distance = min(min_distance, distance)
    return min_distance -1 

# Heuristic 2: Manhattan distance between crate and nearest goal
def heuristic_2(problem: SokobanProblem, state: SokobanState) -> int:
    # Heuristic 2: Manhattan distance between crate and nearest goal
    min_distance = float('inf')
    for crate in state.crates:
        for goal in problem.layout.goals:
            distance = abs(crate.x - goal.x) + abs(crate.y - goal.y)
            min_distance = min(min_distance, distance)
    return min_distance

def equilidean_dist(problem: SokobanProblem, state: SokobanState) -> int:
    # Heuristic 2: Manhattan distance between crate and nearest goal
    min_distance = float('inf')
    for crate in state.crates:
        for goal in problem.layout.goals:
            distance = ((crate.x - goal.x)**2 + (crate.y - goal.y)**2)**.5
            min_distance = min(min_distance, distance)
    return min_distance

# Heuristic 3: Manhattan distance between player and nearest goal
def heuristic_3(problem: SokobanProblem, state: SokobanState) -> int:
    # Heuristic 4: Manhattan distance between player and nearest crate + Manhattan distance between crate and nearest goal
    h1 = heuristic_1(state)
    h2 = heuristic_2(problem,state)
    return h1 + h2 

def first_way(problem: SokobanProblem, state: SokobanState) -> float:
    total_distance = 0

    # Iterate over each crate and calculate the Manhattan distance to its nearest goal
    for crate in state.crates:
        min_distance = float('inf')
        for goal in problem.layout.goals:
            distance = abs(crate.x - goal.x) + abs(crate.y - goal.y)
            min_distance = min(min_distance, distance)
        total_distance += min_distance
    return total_distance
def second_way(problem: SokobanProblem, state: SokobanState) -> float:
    memo: Dict[SokobanState, float] = {}

    def calculate_heuristic(current_state: SokobanState) -> float:
        # Check if the heuristic value for the current state is already computed
        if current_state in memo:
            return memo[current_state]

        # Calculate the heuristic value (cost from the current state to the goal state)
        heuristic_value = 0
        for crate_position in current_state.crates:
            # Find the closest goal for each crate using the Manhattan distance
            min_distance = min(manhattan_distance(crate_position, goal) for goal in problem.layout.goals)
            heuristic_value += min_distance
        # Memoize the computed heuristic value for the current state
        memo[current_state] = heuristic_value
        return heuristic_value

    return calculate_heuristic(state)

def third_way(problem: SokobanProblem, state: SokobanState) -> float:
    memo = problem.cache()

    def calculate_heuristic(current_state: SokobanState) -> float:
        if current_state in memo:
            return memo[current_state]

        heuristic_value = 0
        goals = problem.layout.goals

        # Pre-calculate distances for each crate to each goal
        crate_distances = {
            crate_position: min(manhattan_distance(crate_position, goal) for goal in goals)
            for crate_position in current_state.crates
        }

        # Calculate heuristic value
        for distance in crate_distances.values():
            heuristic_value += distance

        memo[current_state] = heuristic_value
        return heuristic_value

    return calculate_heuristic(state)

def Heursitic_penalty(problem: SokobanProblem, state: SokobanState) -> float:
    # crates = state.crates
    walkable = {value: value for  value in state.layout.walkable}
    crates = {value: value for  value in state.crates}
    goals = {value: value for  value in state.layout.goals}

    # calculate number of goals that next to wall
    critical_goals = {
        'right': sum(1 for goal in goals if goal.x == state.layout.width - 2),
        'left': sum(1 for goal in goals if goal.x == 1),
        'up': sum(1 for goal in goals if goal.y == state.layout.height - 2),
        'down': sum(1 for goal in goals if goal.y == 1)
    }

    # calculate number of cretes that next to wall
    critical_crates = {
        'right': sum(1 for crate in crates if crate.x == state.layout.width - 2),
        'left': sum(1 for crate in crates if crate.x == 1),
        'up': sum(1 for crate in crates if crate.y == state.layout.height - 2),
        'down': sum(1 for crate in crates if crate.y == 1)
    }
    # Calculate the distance to the nearest Create
    min_distance=third_way(problem, state)
    # check on the penalty
    penalty_exists = any(
        corner_penalty(crate, state,
                    critical_goals['left'], critical_goals['right'], critical_goals['up'], critical_goals['down'],
                    critical_crates['right'], critical_crates['left'], critical_crates['up'], critical_crates['down'],
                    walkable, crates)
        for crate in crates if crate not in goals
    )

    return 1000000000 if penalty_exists else min_distance

def corner_penalty(point: Tuple[int, int], state: SokobanState,
                   criricalGoalsLeft:int,criricalGoalsRight:int,criricalGoalsUp:int,criricalGoalsDown:int,
                   criricalCrateRight:int,criricalCrateLeft:int,criricalCrateUp:int,criricalCrateDown:int,
                   walkable,cretes):
    x, y = point
    width,height=  state.layout.width,state.layout.height
    pRight:Point= Point(x+1,y)
    pUp:Point= Point(x,y+1)
    pDown:Point= Point(x,y-1)
    pLeft:Point= Point(x-1,y)
    pTop_Left:Point= Point(x-1,y+1)
    pTop_Right:Point= Point(x+1,y+1)
    pDown_Right:Point= Point(x+1,y-1)
    pDown_Left:Point= Point(x-1,y-1)

    #check if have 2 walls so can't move and deadlocked
    if(pRight not in walkable and pUp not in walkable):
        return True
    if(pUp not in walkable and pLeft not in walkable):
        return True
    if(pDown not in walkable and pRight not in walkable):
        return True
    if(pLeft not in walkable and pDown not in walkable):
        return True

    #check if have 2 walls so can't move and deadlocked

    if((x==1 or x==width-2) and (y==1 or y==height-2)):
        return True
    
    # create can't move in 3 directions

    if( (pLeft not in walkable or pLeft in cretes) and (pUp not in walkable or pUp in cretes) and 
       (pTop_Left not in walkable or pTop_Left in cretes)):
        return True
    if( (pRight not in walkable or pRight in cretes) and (pUp not in walkable or pUp in cretes) and 
       (pTop_Right not in walkable or pTop_Right in cretes)):
        return True
    if( (pRight not in walkable or pRight in cretes) and (pDown not in walkable or pDown in cretes) and 
       (pDown_Right not in walkable or pDown_Right in cretes)):
        return True
    if( (pLeft not in walkable or pLeft in cretes) and (pDown not in walkable or pDown in cretes) and 
       (pDown_Left not in walkable or pDown_Left in cretes)):
        return True
    
    
    nextWall=False

    if(pLeft not in walkable):
        nextWall=True

    if( pRight not in walkable):
        nextWall=True
    
    if(pUp not in walkable):
        nextWall=True

    if( pDown not in walkable):
        nextWall=True

    # check if number of goals next to wall < number of cretes next to wall

    if criricalGoalsLeft < criricalCrateLeft:
        return True
    if criricalGoalsRight < criricalCrateRight:
        return True
    if criricalGoalsUp < criricalCrateUp:
        return True
    if criricalGoalsDown < criricalCrateDown:
        return True

    # check if two cretes next to each other and next to wall
    if any(
    (crete in {point + Point(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)})
    and nextWall
    and (crete.x in {1, width - 2} or crete.y in {1, height - 2})
    for crete in state.crates
    if crete != point
    ):
        return True
    return False
    
def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    #TODO: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    # Extract grid layout, player position, and crates
    
    return Heursitic_penalty(problem, state)
    # NotImplemented()