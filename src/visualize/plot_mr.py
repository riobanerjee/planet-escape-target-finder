import pandas as pd
import seaborn as sns
import glob
import matplotlib.pyplot as plt

def read_csv(file_path):
    """
    Reads a CSV file and returns a pandas DataFrame.

    Parameters:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the CSV data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def plot_mass_radius(data):
    """
    Plots exoplanets on a mass-radius space using seaborn.
    The color and size of the points represent the fraction of the envelope mass to core mass.
    Also plots interior models from txt files in the zeng_models directory.

    Parameters:
        data (pd.DataFrame): DataFrame containing the exoplanet data.

    Returns:
        None
    """

    plt.figure(figsize=(10, 8))
    data['fenv_plot'] = data['fenv'] * 100
    sns.scatterplot(data=data, x='pl_bmasse', y='pl_rade', hue='fenv_plot', size='fenv_plot', sizes=(50, 500), palette="viridis", alpha=0.7, legend=False)

    for i, row in data.iterrows():
        plt.text(row['pl_bmasse'], row['pl_rade'], row['pl_name'], fontsize=12, alpha=0.9)
        plt.text(row['pl_bmasse'], row['pl_rade']-0.01, f"{row['fenv_plot']:.2f}%", fontsize=10)


    # Read all txt files with mass and radius data
    txt_files = glob.glob("zeng_models/*.txt")
    for txt_file in txt_files:
        try:
            line_data = pd.read_csv(txt_file, sep="\s+", header=None, names=['mass', 'radius'])
            plt.plot(line_data['mass'], line_data['radius'], linestyle='-', linewidth=1.5, label=txt_file.split('/')[-1])
        except Exception as e:
            print(f"Could not process file {txt_file}: {e}")

    plt.legend(title="Lines", fontsize=8)

    plt.xlim(data['pl_bmasse'].min() * 0.9, data['pl_bmasse'].max() * 1.1)
    plt.ylim(data['pl_rade'].min() * 0.9, data['pl_rade'].max() * 1.1)
    plt.xlabel("Mass (Earth Masses)")
    plt.ylabel("Radius (Earth Radii)")
    plt.title("Exoplanets and fraction on ef envelope to core mass")
    plt.tight_layout()
    plt.savefig('figs/mass_radius_plot.png')

if __name__ == "__main__":
    # Path to the CSV file
    csv_file_path = "data/surviving/surviving_planets.csv"

    # Read the CSV file
    exoplanet_data = read_csv(csv_file_path)

    # Plot the mass-radius space
    plot_mass_radius(exoplanet_data)