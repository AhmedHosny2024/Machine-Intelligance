from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Dict[int,Point]

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        currentState = dict((i,pos) for i, pos in enumerate(self.cars))
        # return self.cars
        return currentState
        # NotImplemented()
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #TODO: ADD YOUR CODE HERE
        # loop on all states now to check if it goal or no 
        for i ,pos in state.items():
            # check if the car position is in the slots dictionariy before check its right car in right position 
            if pos in self.slots:
                # check of the car in right position or not
                if i !=self.slots[pos]:
                    # if the car in wrong position return false
                    return False
            # if the car in position which is not parking return false
            else: 
                return False
        return True
        # NotImplemented()
   
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE

        res:List=[]
        # loop on all states 
        for i,pos in state.items():
            # loop on all directions
            for dir in Direction:
                # get new position in each direction for the car
                newpos :Point =pos+dir.to_vector() 
                # check if its valid position if not continue
                if(newpos not in self.passages): continue
                # check if another car in this position now if yes continue
                if(newpos in state.values()): continue
                # then its valid position for the car so append it to result
                res.append((i,dir))
        return res
        # NotImplemented()
    
    # # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE

        # get the number of car from action
        carnum:int = action[0]
        # get the direction to move from action
        dir:Direction=action[1]
        # # convert state to list as it tuple so can't modify it
        # listState:list[Point] =list(state)
        # # change the car position
        # listState[carnum]=listState[carnum]+dir.to_vector()
        # # return tuple of the new state

        # change the car position
        state[carnum]=state[carnum]+dir.to_vector()
        return state
        # return Tuple[listState]
        # NotImplemented()

    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #TODO: ADD YOUR CODE HERE

        # get the number of car from action
        carnum:int = action[0]
        # get the direction to move from action
        dir:Direction =action[1]
        #get the car new position
        newpos:Point =state[carnum]+dir.to_vector()
        if(newpos in self.slots):
            if(carnum != self.slots[newpos]):
                return 100 + 26-carnum
        return 26-carnum
        # NotImplemented()
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
