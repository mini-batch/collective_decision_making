import random
import numpy as np
import math

class Robot:
    """
    Simulated robot.
    attributes:
      experimental parameters:
        update_interval: (int) The time the robot waits between updating its decision state
        sample_cycle_length: (int) Number of samples to collect in a cycle
        sample_interval: (int) Time between each sample
        speed: (float)
        env_interval: (float)
        grid_size: (Tuple: int) width by height of grid in cm's
      within-experiment variables:
        position: (List : int) (x, y) co-ordinates of Robot
        sample_colour: (int) The colour that the robot is sampling for currently
        decision_state: (int) Indicates which state the robot is in: 0 is undetermined, 1 is commited to colour 1, 2 is commited to colour 2, ...
        commited_estimation: (float) Concentration estimate for the colour the robot is commited to (if they are)
        neighbour_message: (int) The last received message from a recruiting neighbour - the colour of the neighbours opinion.
    """
    def __init__(self, id, environment, update_interval, sample_cycle_length, sample_interval, speed, communication_range, env_interval, grid_size, sample_colour, decision_state, commited_estimation, position) -> None:
        # ID (index in robots list)
        self.id = id
        # Environment the robot is within
        self.environment = environment
        # How often to update opinion
        self.update_interval = update_interval
        # Number of samples to take in a cycle
        self.sample_cycle_length = sample_cycle_length
        # Amount of time between each sample
        self.sample_interval = sample_interval
        # Speed the robot moves at
        self.speed = speed
        # Range of broadcast messages
        self.communication_range = communication_range
        # How often the environment updates
        self.env_interval = env_interval
        # Size of grid
        self.grid_size = grid_size
        # Current position of Robot
        if position == None:
            self.position = random.uniform(0, grid_size[0]), random.uniform(0, grid_size[1])
        else:
            self.position = position

        # The colour the robot is looking for
        self.sample_colour = sample_colour
        # Number of occurences in sample of sample_colour
        self.sample_colour_occurences = 0
        # Is there self-evidence to be considered in the opinion update routine, non-zero if there is: int representing colour
        self.sample_evidence = 0
        # Stores the self-evidence concentration estimate
        self.self_evidence_estimate = 0
        # How many samples have been taken in the current sample
        self.sample_count = 0

        # Current state of Robot: Uncommitted, colour 1, colour 2, etc.
        self.decision_state = decision_state
        # Current estimation of concentration of colour Robot is committed to
        self.commited_estimation = commited_estimation
        # The last recieved message from a neighbour within the last update interval
        self.neighbour_message = None
        # Is Robot newly recruited
        self.new_recruit = False
        # Broadcast frequency
        self.broadcast_frequency = 2 * min(2 * commited_estimation, 1)
        # Destination for current path
        self.chosen_waypoint = None
        self.choose_random_waypoint()
        #print(f"New waypoint: {self.chosen_waypoint}")
        # Normalised direction vector to current waypoint 
        self.motion_vector = None
        self.get_motion_vector()
    
    def step_robot(self, env_grid, robots):
        """
        Function to be called at each update of the environment
        parameters:
          env_grid: (List[List : int]) The current grid of the environment
          robots: (List : Robot) List of all Robot's in the environment
        """
        self.motion_routine()
        if np.isclose(self.environment.time % self.sample_interval, 0):
            self.sampling_routine(env_grid)
        if self.broadcast_frequency != 0:
            if np.isclose(self.environment.time %  ((1 / self.broadcast_frequency) * 100), 0):
                self.broadcasting_routine(robots)
        if np.isclose(self.environment.time % self.update_interval, 0):
            self.opinion_update_routine()
            self.neighbour_message = None
        
    def choose_random_waypoint(self):
        """
        Choose a coordinate uniformly at random from the grid
        """
        self.chosen_waypoint = random.uniform(0, self.grid_size[0]), random.uniform(0, self.grid_size[1])
    
    def get_motion_vector(self):
        """
        Given a waypoint, find the normalised direction vector to that point from the Robot's position.
        params:
          waypoint: (Tuple : float) x, y 
        """
        x = self.chosen_waypoint[0] - self.position[0]
        y = self.chosen_waypoint[1] - self.position[1]
        magnitude = math.sqrt(x**2 + y**2)
        self.motion_vector =  x / magnitude, y / magnitude

    def motion_routine(self):
        """
        Handle motion of Robot. Move towards current waypoint at each timestep.
        Pick new waypoint if destination reached.
        """
        distance_to_waypoint = np.sqrt(np.square(self.chosen_waypoint[0] - self.position[0]) + np.square(self.chosen_waypoint[1] - self.position[1]))
        step_size = self.env_interval * self.speed
        if distance_to_waypoint < step_size:
            if np.isclose(distance_to_waypoint, 0):
                # Pick new waypoint
                self.choose_random_waypoint()
                #print(f"New waypoint: {self.chosen_waypoint}")
                self.get_motion_vector()
            else:
                self.update_position(self.motion_vector[0] * distance_to_waypoint, self.motion_vector[1] * distance_to_waypoint)
        else:
            self.update_position(self.motion_vector[0] * step_size, self.motion_vector[1] * step_size)

    def update_position(self, x, y):
        """
        Move the robot.
        params:
          x: (float) x direction vector
          y: (float) y direction vector
        """
        self.position = self.position[0] + x, self.position[1] + y
    
    def opinion_update_routine(self):
        """
        Given self-sourced and/or social evidence, decide what opinion the robot should have. 
        """
        if self.sample_evidence and self.neighbour_message != None:
            # Randomly choose between self-source and social evidence
            if random.uniform(0,1) > 0.5:
                # Use self-sourced evidence
                # Discovery transition:
                self.decision_state = self.sample_evidence
                self.commited_estimation = self.self_evidence_estimate
                self.broadcast_frequency = 2 * min(2 * self.commited_estimation, 1)
                #print(f"{self.id}: Discovery transition")
                # Reset sample evidence
                self.sample_evidence = 0
                self.sample_colour = None
            else:
                # Use social evidence
                if self.decision_state != 0:
                    if self.neighbour_message != self.decision_state:
                        # Cross-inhibition transition
                        self.decision_state = 0
                        #print(f"{self.id}: Cross-inhibition transition")
                        # Reset sample evidence
                        self.sample_evidence = 0
                        self.sample_colour = None
                else:
                    # Recruitment transition
                    self.decision_state = self.neighbour_message
                    self.commited_estimation = 0
                    #print(f"{self.id}: Recruitment transition")
                    # Reset sample evidence
                    self.sample_count = 0
                    self.sample_colour_occurences = 0
                    self.commited_estimation = 0
                self.broadcast_frequency = 2 * min(2 * self.commited_estimation, 1)
        elif self.sample_evidence:
            # Discovery transition:
            #print(f"{self.id}: Discovery transition")
            self.decision_state = self.sample_evidence
            self.commited_estimation = self.self_evidence_estimate
            self.broadcast_frequency = 2 * min(2 * self.commited_estimation, 1)
            # Reset sample evidence
            self.sample_evidence = 0
            self.sample_colour = None
        elif self.neighbour_message != None:
            # Use social evidence
            if self.decision_state != 0:
                if self.neighbour_message != self.decision_state:
                    # Cross-inhibition transition
                    self.decision_state = 0
                    self.commited_estimation = 0
                    #print(f"{self.id}: Cross-inhibition transition")
                    self.sample_colour = None
            else:
                # Recruitment transition
                self.new_recruit = True
                self.decision_state = self.neighbour_message
                self.sample_colour = self.decision_state
                #print(f"{self.id}: Recruitment transition")
                self.sample_count = 0
                self.sample_colour_occurences = 0
                self.commited_estimation = 0
                self.broadcast_frequency = 2 * min(2 * self.commited_estimation, 1)
        
    def sampling_routine(self, env_grid):
        """
        The sample routine to be called every after every sample_interval length of time.
        parameters:
          env_grid: (List[List : int]) The current grid of the environment
        """
        if self.sample_colour == None:
            # Choose to sample colour of square at current location
            col, row = self.get_square_robot_is_over()
            self.sample_colour = env_grid[row][col]
            self.sample_count = 0
            self.sample_colour_occurences = 0
            #print(f"New sample colour: {self.sample_colour}")
        else:
            if self.sample_count < self.sample_cycle_length:
                if self.is_robot_over_sample_colour(env_grid):
                    self.sample_colour_occurences += 1
                self.sample_count += 1
                if self.new_recruit:
                    self.broadcast_frequency = 2 * min(2 * self.sample_colour_occurences / self.sample_cycle_length, 1)
            else:
                sample_colour_concentration = self.sample_colour_occurences / self.sample_count
                if sample_colour_concentration > 1:
                    print(f"ERROR: {sample_colour_concentration}, {self.sample_colour_occurences}, {self.sample_count}")
                if self.sample_colour == self.decision_state and self.decision_state != 0:
                    self.commited_estimation = sample_colour_concentration
                    self.broadcast_frequency = 2 * min(2 * self.commited_estimation, 1)
                elif sample_colour_concentration > self.commited_estimation or self.decision_state == 0:
                    # Store colour and concentration estimate of sample for update decision
                    self.sample_evidence = self.sample_colour
                    self.self_evidence_estimate = sample_colour_concentration
                    #print(f"end of sample: {self.sample_evidence}, {self.self_evidence_estimate}")
                # End sample cycle
                self.new_recruit = False
                self.sample_colour = None
                self.sample_colour_occurences = 0
                self.sample_count = 0
            
    def broadcasting_routine(self, robots):
        """
        Sends signals to neighbours of opinion. To be called after broadcast_interval amount of time.
        params:
          robots: (List : Robot)
        """
        if self.decision_state != 0:
            for neighbour_index in self.find_all_neighbours(robots):
                robots[neighbour_index].neighbour_message = self.decision_state

    def find_all_neighbours(self, robots):
        neighbour_indices = []
        for i, robot in enumerate(robots):
            if self.get_distance_to_point(robot.position) < self.communication_range:
                if i == self.id:
                    continue
                else:
                    neighbour_indices.append(i)
        return neighbour_indices


    def get_distance_to_point(self, point):
        """
        Get the distance from the Robot's current position to a point
        params:
          point: (Tuple : float)
        """
        return np.sqrt(np.square(self.position[0] - point[0]) + np.square(self.position[1] - point[1]))


    def is_robot_over_sample_colour(self, env_grid):
        """
        Return whether the sample_colour is present at the current square
        parameters:
          env_grid: (List[List : int]) The current grid of the environment
        return: (bool) True if the sample_colour is present, False otherwise
        """
        col, row = self.get_square_robot_is_over()
        return env_grid[row][col] == self.sample_colour
    
    def get_square_robot_is_over(self):
        """
        Given the Robot's current position, get the row and col index of the square it is currently on.
        """
        return math.floor(self.position[0]), math.floor(self.position[1])
