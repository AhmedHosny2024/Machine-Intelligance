from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #TODO: Write this function
    # loop on all constraints
    for constrain in problem.constraints:
        # get the binary constraints that involve the assigned variable
        if isinstance(constrain, BinaryConstraint) and assigned_variable in constrain.variables:
            # get the other involved variable.
            other_variable = constrain.get_other(assigned_variable)
            # if the other variable has no domain (in other words, it is already assigned), skip this constraint.
            newvar = domains.get(other_variable)
            if not newvar:
                continue
            # Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
            new_domain = {value for value in domains[other_variable] if constrain.condition(assigned_value, value)}
            # if any variable's domain becomes empty, return False. Otherwise update the domain
            if not new_domain:
                return False
            domains[other_variable] = new_domain
    return True
    # NotImplemented()

# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #TODO: Write this function
    new_domain = []
    for value in domains[variable_to_assign]:
        # initaily add 0 for this variable value in the new domain
        new_domain.append((value, 0))
        # loop on all constraints
        for constrain in problem.constraints:
            # get the binary constraints that involve the assigned variable
            if isinstance(constrain, BinaryConstraint) and variable_to_assign in constrain.variables:
                # get the other involved variable.
                other_variable = constrain.get_other(variable_to_assign)
                # if the other variable has no domain (in other words, it is already assigned), skip this constraint.
                newvar = domains.get(other_variable)
                if not newvar:
                    continue
                # Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
                new_domain[-1] = (value, new_domain[-1][1] + len([x for x in domains[other_variable] if not constrain.condition(value, x)]))
    # sort the new domain based on the least restraining value heuristic
    new_domain.sort(key=lambda x: (x[1],x[0]))
    return [x[0] for x in new_domain]
    # NotImplemented()

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.

def solve(problem: Problem) -> Optional[Assignment]:
    # initial assignment is empty
    empty_assignment = {}
    if not one_consistency(problem):  # Check 1-consistency for an empty assignment
        return None
    return solve_recursive(problem,empty_assignment, problem.domains)  # Pass a copy of problem domains

def solve_recursive(problem:Problem,assignment: Dict[str, Any], domains: Dict[str, set]) -> Optional[Assignment]:
    # check if the assignment is complete
    if problem.is_complete(assignment):
        return assignment
    # get the variable that should be picked based on the MRV heuristic.
    var = minimum_remaining_values(problem, domains)
    # get the domain of the given variable order based on the "least restraining value" heuristic.
    values=least_restraining_values(problem, var, domains)
    # loop on all values
    for value in values:
        # assign the value to the variable
        assignment[var] = value
        # create a copy of the domains
        new_domains = domains.copy()
        # remove the variable from the domains
        new_domains.pop(var)
        # forward checking
        if forward_checking(problem, var, value, new_domains):
            # recursive call
            result = solve_recursive(problem,assignment, new_domains)  # Pass a copy of domains
            if result:
                return result
        # if the result is None, remove the variable from the assignment
        del assignment[var]
    return None
#     # NotImplemented()
    