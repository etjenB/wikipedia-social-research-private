import os
import pandas as pd

# Define base directory and file paths dynamically
base_dir = os.path.abspath(os.getcwd())
data_dir = os.path.join(base_dir, "RevisionData")

# Function to map party names and update the CSV
def map_party(file_path, column_name, mapping_dict):
    df = pd.read_csv(file_path)
    df['Party'] = df[column_name].map(mapping_dict)
    df.drop(columns=[column_name], inplace=True)
    df.to_csv(file_path, index=False)
    print(f"Updated {file_path}")

# Mapping dictionaries
party_mapping_aus = {
    'GRÜNE': 'GRÜNE',
    'ÖVP': 'ÖVP',
    'FPÖ': 'FPÖ',
    'SPÖ': 'SPÖ',
    'NEOS': 'NEOS',
    'fraktionslos': 'Independent',
}

party_mapping_ger = {
    'FDP': 'FDP', 
    'CDU/CSU (CDU)': 'CDU',
    'CDU': 'CDU',
    'SPD': 'SPD',
    'DIE LINKE': 'DIE LINKE',
    'Linke': 'DIE LINKE', 
    'Die Linke': 'DIE LINKE', 
    'AfD': 'AFD', 
    'Grüne': 'GRÜNE', 
    'GRÜNE': 'GRÜNE',
    'CDU/CSU (CSU)': 'CSU', 
    'CSU': 'CSU', 
    'BSW': 'BSW', 
    'fraktionslos (LKR)': 'Independent',
    'fraktionslos': 'Independent', 
    'fraktionslos (SSW)': 'Independent', 
    'fraktionslos (AfD)': 'Independent',
}

party_mapping_uk = {
    'Conservative': 'Conservative', 'Conservative Party': 'Conservative', 'Labour': 'Labour',
    'Labour Co-operative': 'Labour', 'Liberal Democrats': 'Liberal Democrats', 'Liberal Democrats[j]': 'Liberal Democrats',
    'Liberal Democrats[h]': 'Liberal Democrats', 'Liberal Democrats[i]': 'Liberal Democrats', 'Liberal Democrats[k]': 'Liberal Democrats',
    'Scottish National': 'SNP', 'SNP': 'SNP', 'Green': 'Green Party', 'Green Party': 'Green Party', 'Plaid Cymru': 'Plaid Cymru',
    'SDLP': 'SDLP', 'Social Democratic and Labour': 'SDLP', 'DUP': 'DUP', 'Democratic Unionist': 'DUP',
    'Democratic Unionist Party': 'DUP', 'UUP': 'UUP', 'Sinn Féin': 'Sinn Féin', 'Alliance': 'Alliance', 'Respect': 'Respect',
    'Change UK[h]': 'Change UK', 'Change UK[j]': 'Change UK', 'Change UK[i]': 'Change UK', 'UKIP': 'UKIP',
    'Independent[j]': 'Independent', 'Independent': 'Independent', 'Independent[a]': 'Independent', 'Independent[i]': 'Independent',
    'Independent[h]': 'Independent', 'Independent(The Independents)[h]': 'Independent', 'Birkenhead Social Justice[i]': 'Other',
    'Health Concern': 'Other', 'BGPV': 'Other', 'The Speaker': 'Speaker', 'The Speaker seeking re-election': 'Speaker',
    'Speaker[i]': 'Speaker', 'Vacant[l]': 'Vacant', 'Vacant[i]': 'Vacant',
}

party_mapping_us_rep = {
    'D': 'Democratic Party', 
    'R': 'Republican Party',
}

party_mapping_us_sen = {
    'Republican': 'Republican Party', 
    'R': 'Republican Party', 
    'Democratic': 'Democratic Party', 
    'D': 'Democratic Party',
    'Independent[10]': 'Independent', 
    'Independent': 'Independent', 
    'I': 'Independent',
}

# Apply mappings to CSVs
map_party(os.path.join(data_dir, 'austria_politician_data.csv'), 'Wahlpartei', party_mapping_aus)
map_party(os.path.join(data_dir, 'germany_politician_data.csv'), 'Fraktion_Partei', party_mapping_ger)
map_party(os.path.join(data_dir, 'uk_politician_data.csv'), 'party', party_mapping_uk)
map_party(os.path.join(data_dir, 'us_representatives_data.csv'), 'party', party_mapping_us_rep)
map_party(os.path.join(data_dir, 'us_senators_data.csv'), 'party', party_mapping_us_sen)

print("Party mapping completed for all files.")
