import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class RaceSimulator:
    """
    Simulates an F1 race strategy by calculating the time added
    from tire degradation and pit stops.
    """

    # Create the tire data Pandas DataFrame

    def __init__(self):

        self.race_laps = 60

        self.tire_data = pd.DataFrame({
            "Tmin": [0, 1, 2],
            "Tmax": [10, 10, 10],
            "alpha": [1/2, 1/4, 1/16],
            "beta": [15, 25, 55]
        }, index = ["Soft", "Medium", "Hard"])





    def tire_time(self, age, Tmin, Tmax, alpha, beta):

        # Calculate Tire Degradation

        tire_time_added = Tmin + (
            (Tmax - Tmin) /
            (1 + np.exp(-alpha*(age - beta)))
        )

        return tire_time_added




    def simulate(self, stint_lengths, tire_types):
        """
        Simulate a 60-lap race using three stints and two pit stops.

        Parameters:
            stint_lengths: List of three positive integer stint lengths.
            tire_types: List of three tire compounds.

        Returns:
            Total additional race time from tire degradation
            and pit stops.
        """

        # Validate the number of stints
        if len(stint_lengths) != 3:
            raise ValueError("A race must have exactly 3 stints.")

        # Validate the number of tire choices
        if len(tire_types) != 3:
            raise ValueError("Exactly 3 tire choices are required.")

        # Validate stint lengths
        for length in stint_lengths:
            if isinstance(length, (bool, np.bool_)) or not isinstance(
                length, (int, np.integer)
            ):
                raise TypeError("Stint lengths must be integers.")

            if length <= 0:
                raise ValueError("Stint lengths must be positive.")

        # Validate total race distance
        if sum(stint_lengths) != self.race_laps:
            raise ValueError("Stint lengths must add up to 60 laps.")

        # Validate tire names
        for tire_type in tire_types:
            if tire_type not in self.tire_data.index:
                raise ValueError(f"Invalid tire type: {tire_type}")

        # Validate tire compound variety
        if len(set(tire_types)) < 2:
            raise ValueError("At least 2 different tire compounds are required.")

        # Create a DataFrame for each stint
        stint_dataframes = []

        for stint_length, tire_type in zip(stint_lengths, tire_types):

            # Retrieve tire parameters
            Tmin = self.tire_data.loc[tire_type, "Tmin"]
            Tmax = self.tire_data.loc[tire_type, "Tmax"]
            alpha = self.tire_data.loc[tire_type, "alpha"]
            beta = self.tire_data.loc[tire_type, "beta"]

            # Generate tire ages
            ages = np.arange(stint_length)

            # Calculate tire degradation
            tire_time_added = self.tire_time(
                ages, Tmin, Tmax, alpha, beta
            )

            # Create the stint DataFrame
            stint_df = pd.DataFrame({
                "tire_type": tire_type,
                "tire_age": ages,
                "tire_time_added": tire_time_added
            })

            stint_dataframes.append(stint_df)

        # Combine the three stint DataFrames
        self.race_df = pd.concat(stint_dataframes, ignore_index=True)

        # Calculate total tire degradation and pit-stop time
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


    ages = np.arange(0, 61)
    plt.figure(figsize=(10, 6))

    for tire_name in simulator.tire_data.index:

        # Retrieve the parameters for the current tire

        Tmin = simulator.tire_data.loc[tire_name, "Tmin"]
        Tmax = simulator.tire_data.loc[tire_name, "Tmax"]
        alpha = simulator.tire_data.loc[tire_name, "alpha"]
        beta = simulator.tire_data.loc[tire_name, "beta"]

        # Calculate the degradation across all tire ages

        times = simulator.tire_time(
            ages, Tmin, Tmax, alpha, beta
        )

        # Plot the degradation curve

        plt.plot(ages, times, label = tire_name, linewidth = 2)

    plt.xlabel("Tire Age (laps)")
    plt.ylabel("Time Added (s)")
    plt.title("Tire Degradation Curves")
    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.tight_layout()
    plt.show()

def find_best_strategy(simulator):
    """
    Test all valid three-stint race strategies and find the one
    with the minimum total tire degradation and pit-stop time.

    Parameters:
        simulator: A RaceSimulator object.

    Returns:
        A tuple containing:
        - The three stint lengths.
        - The three tire compounds.
        - The minimum total additional race time.
    """

    compounds = list(simulator.tire_data.index)

    best_time = float("inf")
    best_strategy = None

    # Precalculate cumulative tire degradation for each compound
    tire_costs = {}

    for tire_name in compounds:

        Tmin = simulator.tire_data.loc[tire_name, "Tmin"]
        Tmax = simulator.tire_data.loc[tire_name, "Tmax"]
        alpha = simulator.tire_data.loc[tire_name, "alpha"]
        beta = simulator.tire_data.loc[tire_name, "beta"]

        ages = np.arange(simulator.race_laps)

        degradation = simulator.tire_time(
            ages, Tmin, Tmax, alpha, beta
        )

        # Store cumulative degradation for each possible stint length
        tire_costs[tire_name] = np.cumsum(degradation)

    # Try every possible ordered combination of three tire compounds
    for tire1 in compounds:
        for tire2 in compounds:
            for tire3 in compounds:

                tire_types = [tire1, tire2, tire3]

                # Require at least two different compounds
                if len(set(tire_types)) < 2:
                    continue

                # Try every valid combination of three stint lengths
                for stint1 in range(1, simulator.race_laps - 1):

                    for stint2 in range(
                        1, simulator.race_laps - stint1
                    ):

                        stint3 = (
                            simulator.race_laps - stint1 - stint2
                        )

                        # Calculate total tire degradation directly
                        total_tire_time = (
                            tire_costs[tire1][stint1 - 1]
                            + tire_costs[tire2][stint2 - 1]
                            + tire_costs[tire3][stint3 - 1]
                        )

                        # Add the two pit-stop penalties
                        total_time = total_tire_time + 50

                        # Update the best strategy
                        if total_time < best_time:

                            best_time = total_time

                            best_strategy = (
                                [stint1, stint2, stint3],
                                tire_types.copy(),
                                total_time
                            )

    # Generate the DataFrame for the winning strategy
    if best_strategy is not None:

        simulator.simulate(
            best_strategy[0],
            best_strategy[1]
        )

    return best_strategy
