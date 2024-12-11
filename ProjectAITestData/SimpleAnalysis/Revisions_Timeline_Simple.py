import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_histograms_by_country(base_folder):
    # Loop through each country folder
    for country in os.listdir(base_folder):
        country_path = os.path.join(base_folder, country)
        if not os.path.isdir(country_path):
            continue  # Skip files, only process directories
        
        revision_data = []
        politicians = []
        
        # Read data for all politicians in the country
        for csv_file in os.listdir(country_path):
            if csv_file.endswith(".csv"):
                file_path = os.path.join(country_path, csv_file)
                politician_name = os.path.splitext(csv_file)[0]
                df = pd.read_csv(file_path)
                df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date is datetime
                df['Politician'] = politician_name  # Add a column for politician name
                revision_data.append(df)
                politicians.append(politician_name)
        
        if not revision_data:
            print(f"No revision data found for {country}. Skipping.")
            continue
        
        # Combine all data for the country
        combined_data = pd.concat(revision_data)
        
        # Plot histogram or timeline
        plt.figure(figsize=(12, 6))
        for politician in politicians:
            politician_data = combined_data[combined_data['Politician'] == politician]
            plt.hist(
                politician_data['Date'], bins=30, alpha=0.7, label=politician
            )  # Change to plt.plot() for a timeline
        
        plt.title(f"Revisions Timeline for Politicians in {country}")
        plt.xlabel("Date")
        plt.ylabel("Number of Revisions")
        plt.legend()
        plt.tight_layout()
        
        # Save the plot
        plot_path = os.path.join(country_path, f"{country}_revisions_histogram.png")
        plt.savefig(plot_path)
        print(f"Saved histogram for {country} at {plot_path}")
        plt.close()

if __name__ == "__main__":
    base_folder = os.getcwd()  # Current directory
    plot_histograms_by_country(base_folder)