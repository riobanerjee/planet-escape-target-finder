import requests
import pandas as pd
from io import StringIO
import os

def get_tap_service_url():
    """
    Returns the base URL for the NASA Exoplanet TAP service.
    """
    return "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

def build_query():
    """
    Constructs the SQL query to retrieve the `pscomppars` table.
    Only exoplanets with a radius less than or equal to 1.8 and measured mass, 
    stellar age > 100Myr and stellar mass > 0.1 MSun and stellar temp < 5000K are included.
    The query selects the following columns:
    - `hostname`: The name of the host star.
    - `st_spectype`: The spectral type of the host star.
    - `st_teff`: The effective temperature of the host star.
    - `st_mass`: The mass of the host star.
    - `st_rad`: The radius of the host star.
    - `st_age`: The age of the host star.
    - `pl_name`: The name of the planet.
    - `pl_rade`: The radius of the planet.
    - `pl_bmasse`: The mass of the planet.
    - `pl_orbper`: The orbital period of the planet.
    
    Returns:
        str: The SQL query string.
    """
    return "SELECT hostname,st_spectype,st_teff,st_mass,st_rad,st_age," +\
                    "pl_name,pl_rade,pl_bmasse,pl_orbper" +\
            " FROM pscomppars" +\
            " WHERE pl_rade<=1.8 AND rv_flag=1 AND tran_flag=1 AND st_age>0.1 AND st_mass>0.1 AND st_teff<5000"

def fetch_pscomppars_table():
    """
    Fetches the `pscomppars` table from the NASA Exoplanet TAP API.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the `pscomppars` table data.
    """
    url = get_tap_service_url()
    query = build_query()
    params = {
        "query": query,
        "format": "csv"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an error for bad HTTP responses

    # Convert the CSV response to a pandas DataFrame
    csv_data = StringIO(response.text)
    return pd.read_csv(csv_data)

def save_table_to_csv(dataframe, output_path):
    """
    Saves a pandas DataFrame to a CSV file.

    Args:
        dataframe (pd.DataFrame): The DataFrame to save.
        output_path (str): The file path where the CSV will be saved.
    """
    dataframe.to_csv(output_path, index=False)
    print(f"Table saved to {output_path}")

def main():
    """
    Main function to retrieve the `pscomppars` table and save it to a CSV file.
    """
    print("Fetching the `pscomppars` table from the NASA Exoplanet TAP API...")
    pscomppars_table = fetch_pscomppars_table()
    print("Table fetched successfully!")
    print(f"Number of rows: {len(pscomppars_table)}")
    
    # Create data directory if it doesn't exist
    os.makedirs("data/raw", exist_ok=True)

    output_path = "data/raw/pscomppars.csv"
    save_table_to_csv(pscomppars_table, output_path)

if __name__ == "__main__":
    main()