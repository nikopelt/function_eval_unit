import matplotlib.pyplot as plt
import numpy as np
from random import randint
from random import random
from copy import deepcopy

"""
    Simulated Annealing Script to calculate the lowest energy point mapping to a specific range to divide it in a 
    specific number of segments.
"""


def fun(x):
    return 1/(1 + np.exp(-x))

# Plot np.array type points in the function graph
def plot(res_points, start_points, start, end):
    
    fig, axs = plt.subplots(2)
    fig.suptitle('Simulated Annealing Optimization')
    space = np.linspace(start,end,100)
    axs[0].set_title("Segments of equal width")
    axs[0].plot(space, fun(space),'b--', start_points, fun(start_points), 'r--', start_points, fun(start_points), 'r.',ms = 12)
    
    axs[1].set_title("Segments after simulated annealing optimization")
    axs[1].plot(space, fun(space),'b--', res_points, fun(res_points), 'r--', res_points, fun(res_points), 'r.',ms = 12)
    print("Final points: " + str(res_points))
    plt.show()



class points:

    """
        Class of points for linear interpolation used in pwl approximation of a function

    """
    def __init__(self, start, end, num_points, diff):
        self.start = start
        self.end = end
        self.diff = diff
        self.num_points = num_points
        init_width = abs(end-start)/num_points
        init_points = []

        for i in range(num_points + 1):
            init_points.append(start + init_width*i)
        
        self.points = np.array(init_points)

    def next(self, point):
        rand = randint(0,1000)
        if rand % 2:
            if self.points[point] + 2*self.diff < self.points[point + 1]: 
                self.points[point] = self.points[point] + self.diff
        else:
            if self.points[point] - 2*self.diff > self.points[point - 1]: 
                self.points[point] = self.points[point] - self.diff
        return self.points
    
    def set_points(self, new_points):
        self.points = np.copy(new_points)
   
   # MSE of the points
    def E(self):

        err = 0
        

        for i in range(1, self.num_points + 1):
            p = (self.points[i] + self.points[i - 1])/2
            err += (self.points[i] - self.points[i-1])*(fun(p) - (fun(self.points[i - 1]) + fun(self.points[i]))/2 )**2

        err = err/self.num_points

        return err
    def E_abs(self):
        err = 0
        
        for i in range(1, self.num_points):
            x = np.linspace(self.points[i-1], self.points[i], 50)
        
            slope = (fun(self.points[i]) - fun(self.points[i-1])) / (self.points[i] - self.points[i-1])
        
            y_true = fun(x)
            y_approx = fun(self.points[i-1]) + slope * (x - self.points[i-1])
        
            segment_max_err = (np.max(np.abs(y_true - y_approx)))**2
        
            if segment_max_err > err:
                err = segment_max_err
            
        return err

def P(old, new, temp):
    if new < old:
        return 1.0
    return np.exp((old-new)/temp)

def sim_anneal(T, T_min, points, best, next_state):
    N = points.num_points - 1 
    cursor = 0;

    while T > T_min:
        next_state.set_points(points.points)
        
        next_state.next((cursor % N) + 1)

        if best.E() > points.E():
            best.set_points(points.points)
        
        if P(points.E(), next_state.E(), T) >= random():
            points.set_points(next_state.points)

        cursor = cursor + 1
        T = T*0.9995

    points.set_points(best.points)


def sim_anneal_abs(T, T_min, points, best, next_state):
    N = points.num_points - 1 
    cursor = 0;

    while T > T_min:
        next_state.set_points(points.points)
        
        next_state.next((cursor % N) + 1)

        if best.E_abs() > points.E_abs():
            best.set_points(points.points)
        
        if P(points.E_abs(), next_state.E_abs(), T) >= random():
            points.set_points(next_state.points)

        cursor = cursor + 1
        T = T*0.9995

    points.set_points(best.points)

def main():
    START = int(input("Enter the START point: "))
    END = int(input("Enter the END point: "))
    DIFF = float(input("Enter the step: "))
    SEGMENTS = int(input("Enter the number of SEGMENTS: "))
    mode = int(input("Enter the Energy function configuration (0:Absolute Error, 1:MSE): "))
    TEMP = 1
    T_MIN = 0.0000001


    p1 = points(start = START, end = END,num_points = SEGMENTS, diff = DIFF)
    b1 = points(start = START, end = END,num_points = SEGMENTS, diff = DIFF)
    n1 = points(start = START, end = END,num_points = SEGMENTS, diff = DIFF)

    p2 = points(start = START, end = END,num_points = SEGMENTS, diff = DIFF)
    print("Initial points: " + str(p1.points))
    E_old = p1.E_abs()

    if mode:
        sim_anneal(TEMP, T_MIN, p1, b1, n1)
    else:   
        sim_anneal_abs(TEMP, T_MIN, p1, b1, n1)

    plot(p1.points, p2.points, START, END)
    print("Relative energy optimization: " + str((E_old - p1.E_abs())/E_old))

        
    with open("points.txt","w") as f:
        for i in range(len(p1.points)):
            f.writelines(str(p1.points[i]) + "\n")


if __name__ == "__main__" :
    main()
