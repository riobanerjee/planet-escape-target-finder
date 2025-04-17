## Code Under Construction

This project retrieves data from the NASA Exoplanet Archive using TAP to filter planets based on specific conditions. It then uses **photoevolver** to calculate escape rates, identifying planets capable of retaining atmospheres above a given threshold.

### Setup Instructions

1. Create a new environment.
2. Install dependencies, including **photoevolver** and **Mors**.

### Running Instructions

Navigate to the top-level folder and execute the following commands:

1. `python -m src.data.collect`  
    Collects data from the NASA Exoplanet Archive.

2. `python -m src.planet.find_survivors`  
    Identifies planets that meet the atmospheric retention criteria.

3. `python -m src.visualize.plot_mr`  
    Generates visualizations for mass-radius relationships.

### Notes

- Ensure all dependencies are installed before running the commands.
- Refer to the documentation for additional details on configuration and usage.