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

def load_politician_data(politicians_folder, country_name):
    #Combine all politician info of given directory and add Country Name as a column
    politician_files = [file for file in os.listdir(politicians_folder) if file.endswith('.csv')]
    politician_data = []
    
    for file in politician_files:
        dataframe = pd.read_csv(os.path.join(politicians_folder, file))
        dataframe['Country'] = country_name
        politician_data.append(dataframe)
    
    return pd.concat(politician_data, ignore_index=True)

def clean_and_merge_data(revisions_dataframe, austria_dataframe, germany_dataframe):
    #Merge revision dataframe with German and Austrian politician information
    #by creating a Politician column
    politicians_information = pd.concat([austria_dataframe, germany_dataframe], ignore_index=True)
    politicians_information['Politician'] = politicians_information['link'].str.split('/').str[-1]
    
    # Merging revision dataframe with politician information
    politicians_dataframe = pd.merge(revisions_dataframe, politicians_information, on='Politician', how='inner')
    
    # Combine 'Wahlpartei' columns and drop unnecessary columns
    politicians_dataframe['Wahlpartei'] = politicians_dataframe['Wahlpartei.1'].combine_first(politicians_dataframe['Wahl­partei.1'])
    politicians_dataframe.drop(columns=['Wahlpartei.1', 'Wahl­partei.1'], inplace=True)
    
    # Combine 'Fraktion_Partei' columns and drop unnecessary columns
    politicians_dataframe['Fraktion_Partei'] = (
        politicians_dataframe['Fraktion (ggf. Partei)']
        .combine_first(politicians_dataframe['Partei'])
        .combine_first(politicians_dataframe['Fraktion oder Gruppe (Partei)'])
    )
    politicians_dataframe.drop(columns=['Fraktion oder Gruppe (Partei)', 'Fraktion (ggf. Partei)', 'Partei'], inplace=True)
    
    return politicians_dataframe

def save_politician_data(politicians_dataframe, output_folder):
    #Save German and Austrian data in seperate CSVs 
    austrian_politicians = politicians_dataframe[politicians_dataframe['Country'] == 'Austria']
    german_politicians = politicians_dataframe[politicians_dataframe['Country'] == 'Germany']
    
    # Drop empty columns
    austrian_politicians.dropna(axis=1, how='any', inplace=True)
    german_politicians.dropna(axis=1, how='any', inplace=True)
    
    austrian_politicians.to_csv(os.path.join(output_folder, 'austria_politician_data.csv'), index=False)
    german_politicians.to_csv(os.path.join(output_folder, 'germany_politician_data.csv'), index=False)


revisions_ger_aus = '/Users/leonmoik/Documents/RevisionData/GER/Revisions_of_german_and_austiran_MoP/revisionen'
aus_folder = '/Users/leonmoik/Documents/RevisionData/GER/Austria_data/infos_to_austrian_mop/infos_to_austrian_mop'
ger_folder = '/Users/leonmoik/Documents/RevisionData/GER/Germany_data/infos_to_german_mop/infos_to_german_mop'
output_folder = '/Users/leonmoik/Documents/RevisionData'


revisions_dataframe = load_revision_data(revisions_ger_aus)
austria_dataframe = load_politician_data(aus_folder, 'Austria')
germany_dataframe = load_politician_data(ger_folder, 'Germany')
politicians_dataframe = clean_and_merge_data(revisions_dataframe, austria_dataframe, germany_dataframe)
save_politician_data(politicians_dataframe, output_folder)