import random
import numpy as np
import experiment_objects.Robot as r
import main as m

# Robot parameters
UPDATE_INTERVAL = 200
SAMPLE_CYCLE_LENGTH = 15
SAMPLE_INTERVAL = 400
SPEED = 0.01
COMMUNICATION_RANGE = 2
POSITION = None#[0,0]
SAMPLE_COLOUR = None
DECISION_STATE = 2
COMMITED_ESTIMATION = 0.8


class Environment:
    """
    Object containing the grid and robots for the experiment.
    """
    def __init__(self, grid_size, colour_prob, num_robots, robot_params, interval, experiment_length, gradual_change=None) -> None:
        self.grid_size = grid_size
        self.grid = create_grid(grid_size, colour_prob)
        self.colour_prob = colour_prob
        self.majority_colour = np.argmax(colour_prob) + 1
        self.num_states = len(colour_prob) + 1
        self.num_robots = num_robots
        self.robots = [r.Robot(i, self, *robot_params) for i in range(num_robots)]
        self.time = 0
        self.interval = interval
        self.experiment_length = experiment_length
        self.state_history = [self.get_state()]
        self.time_history = [0]
        self.adaptation_time = None
        if gradual_change == None:
            self.gradual_change = gradual_change
        else:
            self.gradual_change = gradual_change
            self.final_proportion = gradual_change[0] # proportion of majority colour at end of gradual change
            self.change_time = gradual_change[1] # time it takes to reach final proportion
            self.change_rate = 0.1 / (self.change_time / 300) # rate of change of proportion of majority colour

    def run_for_visual(self):
        while self.time < self.experiment_length:
            if self.time % 100 == 0:
                #print(f"Time: {self.time}")
                pass
            if self.gradual_change != None:
                if self.time % 300 == 0 and self.time > 0 and self.time <= self.change_time:
                    self.colour_prob = [self.colour_prob[0] - self.change_rate, self.colour_prob[1] + self.change_rate]
                    self.grid = create_grid(self.grid_size, self.colour_prob)
                    #print(f"Time: {self.time}, Colour Prob: {self.colour_prob}")
            for robot in self.robots:
                robot.step_robot(self.grid, self.robots)
            if self.time % 200 == 0:
                #print(f"{self.time}: {self.get_state()}")
                #print(f"{self.time}: {self.get_sampling_colour_counts()}")
                pass
            self.time += self.interval
            yield None
    
    def run(self):
        while self.time < self.experiment_length:
            #if self.time == 4000:
            #    self.grid = create_grid(self.grid_size, [0.9,0.1])
            for robot in self.robots:
                robot.step_robot(self.grid, self.robots)
            if self.time % 200 == 0:
                print(f"{self.time}: {self.get_state()}")
                current_state = self.get_state()
                self.state_history.append(current_state)
                self.time_history.append(self.time)
                if current_state[self.majority_colour] / self.num_robots > 0.7:
                    if self.adaptation_time == None:
                        self.adaptation_time = self.time
                    else:
                        if self.time - self.adaptation_time > 2 * 60 * 100:
                            return True
                else:
                    self.adaptation_time = None
            self.time += self.interval
        self.adaptation_time = None
        return False

    def get_state(self):
        """
        Count the number of robots in each state currently: undecided, colour 1, colour 2, ...
        """
        state_count = [0 for i in range(self.num_states)]
        for robot in self.robots:
            state_count[robot.decision_state] += 1
        return state_count

    def get_sampling_colour_counts(self):
        """
        Count the number of robots in each sampling colour currently: undecided, colour 1, colour 2, ...
        """
        colour_count = [0 for i in range(self.num_states)]
        for robot in self.robots:
            if robot.sample_colour == None:
                colour_count[0] += 1
            else:
                colour_count[robot.sample_colour] += 1
        return colour_count
            

def create_grid(size, colour_prob):
    """
    Create a grid from a distribution of colours
    params:
      size: (Tuple : int) # col, # row. number of rows and cols of squares in grid
      colour_prob: (List : float) probability distribution of each colour, where colour is represented by index + 1
    return: (List[List : int])
    """
    colour_ints = [i + 1 for i in range(len(colour_prob))]
    colours = random.choices(colour_ints, colour_prob, k=size[0] * size[1])
    return [[colours[size[0] * row + col] for col in range(size[0])] for row in range(size[1])]
    
    
