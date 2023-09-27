import pygame
import pandas as pd
from pygame.locals import *
import experiment_objects.Environment as e
import frontend.SceneManager as sm
import experiment_objects.Robot as r


X_SQUARES = 20 # (number of cols)
Y_SQUARES = 40 # (number of rows)
COLOUR_PROB = [0.8, 0.2]
ENV_INTERVAL = 1
GRID_SIZE = [X_SQUARES, Y_SQUARES]
EXPERIMENT_LENGTH = 100000
NUM_ROBOTS = 50

# Robot parameters
UPDATE_INTERVAL = 200
SAMPLE_CYCLE_LENGTH = 15
SAMPLE_INTERVAL = 400
SPEED = 0.002
COMMUNICATION_RANGE = 2
POSITION = None#[0,0]
SAMPLE_COLOUR = None
DECISION_STATE = 2
COMMITED_ESTIMATION = 0.8

SQUARE_SIZE = 1000 / max(X_SQUARES, Y_SQUARES)
WIN_WIDTH = X_SQUARES * SQUARE_SIZE
WIN_HEIGHT = Y_SQUARES * SQUARE_SIZE
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 0
FLAGS = 0


def visualise():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, DEPTH, FLAGS)
    pygame.display.set_caption("Experiment")
    timer = pygame.time.Clock()
    running = True

    ROBOT_PARAMS = [UPDATE_INTERVAL, SAMPLE_CYCLE_LENGTH, SAMPLE_INTERVAL, SPEED, COMMUNICATION_RANGE, ENV_INTERVAL, GRID_SIZE, SAMPLE_COLOUR, DECISION_STATE, COMMITED_ESTIMATION, POSITION]
    env = e.Environment([X_SQUARES,Y_SQUARES], COLOUR_PROB, NUM_ROBOTS, ROBOT_PARAMS, ENV_INTERVAL, EXPERIMENT_LENGTH, [0.5, 10000])
    manager = sm.SceneMananger(env)

    while running:
        timer.tick(60)

        if pygame.event.get(QUIT):
            running = False
            return
        
        manager.scene.handle_events(pygame.event.get())
        manager.scene.update()
        manager.scene.render(screen)
        pygame.display.flip()
    
    return 0


import experiments.experiment1 as e1
def experiment1():
    print(e1.run_repeat_simulation(30))

import experiments.experiment2 as e2

def experiment2():
    for c_range in [1,2,3,4,5,6,7,8,9,15,25,45]:#[0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 25, 45]: 
        results = e2.run_repeat_simulation(20, c_range)
        df = pd.DataFrame(results, columns=["adapted", "adaptation_time", "state_history", "time_history", "color_history"])
        df.to_csv(f"./results/exp2/sample_len/exp2_{c_range}.csv")

def main():
    env = e.Environment([X_SQUARES,Y_SQUARES], COLOUR_PROB, None, 1, 15000)
    env.run()
    return 0


if __name__=="__main__":
    #main()
    #experiment1()
    visualise()
