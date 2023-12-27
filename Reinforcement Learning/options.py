# This file contains the options that you should modify to solve Question 2

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    return {
        "noise": 0,
        "discount_factor": 1, # we need to take the future reword into account
        "living_reward": -5   # give a negative reward to encourage the agent to reach the terminal state as soon as possible
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,
        "discount_factor": 0.2, # we need to go 1 not 10 so make value of discount_factor small as we go far from the terminal state the value of the utility will be small (gamma,gamma^2,gamma^3,....)
        "living_reward": -1.0   # give it normal reward to encourage the agent to reach the terminal state in the long safe path, but not the longest(not to +10)
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1.2, # increase the discount factor more than one, to make the factor increase as we go furthur (gamma^2, gamma^3 ..etc) to don't make the agent more greedy and instead of going to the near terminal state it will go to the furthur one terminal state
        "living_reward": -5     # give a negative reward to encourage the agent to reach the terminal state as soon as possible
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
        return {
        "noise": 0.2,
        "discount_factor": 1.5, # increase the discount factor more than one, to make the factor increase as we go furthur (gamma^2, gamma^3 ..etc) to don't make the agent more greedy and instead of going to the near terminal state it will go to the furthur one terminal state
        "living_reward": -5     # give a negative reward to encourage the agent to reach the terminal state as soon as possible
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": 100 # why go to terminal while you can get a high reward as we go forever in the grid so i give a very high positive reward to encourage the agent to not go to the terminal state
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -100 # to reach the terminal state as soon as possible so i give a very high negative reward 
    }