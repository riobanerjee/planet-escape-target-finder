import pandas as pd
import photoevolver as ph
import matplotlib.pyplot as plt
import Mors as mors
import os

def load_planetary_data(csv_path):
    """
    Load planetary data from a CSV file.

    Args:
        csv_path (str): Path to the CSV file containing planetary data.

    Returns:
        pd.DataFrame: DataFrame containing the planetary data.
    """
    df = pd.read_csv(csv_path)
    return df

def has_surviving_atmosphere(row, fenv_percent=0.01):
    """
    Determine if a planet has a surviving atmosphere using PhotoEvolver.

    Args:
        row (pd.Series): A row of planetary data.
        fenv_percent (float): The threshold for the envelope mass fraction to consider the atmosphere as surviving.
        Default is 0.01% (0.0001).

    Returns:
        bool: True if the planet's atmosphere survives, False otherwise.
    """
    try:
        # Extract necessary parameters from the row
        planet_mass = row['pl_bmasse']  # Planet mass in Jupiter masses
        planet_radius = row['pl_rade']  # Planet radius in Jupiter radii
        planet_period = row['pl_orbper']  # Orbital period in days
        star_age = row['st_age'] * 1000        # Star age in Myr
        star_mass = row['st_mass']      # Star mass in solar units

        # planet_mass = 5.0
        # planet_radius = 3.0
        # planet_period = 5.0
        # star_age = 100.0
        # star_mass = 1.0

        # Ensure all required parameters are present
        if pd.isna(planet_mass) or pd.isna(planet_radius) or pd.isna(star_age) or pd.isna(star_mass) or pd.isna(planet_period):
            return False, 0
        try:
            # initialize planet and star
            planet = ph.Planet(
            mass=float(planet_mass),
            radius=float(planet_radius),
            period=float(planet_period)
            )

            star = mors.Star(
            Mstar=float(star_mass),
            percentile=50.0
            )

            planet.set_models(
            core  = ph.models.core_otegi20,
            env   = ph.models.envelope_chen16,
            mloss = ph.models.massloss_energy_limited,
            star  = star
            )

            # Set up evolution
            structure = planet.solve_structure(age=float(star_age))
            fenv = structure.fenv
        except Exception as e:
            print(f"Error during planet and star initialization or evolution: {e}")
            return False, 0

        # evo_df = planet.evolve(start=100.0, end=1000.0, step=0.1, progressbar=True)

        # fig, (axr, axm) = plt.subplots(nrows = 2, dpi = 100, sharex = True)

        # axr.set_xscale('log')
        # axm.set_xlabel('Age [Myr]')
        # axr.set_ylabel(r'Planet radius [$R_{\oplus}$]')
        # axm.set_ylabel(r'Envelope mass fraction')

        # evo_df.plot('age', 'radius', ax = axr)
        # evo_df.plot('age', 'fenv', ax = axm)
        # plt.tight_layout()
        # plt.savefig(row['pl_name'] + '.png')

        # Check if the envelope mass fraction is below a 0.01% of core mass
        if fenv < fenv_percent/100.0:
            return False, 0
        else:
            return True, fenv


    except Exception as e:
        print(f"Error processing row: {e}")
        return False

def find_surviving_planets(data, fenv_percent=0.01):
    """
    Find planets with surviving atmospheres in the dataset.

    Args:
        data (pd.DataFrame): DataFrame containing planetary data.
        fenv_percent (float): The threshold for the envelope mass fraction to consider the atmosphere as surviving.
        Default is 0.01% (0.0001).

    Returns:
        pd.DataFrame: DataFrame containing planets with surviving atmospheres.
    """
    n_rows = len(data)
    surviving_planets = data.copy()
    # Add a new column for fenv
    surviving_planets['fenv'] = None
    for i, row in data.iterrows():
        # Print the current row number being processed
        print(f"Processing {i+1}/{n_rows} {row['pl_name']}")
        survivor, fenv = has_surviving_atmosphere(row, fenv_percent=0.01)
        
        # Update the fenv value in the DataFrame
        surviving_planets.at[i, 'fenv'] = fenv
        
        if survivor:
            print("Survives")
        else:
            print("Does not survive")
            surviving_planets.drop(i, inplace=True)
    print(f"Found {len(surviving_planets)} planets with surviving atmospheres.")
    print(f"Dropped {n_rows - len(surviving_planets)} planets.")
    return surviving_planets

def save_results(surviving_planets, output_path):
    """
    Save the results to a CSV file.

    Args:
        surviving_planets (pd.DataFrame): DataFrame containing planets with surviving atmospheres.
        output_path (str): Path to save the results CSV file.
    """
    surviving_planets.to_csv(output_path, index=False)
    print(f"Found {len(surviving_planets)} planets with surviving atmospheres. Results saved to {output_path}.")

def main():
    """
    Main function to find planets with surviving atmospheres.
    """
    # Paths to input and output files
    csv_path = 'data/raw/pscomppars.csv'

    os.makedirs("data/surviving", exist_ok=True)
    output_path = 'data/surviving/surviving_planets.csv'

    # Load planetary data
    data = load_planetary_data(csv_path)

    # # Find planets with surviving atmospheres
    fenv_percent = 0.01
    surviving_planets = find_surviving_planets(data, fenv_percent=fenv_percent)

    # Save the results
    save_results(surviving_planets, output_path)

if __name__ == "__main__":
    main()