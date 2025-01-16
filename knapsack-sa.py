import random
import csv
import math

# File containing the items data
ITEMS_FILE = "knapsack_items.csv"

# Knapsack constraints
MAX_WEIGHT = 16  # in kg
MAX_VOLUME = 13  # in L

# Create a class of SA algorithms to solve the knapsack problem
class KnapsackSA():
    def __init__(self,
                 max_weight: int,
                 max_volume: int,
                 initial_solution: list, 
                 initial_temperature: int,
                 end_temperature: float = 0.01,
                 cooling_type: str = "rate",
                 cooling_rate: float = 0.95, 
                 cooling_difference: float = 0.01):
        '''
        Preconditions:
        - cooling_type is either "rate" or "difference"
        - end_temp >= 0
        - 0 < cooling_rate < 1
        - 0 < cooling_difference'''

        self.solution = initial_solution
        self.temp = initial_temperature
        self.end_temp = end_temperature
        self.cooling_type = cooling_type
        self.cooling_rate = cooling_rate
        self.cooling_difference = cooling_difference
        self.max_weight = max_weight
        self.max_volume = max_volume
        

    # Define the objective function
    def reward_func(self, solution):
        '''Return the value of the items in the knapsack according to solution,
        if the constraints are met.
        If the constraints are not met return the negative sum of the weight and volume
        of all items in the knapsack.'''

        value = 0
        weight = 0
        volume = 0

        # Evaluate each item in the knapsack
        for idx, parameter in enumerate(solution):
            if parameter == 1:
                item = items[idx]
                value += item["Value"]
                weight += item["Weight"]
                volume += item["Volume"]
        
        if weight > self.max_weight or volume > self.max_volume:
            # Penalize the reward if the constraints are not respected
            return -(weight + volume)
        else:
            # Reward the value of the items in the knapsack if constraints are met
            return value

    # Define the perturbation function to generate neighbouring solutions
    def create_neighbour(self):
        '''Return a copy of the current solution with a random parameter flipped.'''

        new_solution = self.solution.copy()
        rand_idx = random.randint(0, len(self.solution) - 1)

        if new_solution[rand_idx] == 0:
            new_solution[rand_idx] = 1
        elif new_solution[rand_idx] == 1:
            new_solution[rand_idx] = 0
        
        return new_solution

    # Define the acceptance function
    def acceptance_func(self, reward_delta):
        '''Return True if the new solution is accepted, else return False.
        The decision is based on the difference of reward between the new solution
        and the current one, and the current temperature.'''

        if reward_delta > 0:
            # Accept any solution that yields a better reward than the current one
            return True
        else:
            return random.random() <= math.exp(reward_delta / self.temp)

    def run(self):
        while self.temp > self.end_temp:
            new_solution = self.create_neighbour()
            reward_delta = self.reward_func(new_solution) - self.reward_func(self.solution)

            if self.acceptance_func(reward_delta):
                self.solution = new_solution

            # Cool down the temperature
            if self.cooling_type == "rate":
                self.temp = self.cooling_rate * self.temp
            elif self.cooling_type == "difference":
                self.temp = self.temp - self.cooling_difference

# Initialize a list with the items data
with open(ITEMS_FILE) as file:
    reader = csv.reader(file)
    header = next(reader)
    items = [{"Name" : row[0],
              "Value" : int(row[1]),
              "Weight" : int(row[2]),
              "Volume" : int(row[3])} for row in reader]

# Parameters for the SA algorithm
initial_solution = random.choices([0, 1], k = len(items))
initial_temp = 10000
end_temp = 0.0001

cooling_type = "rate"
cooling_rate = 0.9999

# Run the SA
sa = KnapsackSA(max_weight=MAX_WEIGHT,
                max_volume=MAX_VOLUME,
                initial_solution=initial_solution, 
                initial_temperature=initial_temp, 
                end_temperature=end_temp,
                cooling_type=cooling_type,
                cooling_rate=cooling_rate)

sa.run()

# Print results
print(f"Optimal solution: {sa.solution}")
print(f"Reward of optimal solution: {sa.reward_func(sa.solution)}")