import multiprocessing
import experiment_objects.Environment as e
import experiment_objects.Robot as r

# Env
X_SQUARES = 20
Y_SQUARES = 40
GRID_SIZE = [X_SQUARES, Y_SQUARES]
COLOUR_PROB = [0.9, 0.1]
ENV_INTERVAL = 1
NUM_STEPS = 100000

# Robots
UPDATE_INTERVAL = 200
SAMPLE_CYCLE_LENGTH = 15
SAMPLE_INTERVAL = 400
SPEED = 0.01
COMMUNICATION_RANGE = 2
POSITION = None
SAMPLE_COLOUR = None
DECISION_STATE = 2
COMMITED_ESTIMATION = 0.8

NUM_ROBOTS = 50
ROBOT_PARAMS = [UPDATE_INTERVAL, SAMPLE_CYCLE_LENGTH, SAMPLE_INTERVAL, SPEED, COMMUNICATION_RANGE, ENV_INTERVAL, GRID_SIZE, SAMPLE_COLOUR, DECISION_STATE, COMMITED_ESTIMATION, POSITION]

def run_repeat_simulation(num_runs):
    env_params = [[X_SQUARES,Y_SQUARES], COLOUR_PROB, NUM_ROBOTS, ROBOT_PARAMS, ENV_INTERVAL, NUM_STEPS]
    pool_arguments = [env_params for i in range(num_runs)]
    with multiprocessing.Pool() as pool:
        sim_stats = pool.starmap(run_test, pool_arguments)
    return sim_stats

def run_test(*env_params):
    env = e.Environment(*env_params)
    adapted = env.run()
    return [adapted, env.adaptation_time]