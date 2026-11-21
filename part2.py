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

        self.tire_data = pd.DataFrame({
            "Tmin": [0, 1, 2],
            "Tmax": [10, 10, 10],
            "alpha": [1/2, 1/4, 1/16],
            "beta": [15, 25, 55]
        }, index = ["Soft", "Medium", "Hard"])

        

    def tire_time(self, age, Tmin, Tmax, alpha, beta):

        tire_time_added = Tmin + (
            (Tmax - Tmin) /
            (1 + np.exp(-alpha*(age - beta)))
        )

        return tire_time_added
        


    def simulate(self, stint_lengths, tire_types):

        # Create a DataFrame (Table) for each stint

        stint_dataframes = []  
        
        # Look up the tire parameters 

        for stint_length, tire_type in zip(stint_lengths, tire_types):
            Tmin = self.tire_data.loc[tire_type, "Tmin"]
            Tmax = self.tire_data.loc[tire_type, "Tmax"]
            alpha = self.tire_data.loc[tire_type, "alpha"]
            beta = self.tire_data.loc[tire_type, "beta"]

            # Create the tire ages 

            ages = np.arange(stint_length)
 
            # Calculate tire ages and degradation 

            tire_time_added = (self.tire_time(ages, Tmin, Tmax, alpha, beta))

            # Create a DataFrame for the stint 

            stint_df = pd.DataFrame({
                "tire_type": tire_type,
                "tire_age": ages, 
                "tire_time_added": tire_time_added
            })

            # Append the DataFrame to the list 

            stint_dataframes.append(stint_df)

        # Concatenate the three DataFrames
        self.race_df = pd.concat(stint_dataframes, ignore_index = True)

        total_additional_race_time = (
            self.race_df["tire_time_added"].sum() + 50
        )

        return total_additional_race_time
        
     


def plot_tires(simulator):
    """
    Plot tire degradation curves for all tire compounds.

    Parameters:
        simulator: A RaceSimulator object containing tire data.

    Returns:
        None.
    """
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
    pass