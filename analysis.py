import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast

sns.set_style("whitegrid")

def plot_adaptation_times():
    x = []
    y = []
    err = []
    for c in [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,25,45]:#[1,2,3,4,5,6,7,8,9,15,25,45]
        df = pd.read_csv(f'results/exp1/exp1_0.7/speed_0.002/exp1_{c}.csv')
        df["adapted"] = df["adapted"].astype(int)
        x.append(c)
        y.append(df["adaptation_time"].mean())
        err.append(df["adaptation_time"].std())

    fig, ax = plt.subplots()
    eb = ax.errorbar(range(len(x)), y, err, linestyle='None', marker='^')
    eb[-1][0].set_linestyle('--')
    ax.set(xlabel='Communication Range', ylabel='Average Adaptation Time')
    plt.xticks(range(len(x)), x)
    plt.show()

def plot_average_opinion(c):
    df = pd.read_csv(f'results/exp1/exp1_0.7/speed_0.002/exp1_{c}.csv')
    test = df["state_history"]
    test = np.array([np.array(ast.literal_eval(i)) for i in test], dtype=object)
    #col_history = df["color_history"].iloc[0]
    #col_history = np.array(ast.literal_eval(col_history))[:,0]
    max_length = 0
    for i in test:
        if i.shape[0] > max_length:
            max_length = i.shape[0]
    print(max_length)
    for ind, i in enumerate(test):
        print(i.shape)
        if len(i) < max_length:
            test[ind] = np.append(i, np.array([[0,50,0] for j in range(max_length - i.shape[0])]),0)
    #col_history = np.append(col_history, np.array([0.8 for j in range(max_length - col_history.shape[0])]),0)
    x = np.arange(0, max_length * 2, 2)
    y0 = (np.sum(test)[:,0] / 30) / 50
    y1 = (np.sum(test)[:,1] / 30) / 50
    y2 = (np.sum(test)[:,2] / 30) / 50
    #y3 = col_history
    fig, ax = plt.subplots()
    ax.plot(x, y0, label="Uncommitted", color="black")
    ax.plot(x, y1, label="Orange", color="sandybrown")
    ax.plot(x, y2, label="Blue", color="lightskyblue")
    #ax.plot(x, y3, label="Orange Square Proportion", color="sandybrown", linestyle="--")
    ax.legend()
    ax.set(xlabel='Time (seconds)', ylabel='Average state proportion')
    plt.show()

plot_average_opinion(0.5)
#plot_average_opinion(6.5)
plot_average_opinion(45)

plot_adaptation_times()
