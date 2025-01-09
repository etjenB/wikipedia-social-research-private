import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Election details
election_times = {
    'UK': {
        'General': ['2010-05-06', '2015-05-07', '2017-06-08', '2019-12-12', '2024-07-04']
    },
    'USA': {
        'General': ['2012-11-06', '2014-11-04', '2016-11-08', '2018-11-06', '2020-11-03', '2022-11-08', '2024-11-05']
    },
    'Germany': {
        'Bundestag': ['2013-09-22', '2017-09-24', '2021-09-26']
    },
    'Austria': {
        'Nationalrat': ['2013-09-29', '2017-10-15', '2019-09-29', '2024-09-29']
    }
}

election_color = {
    "Bundestag": "blue",
    "Represantatives": "blue",
    "Senators": "blue",
    "Nationalrat": "blue",
    "General": "blue"
}

country_name_mapping = {
    "us": "USA",
    "uk": "UK",
    "germany": "Germany",
    "austria": "Austria",
}

def plot_revisions_country(data_folder, plots_folder):
    if not os.path.exists(plots_folder):
        os.makedirs(plots_folder)  # Create the plots folder if it doesn't exist

    us_combined = False  # Flag to track if US plot is combined

    for country_file in os.listdir(data_folder):
        if not country_file.endswith('.csv'):
            continue  # Skip non-CSV files

        country_name = country_file.split('_')[0]  # Extract country name from filename

        # Skip individual US files after creating the combined plot
        if country_name == "us" and us_combined:
            continue

        # Special handling for the United States
        if country_name == "us" and not us_combined:
            # Paths to the Representatives and Senators data files
            representatives_path = os.path.join(data_folder, "us_representatives_data.csv")
            senators_path = os.path.join(data_folder, "us_senators_data.csv")

            # Check if both files exist
            if not os.path.exists(representatives_path) or not os.path.exists(senators_path):
                print(f"Error: One or both US data files are missing! Expected at:\n"
                    f"Representatives: {representatives_path}\n"
                    f"Senators: {senators_path}")
                continue

            # Load both data files into DataFrames
            try:
                rep_data = pd.read_csv(representatives_path)
                sen_data = pd.read_csv(senators_path)
            except Exception as e:
                print(f"Error reading US data files: {e}")
                continue

            # Convert 'Date' columns to datetime in both DataFrames
            rep_data['Date'] = pd.to_datetime(rep_data['Date'], errors='coerce')
            sen_data['Date'] = pd.to_datetime(sen_data['Date'], errors='coerce')

            # Combine the two DataFrames
            dataframe = pd.concat([rep_data, sen_data], ignore_index=True)
            print(f"Successfully combined Representatives and Senators data for USA. Total records: {len(dataframe)}")

            # Assign USA-specific variables
            country_name = "USA"  # For the plot title and file name
            mapped_country_name = "USA-Combined"  # For looking up election details
            us_combined = True  # Set the flag to avoid reprocessing this block later

        else:
            # For other countries, process normally
            file_path = os.path.join(data_folder, country_file)

            # Check if the file exists
            if not os.path.exists(file_path):
                print(f"Error: Data file for {country_file} not found at {file_path}")
                continue

            # Load the country's data file into a DataFrame
            try:
                dataframe = pd.read_csv(file_path)
            except Exception as e:
                print(f"Error reading data file for {country_file}: {e}")
                continue

            # Convert 'Date' column to datetime
            dataframe['Date'] = pd.to_datetime(dataframe['Date'], errors='coerce')
            print(f"Loaded data for {country_name}. Total records: {len(dataframe)}")

        # Group data by 8-week periods and by party
        grouped_data = (dataframe.groupby([pd.Grouper(key='Date', freq='8W'), 'Party'])
                        .size()
                        .reset_index(name='Revisions'))

        # Filter data to the timeframe 2010-2024
        grouped_data = grouped_data[(grouped_data['Date'] >= '2010-01-01') & 
                                    (grouped_data['Date'] <= '2024-12-31')]

        # Plotting
        plt.figure(figsize=(12, 6))
        for party in grouped_data['Party'].unique():
            party_data = grouped_data[grouped_data['Party'] == party]
            plt.plot(party_data['Date'], party_data['Revisions'], label=party, linewidth=2, marker='.')

        # Add election period highlights
        added_election_labels = set()

        # Map the country name correctly for election periods
        mapped_country_name = country_name_mapping.get(country_name.lower(), country_name)

        if mapped_country_name in election_times:
            for election_type, dates in election_times[mapped_country_name].items():
                for election_date in dates:
                    # Convert the election date to a datetime object
                    election_date = pd.to_datetime(election_date, errors='coerce')

                    # Ensure valid datetime
                    if pd.isna(election_date):
                        continue

                    start_date = election_date - pd.Timedelta(days=90)
                    end_date = election_date + pd.Timedelta(days=90)
                    color = election_color.get(election_type, 'grey')  # Default to gray if type not found

                    # Add axvspan and ensure no duplicate labels
                    if election_type not in added_election_labels:
                        plt.axvspan(start_date, end_date, color=color, alpha=0.2, label=f'{election_type} Election')
                        added_election_labels.add(election_type)
                    else:
                        plt.axvspan(start_date, end_date, color=color, alpha=0.2)

        # Set plot title and labels
        plt.title(f"Wikipedia Revisions Trends in {country_name}")
        plt.xlabel("Date")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # Show date every 6 months
        plt.xticks(rotation=45)
        plt.ylabel("Number of Revisions per 8 Weeks")
        plt.legend()

        # Save the plot
        plot_path = os.path.join(plots_folder, f"{country_name}_revisions_trends.png")
        plt.tight_layout()
        plt.savefig(plot_path)
        print(f"Saved plot for {country_name} at {plot_path}")
        plt.close()

if __name__ == "__main__":
    base_dir = os.path.abspath(os.getcwd())
    data_folder = os.path.join(base_dir, "RevisionData")  # Input folder
    plots_folder = os.path.join(data_folder, "Plots")  # Output folder
    plot_revisions_country(data_folder, plots_folder)