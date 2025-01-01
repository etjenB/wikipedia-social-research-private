import os
import pandas as pd

def load_revision_data(revisions_folder):
    #Combine all CSV files of given directory
    revision_files = os.listdir(revisions_folder)
    revision_data = []
    
    for file in revision_files:
        if file.endswith('_revisions.csv'):
            try:
                politician_name = file.replace('_revisions.csv', '')
                revisions = pd.read_csv(os.path.join(revisions_folder, file))
                revisions['Politician'] = politician_name
                revision_data.append(revisions)
            except:
                continue
    
    return pd.concat(revision_data, ignore_index=True)

def load_politician_data(politicians_folder):
    #Combine all politician info of given directory
    politician_files = [file for file in os.listdir(politicians_folder) if file.endswith('.csv')]
    politician_data = []
    
    for file in politician_files:
        dataframe = pd.read_csv(os.path.join(politicians_folder, file))
        politician_data.append(dataframe)
    
    return pd.concat(politician_data, ignore_index=True)

def clean_and_merge_data(revisions_dataframe, dataframe):
    #Create Politician column
    dataframe['Politician'] = dataframe['wiki_tag']

    # Merging revision dataframe with politician information
    merged_dataframe = pd.merge(revisions_dataframe, dataframe, on='Politician', how='inner')
    
    return merged_dataframe

def save_politician_data(merged_dataframe, output_folder):
    #Save Merged data into csv file 
    output_file = os.path.join(output_folder, 'us_sen_politician_data.csv') #change file name
    merged_dataframe.to_csv(output_file, index=False)


revisions_uk = '/Users/leonmoik/Documents/RevisionData/UK/revisions'
revisions_us = '/Users/leonmoik/Documents/RevisionData/USA/revisions'
uk_folder = '/Users/leonmoik/Documents/RevisionData/UK/election_data'
us_represantatives_folder = '/Users/leonmoik/Documents/RevisionData/USA/representatives_data'
us_senators_folder = '/Users/leonmoik/Documents/RevisionData/USA/senators_data'
output_folder = '/Users/leonmoik/Documents/RevisionData'


#UK
revisions_dataframe = load_revision_data(revisions_uk)
uk_dataframe = load_politician_data(uk_folder)
merged_dataframe = clean_and_merge_data(revisions_dataframe, uk_dataframe)
save_politician_data(merged_dataframe, output_folder)

#US Reps
revisions_dataframe = load_revision_data(revisions_us)
us_dataframe = load_politician_data(us_represantatives_folder)
merged_dataframe = clean_and_merge_data(revisions_dataframe, us_dataframe)
save_politician_data(merged_dataframe, output_folder)

#US Senat
revisions_dataframe = load_revision_data(revisions_us)
us_dataframe = load_politician_data(us_senators_folder)
merged_dataframe = clean_and_merge_data(revisions_dataframe, us_dataframe)
save_politician_data(merged_dataframe, output_folder)