import pandas as pd
import time
import multiprocessing
from joblib import Parallel, delayed, parallel_backend
from prepare_monte_carlo_inputs import monteCarloInputs, baselineInputs

# =====================
# Simple model to demonstrate
# =====================

def simple_model(a=1.0, b=2.0, c=3.0, d=4.0):

    x = a + b / c + d
    y = a + b -2* c - d

    return x, y


# =====================
# Wrapper function - goal is to return inputs, constants and outputs as a single series for easy data analysis
# =====================

def model_wrapper(inputs, constants):

    # Track run time
    t0 = time.time()

    # Run simulation (This is where an external function could be called)
    x, y = simple_model(a=inputs['a'], b=inputs['b'], c=inputs['c'], d=constants['d'])

    # Pack results in Series
    outputs = pd.Series(index=['x', 'y'])
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
    studyName = "results_monte_carlo_xls"

    # Monte Carlo Inputs
    xls_filename = "inputs_monte_carlo.xlsx"
    sheetnames = ["case1","case2","case3","case4"]
    iterations = 100

    # Constants
    constants = pd.Series(index=['d'])
    constants['d'] = 10.0

    # ==============
    # Run Simulations
    # ==============
    all_outputs = []

    # Number of cores to use
    num_cores = multiprocessing.cpu_count() - 1  # Save one for other processes

    # Iterate each Monte Carlo case
    for sheetname in sheetnames:

        inputs = monteCarloInputs(xls_filename, sheetname, iterations)

        # Perform Simulations (Run all plant variations in parallel)
        with parallel_backend('multiprocessing', n_jobs=num_cores):
            output = Parallel(verbose=10)(
                delayed(model_wrapper)(inputs.loc[index], constants) for index in range(iterations))

        # Add output to all_outputs
        all_outputs = all_outputs + output

    # Combine outputs into single dataframe and save
    df = pd.DataFrame(all_outputs)
    df.to_csv(studyName + '.csv')

