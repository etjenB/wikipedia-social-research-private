import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Define election periods and their types for each country
ELECTION_PERIODS = {
    "Germany": {
        "Federal": ["2005-09-18", "2009-09-27", "2013-09-22", "2017-09-24", "2021-09-26"],
        "State": ["2018-10-14", "2022-10-09"]  # Add major state-level elections as needed
    },
    "USA": {
        "Presidential": ["2004-11-02", "2008-11-04", "2012-11-06", "2016-11-08", "2020-11-03"],
        "Midterm": ["2006-11-07", "2010-11-02", "2014-11-04", "2018-11-06", "2022-11-08"]
    },
    "UK": {
        "General": ["2005-05-05", "2010-05-06", "2015-05-07", "2017-06-08", "2019-12-12"],
        "Referendum": ["2016-06-23"]  # Brexit referendum
    },
    "France": {
        "Presidential": ["2007-04-22", "2012-04-22", "2017-04-23", "2022-04-10"],
        "Legislative": ["2007-06-10", "2012-06-10", "2017-06-11", "2022-06-12"]
    },
    "India": {
        "General": ["2004-04-20", "2009-04-16", "2014-04-07", "2019-04-11"],
        "State": ["2018-12-07", "2022-03-10"]  # Example state elections; add more specific ones
    },
    "Japan": {
        "General": ["2005-09-11", "2009-08-30", "2012-12-16", "2014-12-14", "2017-10-22", "2021-10-31"],
        "Upper_House": ["2004-07-11", "2007-07-29", "2010-07-11", "2013-07-21", "2016-07-10", "2019-07-21"]
    },
    "Spain": {
        "General": ["2004-03-14", "2008-03-09", "2011-11-20", "2015-12-20", "2016-06-26", "2019-11-10"],
        "Regional": ["2012-11-25", "2015-09-27", "2017-12-21", "2021-02-14"]  # Catalonia-focused examples
    },
    "Brazil": {
        "Presidential": ["2002-10-06", "2006-10-01", "2010-10-03", "2014-10-05", "2018-10-07", "2022-10-02"],
        "Local": ["2004-10-03", "2008-10-05", "2012-10-07", "2016-10-02", "2020-11-15"]
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
    "Referendum": "cyan",          # For events like Brexit
    "Upper_House": "teal",        # Japan-specific House of Councillors
    "Legislative": "violet"       # For France and other countries with legislative elections
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