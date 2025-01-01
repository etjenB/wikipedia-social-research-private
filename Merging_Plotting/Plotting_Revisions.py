import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Election details
election_times = {
    'UK': {
        'General': ['2010-05-06', '2015-05-07', '2017-06-08', '2019-12-12', '2024-07-04']
    },
    'USA-Represantatives': {
        'Represantatives': ['2012-11-06', '2014-11-04', '2016-11-08', '2018-11-06', '2020-11-03'],
    },
    'USA-Senat': {
        'Senators': ['2012-11-06', '2014-11-04', '2016-11-08', '2018-11-06', '2020-11-03']
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

def plot_revisions_country(data_folder, plots_folder):
    if not os.path.exists(plots_folder):
        os.makedirs(plots_folder)  # Create the plots folder if it doesn't exist

    for country_file in os.listdir(data_folder):
        if not country_file.endswith('.csv'):
            continue  # Skip non-CSV files

        country_name = country_file.split('_')[0]  # Extract country name from filename
        file_path = os.path.join(data_folder, country_file)
        dataframe = pd.read_csv(file_path)

        # Convert 'Date' column to datetime
        dataframe['Date'] = pd.to_datetime(dataframe['Date'])

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
        if country_name in election_times:
            for election_type, dates in election_times[country_name].items():
                for election_date in dates:
                    # Convert the election date to a datetime object
                    election_date = pd.to_datetime(election_date)

                    start_date = election_date - pd.Timedelta(days=90)
                    end_date = election_date + pd.Timedelta(days=90)
                    color = election_color[election_type]
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
    data_folder = "/Users/leonmoik/Documents/RevisionData/Final Datasets"  # Input folder
    plots_folder = "/Users/leonmoik/Documents/RevisionData/Plots"  # Output folder
    plot_revisions_country(data_folder, plots_folder)