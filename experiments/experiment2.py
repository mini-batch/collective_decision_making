import multiprocessing
import experiment_objects.Environment as e
import experiment_objects.Robot as r

# Env
X_SQUARES = 20
Y_SQUARES = 40
GRID_SIZE = [X_SQUARES, Y_SQUARES]
COLOUR_PROB = [0.2, 0.8]
ENV_INTERVAL = 1
NUM_STEPS = 100000
GRADUAL_CHANGE = [0.2, 36000]

# Robots
UPDATE_INTERVAL = 200
#SAMPLE_CYCLE_LENGTH = 15
SAMPLE_INTERVAL = 400
SPEED = 0.002
#COMMUNICATION_RANGE = 2
POSITION = None
SAMPLE_COLOUR = None
DECISION_STATE = 2
COMMITED_ESTIMATION = 0.8

NUM_ROBOTS = 50
#ROBOT_PARAMS = [UPDATE_INTERVAL, SAMPLE_CYCLE_LENGTH, SAMPLE_INTERVAL, SPEED, COMMUNICATION_RANGE, ENV_INTERVAL, GRID_SIZE, SAMPLE_COLOUR, DECISION_STATE, COMMITED_ESTIMATION, POSITION]

def run_repeat_simulation(num_runs, sample_len):
    ROBOT_PARAMS = [UPDATE_INTERVAL, sample_len, SAMPLE_INTERVAL, SPEED, 0, ENV_INTERVAL, GRID_SIZE, SAMPLE_COLOUR, DECISION_STATE, COMMITED_ESTIMATION, POSITION]
    env_params = [[X_SQUARES,Y_SQUARES], COLOUR_PROB, NUM_ROBOTS, ROBOT_PARAMS, ENV_INTERVAL, NUM_STEPS, GRADUAL_CHANGE]
    pool_arguments = [env_params for i in range(num_runs)]
    with multiprocessing.Pool() as pool:
        sim_stats = pool.starmap(run_test, pool_arguments)
    return sim_stats

def run_test(*env_params):
    env = e.Environment(*env_params)
    adapted = env.run()
    if env.adaptation_time == None:
        adapt_time = -1
    else:
        adapt_time = env.adaptation_time
    return [adapted, adapt_time, env.state_history, env.time_history, env.grid_colour_hist]