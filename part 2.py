import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations, combinations_with_replacement


class RaceSimulator:
    """
    Simulates an F1 race strategy by calculating the time added
    from tire degradation and pit stops.
    """

    def __init__(self):
        """
        Initialize the simulator and store tire data.
        """
        pass


    def tire_time(self, age, Tmin, Tmax, alpha, beta):
        """
        Calculate the time added due to tire degradation.

        Parameters:
            age: Tire age in laps.
            Tmin: Minimum time added by the tire.
            Tmax: Maximum time added by the tire.
            alpha: Tire degradation rate parameter.
            beta: Tire degradation midpoint parameter.

        Returns:
            Tire time added for the given tire age.
        """
        pass


    def simulate(self, stint_lengths, tire_types):
        """
        Simulate a complete race strategy.

        Parameters:
            stint_lengths: Length of each race stint.
            tire_types: Tire compound used for each stint.

        Returns:
            Total time added from tire degradation and pit stops.
        """
        pass


def plot_tires(simulator):
    """
    Plot tire degradation curves for all tire compounds.

    Parameters:
        simulator: A RaceSimulator object containing tire data.

    Returns:
        None.
    """
    ages = np.arange(0, 61)
    plt.figure(figsize=(10, 6))

    for name, p in simulator.tire_data.items():
        times = [simulator.tire_time(a, p["Tmin"], p["Tmax"], p["alpha"], p["beta"])
                 for a in ages]
        plt.plot(ages, times, label=name, linewidth=2)

    plt.xlabel("Tire Age (laps)")
    plt.ylabel("Time Added (s)")
    plt.title("Tire Degradation Curves")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    pass


def find_best_strategy(simulator):
    """
    Test all valid race strategies and find the one
    with the minimum total time added.

    Parameters:
        simulator: A RaceSimulator object.

    Returns:
        The strategy with the lowest total tire and pit time.
    """
    compounds = list(simulator.tire_data.keys())
    best_time = float("inf")
    best_strategy = None

    
    for n_stints in (2, 3):
        
        for tire_combo in combinations_with_replacement(compounds, n_stints):
            
            if len(set(tire_combo)) < 2:
                continue

            
            if n_stints == 2:
                for s1 in range(5, simulator.race_laps - 4):
                    stints = [s1, simulator.race_laps - s1]
                    t = simulator.simulate(stints, list(tire_combo))
                    if t < best_time:
                        best_time = t
                        best_strategy = (stints, list(tire_combo), t)

            else:  # 3 stints
                for s1 in range(5, simulator.race_laps - 9):
                    for s2 in range(5, simulator.race_laps - s1 - 4):
                        s3 = simulator.race_laps - s1 - s2
                        if s3 < 5:
                            continue
                        stints = [s1, s2, s3]
                        t = simulator.simulate(stints, list(tire_combo))
                        if t < best_time:
                            best_time = t
                            best_strategy = (stints, list(tire_combo), t)

    return best_strategy
    pass