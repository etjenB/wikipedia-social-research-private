import os
import pandas as pd

# Get the base directory of the script execution
base_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))

# Define paths dynamically based on the base directory
revisions_uk = os.path.join(base_dir, "FetchingRelevantPoliticians", "UK", "UK_Politicians")
revisions_us = os.path.join(base_dir, "FetchingRelevantPoliticians", "USA", "USA_Politicians")
uk_folder = os.path.join(base_dir, "FetchingRelevantPoliticians", "UK", "election_data")
us_representatives_folder = os.path.join(base_dir, "FetchingRelevantPoliticians", "USA", "representatives_data")
us_senators_folder = os.path.join(base_dir, "FetchingRelevantPoliticians", "USA", "senators_data")

# Define the output folder within Merging_Plotting
output_folder = os.path.join(os.getcwd(), "RevisionData")

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def load_revision_data(revisions_folder):
    # Combine all CSV files in the given directory
    revision_files = os.listdir(revisions_folder)
    revision_data = []
    
    for file in revision_files:
        if file.endswith('_revisions.csv'):
            try:
                politician_name = file.replace('_revisions.csv', '')
                revisions = pd.read_csv(os.path.join(revisions_folder, file))
                revisions['Politician'] = politician_name
                revision_data.append(revisions)
            except Exception as e:
                print(f"Error processing file {file}: {e}")
                continue
    
    return pd.concat(revision_data, ignore_index=True)

def load_politician_data(politicians_folder):
    # Combine all politician info CSVs in the given directory
    politician_files = [file for file in os.listdir(politicians_folder) if file.endswith('.csv')]
    politician_data = []
    
    for file in politician_files:
        dataframe = pd.read_csv(os.path.join(politicians_folder, file))
        politician_data.append(dataframe)
    
    return pd.concat(politician_data, ignore_index=True)

def clean_and_merge_data(revisions_dataframe, dataframe):
    # Create a Politician column in the dataframe
    dataframe['Politician'] = dataframe['wiki_tag']

    # Merge revision dataframe with politician information
    merged_dataframe = pd.merge(revisions_dataframe, dataframe, on='Politician', how='inner')
    
    return merged_dataframe

def save_politician_data(merged_dataframe, output_file):
    # Save merged data to a CSV file
    merged_dataframe.to_csv(output_file, index=False)

def process_and_save(revisions_folder, data_folder, output_filename):
    revisions_dataframe = load_revision_data(revisions_folder)
    dataframe = load_politician_data(data_folder)
    merged_dataframe = clean_and_merge_data(revisions_dataframe, dataframe)
    output_file = os.path.join(output_folder, output_filename)
    save_politician_data(merged_dataframe, output_file)

if __name__ == "__main__":
    # Process UK data
    process_and_save(revisions_uk, uk_folder, "uk_politician_data.csv")
    
    # Process US Representatives data
    process_and_save(revisions_us, us_representatives_folder, "us_representatives_data.csv")
    
    # Process US Senators data
    process_and_save(revisions_us, us_senators_folder, "us_senators_data.csv")

    print(f"Data has been successfully processed and saved in '{output_folder}'")
