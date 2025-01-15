import os
import pandas as pd
import matplotlib.pyplot as plt

# Party alignments
party_alignment = {
    # Austria
    'GRÜNE': 'left',
    'FPÖ': 'right',
    'NEOS': 'center',
    'SPÖ': 'left',
    'ÖVP': 'right',

    # Germany
    'AFD': 'right',
    'CDU': 'right',
    'CSU': 'right',
    'DIE LINKE': 'left',
    'FDP': 'center',
    'GRÜNE': 'left',
    'SPD': 'left',
    'BSW': 'right',
    'Vacant': 'neutral',

    # UK
    'Conservative': 'right',
    'Labour': 'left',
    'Liberal Democrats': 'center',
    'Green Party': 'left',
    'SNP': 'left',
    'Plaid Cymru': 'left',
    'UKIP': 'right',
    'DUP': 'right',
    'SDLP': 'left',
    'Respect': 'left',
    'Alliance': 'center',
    'Sinn Féin': 'left',
    'UUP': 'right',
    'Change UK': 'center',
    'Independent': 'neutral',
    'Speaker': 'neutral',
    'Other': 'neutral',

    # USA
    'Democratic Party': 'left',
    'Republican Party': 'right',

    # Additional
    'Vacant': 'neutral'
}

def load_and_preprocess_data(data_folder, country_file):
    country_name = country_file.split('_')[0]

    # Special handling for the United States (combining Representatives and Senators data)
    if country_name == "us":
        representatives_path = os.path.join(data_folder, "us_representatives_data.csv")
        senators_path = os.path.join(data_folder, "us_senators_data.csv")

        if not os.path.exists(representatives_path) or not os.path.exists(senators_path):
            print(f"Error: One or both US data files are missing!")
            return None, None  # Return None for both dataframe and country_name

        try:
            rep_data = pd.read_csv(representatives_path)
            sen_data = pd.read_csv(senators_path)
            rep_data['Date'] = pd.to_datetime(rep_data['Date'], errors='coerce')
            sen_data['Date'] = pd.to_datetime(sen_data['Date'], errors='coerce')
            dataframe = pd.concat([rep_data, sen_data], ignore_index=True)
            country_name = "USA"  # Use "USA" for the combined plot
        except Exception as e:
            print(f"Error reading US data files: {e}")
            return None, None

    else:
        file_path = os.path.join(data_folder, country_file)
        if not os.path.exists(file_path):
            print(f"Error: Data file for {country_file} not found at {file_path}")
            return None, None

        try:
            dataframe = pd.read_csv(file_path)
            dataframe['Date'] = pd.to_datetime(dataframe['Date'], errors='coerce')
        except Exception as e:
            print(f"Error reading data file for {country_file}: {e}")
            return None, None

    return dataframe, country_name

def create_alignment_bar_charts(data_folder, plots_folder):
    if not os.path.exists(plots_folder):
        os.makedirs(plots_folder)

    for country_file in os.listdir(data_folder):
        if not country_file.endswith('.csv'):
            continue

        dataframe, country_name = load_and_preprocess_data(data_folder, country_file)
        if dataframe is None:  # Skip to the next file if data loading failed
            continue

        # Group data by 8 week periods and by party
        grouped_data = dataframe.groupby([pd.Grouper(key='Date', freq='8W'), 'Party']).size().reset_index(
            name='Revisions')

        # Filter data to the timeframe 2010-2024
        grouped_data = grouped_data[
            (grouped_data['Date'] >= '2010-01-01') & (grouped_data['Date'] <= '2024-12-31')]

        # Calculate Revisions by Alignment
        revisions_by_alignment = {'left': 0, 'right': 0}
        for index, row in grouped_data.iterrows():
            party = row['Party']
            alignment = party_alignment.get(party, 'neutral')
            if alignment in revisions_by_alignment:
                revisions_by_alignment[alignment] += row['Revisions']

        plt.figure(figsize=(8, 6))  # Adjust figure size if needed

        bar_width = 0.5  # Adjust bar width
        x_positions = [1, 2]  # Positions for the left and right bars

        bars = plt.bar(x_positions, revisions_by_alignment.values(),
                       color=['red', 'blue'], width=bar_width)

        # Add value labels to the top of each bar
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), va='bottom', ha='center')

        #plt.title(f"Total Wikipedia Revisions by Political Alignment in {country_name}")
        #plt.xlabel("Political Alignment")
        #plt.ylabel("Number of Revisions")
        plt.axhline(y=0, color='black', linewidth=0.8)

        # Set x-axis ticks and labels to match bar positions
        plt.xticks(x_positions, revisions_by_alignment.keys())

        plt.tight_layout()

        # Save the bar chart
        bar_chart_path = os.path.join(plots_folder, f"{country_name}_alignment_revisions_barchart.png")
        plt.savefig(bar_chart_path)
        print(f"Saved bar chart for {country_name} at {bar_chart_path}")
        plt.close()

if __name__ == "__main__":
    base_dir = os.path.abspath(os.getcwd())
    data_folder = os.path.join(base_dir, "RevisionData")  # Input folder
    plots_folder = os.path.join(data_folder, "BarChartPlots")  # Output folder for bar charys
    create_alignment_bar_charts(data_folder, plots_folder)