import random, string, collections, heapq

# Subsitutes character if mapping exists from current to substitution
# Assumes current and substitution are Capital Strings with no repeating characters
# Case of return character is same as input character
def substitute(character, current, substitution):
    if character.upper() not in current:
        return character
    index_in_substitution = current.find(character.upper())
    if character.isupper():
        return substitution[index_in_substitution]
    return substitution[index_in_substitution].lower()

# Uses substitution cipher to encrypt text
# To encrypt just call encrypt(text, key) where
# key is a permutation of sting.ascii_uppercase
# 
# To decrypt, just call encrypt(text, string.ascii_uppercase, key)
# with the key used to encrypt
def encrypt(text, key, original=string.ascii_uppercase):
    result = ""
    for char in text:
        letter = substitute(char, original, key)
        result += letter
    return result

# Returns random permutation (as a string) of string.ascii_uppercase
def generateKey():
    key = list(string.ascii_uppercase)
    random.shuffle(key)
    return ''.join(key)

# Returnes text with added noise.
# Each alphabet character has noise chance of getting changed to another random alphabet letter of same case
def add_noise(text, noise):
    result = ""
    for letter in text:
        if letter in string.ascii_letters and random.random() < noise:
            random_letter = randomLetter()
            letter = random_letter.upper() if letter.isupper() else random_letter.lower()
        result += letter
    return result
    
# From CS221 Text Reconstruction Assignment

class SearchProblem:
    # Return the start state.
    def startState(self): raise NotImplementedError("Override me")

    # Return whether |state| is a goal state or not.
    def isGoal(self, state): raise NotImplementedError("Override me")

    # Return a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|.
    def succAndCost(self, state): raise NotImplementedError("Override me")

class SearchAlgorithm:
    # First, call solve on the desired SearchProblem |problem|.
    # Then it should set two things:
    # - self.actions: list of actions that takes one from the start state to a goal
    #                 state; if no action sequence exists, set it to None.
    # - self.totalCost: the sum of the costs along the path or None if no valid
    #                   action sequence exists.
    def solve(self, problem): raise NotImplementedError("Override me")

# Data structure for supporting uniform cost search.
class PriorityQueue:
    def  __init__(self):
        self.DONE = -100000
        self.heap = []
        self.priorities = {}  # Map from state to priority

    # Insert |state| into the heap with priority |newPriority| if
    # |state| isn't in the heap or |newPriority| is smaller than the existing
    # priority.
    # Return whether the priority queue was updated.
    def update(self, state, newPriority):
        oldPriority = self.priorities.get(state)
        if oldPriority == None or newPriority < oldPriority:
            self.priorities[state] = newPriority
            heapq.heappush(self.heap, (newPriority, state))
            return True
        return False

    # Returns (state with minimum priority, priority)
    # or (None, None) if the priority queue is empty.
    def removeMin(self):
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)
            if self.priorities[state] == self.DONE: continue  # Outdated priority, skip
            self.priorities[state] = self.DONE
            return (state, priority)
        return (None, None) # Nothing left...


class UniformCostSearch(SearchAlgorithm):
    def __init__(self, verbose=0):
        self.verbose = verbose

    def solve(self, problem):
        # If a path exists, set |actions| and |totalCost| accordingly.
        # Otherwise, leave them as None.
        self.actions = None
        self.totalCost = None
        self.numStatesExplored = 0

        # Initialize data structures
        frontier = PriorityQueue()  # Explored states are maintained by the frontier.
        backpointers = {}  # map state to (action, previous state)

        # Add the start state
        startState = problem.startState()
        frontier.update(startState, 0)

        while True:
            # Remove the state from the queue with the lowest pastCost
            # (priority).
            state, pastCost = frontier.removeMin()
            if state == None: break
            self.numStatesExplored += 1
            if self.verbose >= 2:
                print "Exploring %s with pastCost %s" % (state, pastCost)

            # Check if we've reached the goal; if so, extract solution
            if problem.isGoal(state):
                self.actions = []
                while state != startState:
                    action, prevState = backpointers[state]
                    self.actions.append(action)
                    state = prevState
                    self.actions.reverse()
                    self.totalCost = pastCost
                if self.verbose >= 1:
                    print "numStatesExplored = %d" % self.numStatesExplored
                    print "totalCost = %s" % self.totalCost
                    print "actions = %s" % self.actions
                return

            # Expand from |state| to new successor states,
            # updating the frontier with each newState.
            for action, newState, cost in problem.succAndCost(state):
                if self.verbose >= 3:
                    print "  Action %s => %s with cost %s + %s" % (action, newState, pastCost, cost)
                if frontier.update(newState, pastCost + cost):
                    # Found better way to go to |newState|, update backpointer.
                    backpointers[newState] = (action, state)
        if self.verbose >= 1:
            print "No path found"
