import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Define election periods and their types for each country
ELECTION_PERIODS = {
    "Germany": {
        "Federal": ["2017-09-24", "2021-09-26"],
        "State": ["2018-10-14", "2022-10-09"]
    },
    "USA": {
        "Presidential": ["2016-11-08", "2020-11-03"],
        "Midterm": ["2018-11-06", "2022-11-08"]
    },
    "Nigeria": {
        "General": ["2015-03-28", "2019-02-23"],
        "Local": ["2018-08-11", "2022-08-11"]
    },
    "Austria": {
        "National": ["2017-10-15", "2019-09-29"],
        "Regional": ["2018-03-11", "2021-04-18"]
    },
    "Bosnia": {
        "Country": ["2018-10-07", "2022-10-02"],
        "Local": ["2020-11-15", "2024-11-15"]
    }
}

# Define colors for election types
ELECTION_COLORS = {
    "Federal": "orange",
    "State": "green",
    "Presidential": "red",
    "Midterm": "blue",
    "General": "purple",
    "Local": "brown",
    "National": "gold",
    "Regional": "pink",
    "Country": "red",
    "Local": "brown"
}

def plot_revisions_trends(base_folder):
    for country in os.listdir(base_folder):
        country_path = os.path.join(base_folder, country)
        if not os.path.isdir(country_path):
            continue  # Skip files, only process directories
        
        revision_data = []
        for csv_file in os.listdir(country_path):
            if csv_file.endswith(".csv"):
                file_path = os.path.join(country_path, csv_file)
                df = pd.read_csv(file_path)
                df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date is datetime
                revision_data.append(df)
        
        if not revision_data:
            print(f"No revision data found for {country}. Skipping.")
            continue
        
        # Combine data and aggregate by 8-week periods
        combined_data = pd.concat(revision_data)
        combined_data = (
            combined_data.groupby(pd.Grouper(key='Date', freq='8W'))  # Group by 8-week intervals
            .size()
            .reset_index(name='Revisions')
        )
        
        # Plot the line chart
        plt.figure(figsize=(12, 6))
        plt.plot(
            combined_data['Date'], combined_data['Revisions'],
            label="Total Revisions", linewidth=2, marker="o"
        )
        
        # Add election periods as shaded regions
        added_election_labels = set()
        if country in ELECTION_PERIODS:
            for election_type, dates in ELECTION_PERIODS[country].items():
                for election_date in dates:
                    election_date = pd.to_datetime(election_date)
                    start_date = election_date - pd.Timedelta(days=180)  # 6 months before
                    end_date = election_date + pd.Timedelta(days=180)    # 6 months after
                    color = ELECTION_COLORS[election_type]
                    if election_type not in added_election_labels:
                        plt.axvspan(start_date, end_date, color=color, alpha=0.3, label=f"{election_type} Election")
                        added_election_labels.add(election_type)
                    else:
                        plt.axvspan(start_date, end_date, color=color, alpha=0.3)
        
        # Logarithmic Y-axis
        plt.yscale('log')
        
        # Formatting
        plt.title(f"Revision Trends for {country}", fontsize=16)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Number of Revisions (log scale)", fontsize=12)
        plt.legend()
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # Show date every 6 months
        plt.xticks(rotation=45)
        
        # Save the plot
        plot_path = os.path.join(country_path, f"{country}_revision_trends.png")
        plt.tight_layout()
        plt.savefig(plot_path)
        print(f"Saved revision trend plot for {country} at {plot_path}")
        plt.close()

if __name__ == "__main__":
    base_folder = os.getcwd()  # Current directory
    plot_revisions_trends(base_folder)