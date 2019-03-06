import pandas as pd
import time
import numpy as np
import multiprocessing
from joblib import Parallel, delayed, parallel_backend

# =====================
# Simple model to demonstrate
# =====================

def simple_model(a=1.0, b=2.0, c=3.0, d=4.0):

    x = a**b/c+d
    y = a+b**c-d

    return x,y

# =====================
# Wrapper function - goal is to return inputs, constants and outputs as a single series for easy data analysis
# =====================

def model_wrapper(inputs, constants):

    # Track run time
    t0 = time.time()

    # Run simulation (This is where an external function could be called)
    x, y = simple_model(a=inputs['a'],b=inputs['b'],c=inputs['c'],d=constants['d'])

    # Pack results in Series
    outputs = pd.Series(index=['x','y'])
    outputs['x'] = x
    outputs['y'] = y

    # Display Elapsed Time
    t1 = time.time()
    print "Time Elapsed: " + str(round(t1 - t0, 2)) + " s"

    # Combine inputs and results into output and then return
    combined = pd.concat([inputs, constants, outputs], axis=0)
    return combined

# =====================
# Main Program
# =====================
if __name__ == '__main__':

    # ==============
    # User Inputs
    # ==============
    studyName = "results_monte_carlo_simple"

    iterations = 1000

    # Constants
    constants = pd.Series(index=['d'])
    constants['d'] = 10.0

    # Stochastic variables with low and high values
    a = [1E3, 2.5E4]  # m3
    b = [1.1, 4.9]  # bar
    c = [5, 100]  # bar

    # ==============
    # Prepare Monte Carlo Distributions
    # For more distributions, see https://docs.scipy.org/doc/numpy/reference/routines.random.html
    # ==============
    inputs = pd.DataFrame(index=range(iterations), columns=['a', 'b', 'c'])
    inputs.loc[:, 'a'] = np.random.uniform(low=a[0], high=a[1], size=iterations)
    inputs.loc[:, 'b'] = np.random.uniform(low=b[0], high=b[1], size=iterations)
    inputs.loc[:, 'c'] = np.random.uniform(low=c[0], high=c[1], size=iterations)

    # ==============
    # Run Simulations
    # ==============

    # Number of cores to use
    num_cores = multiprocessing.cpu_count() - 1  #  Save one for other processes

    # Perform Simulations (Run all plant variations in parallel)
    with parallel_backend('multiprocessing', n_jobs=num_cores):
        output = Parallel(verbose=10)(delayed(model_wrapper)(inputs.loc[index], constants) for index in range(iterations))

    # Combine outputs into single dataframe and save
    df = pd.concat(output, axis=1)
    df = df.transpose()
    df.to_csv(studyName + '.csv')
