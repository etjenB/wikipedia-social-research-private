import pandas as pd

#Mapping parties of Countries 
def map_party(df, column_name, mapping_dict, output_file):
    df['Party'] = df[column_name].map(mapping_dict)
    df.drop(columns=[column_name], inplace=True)
    df.to_csv(output_file, index=False)


#Mapping Austrian parties 
aus = pd.read_csv('/Users/leonmoik/Documents/RevisionData/austria_politician_data.csv')
map_party(aus, 'Wahlpartei', {}, '/Users/leonmoik/Documents/RevisionData/austria_politician_data.csv')

#Mapping German parties
ger = pd.read_csv('/Users/leonmoik/Documents/RevisionData/germany_politician_data.csv')
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
map_party(ger, 'Fraktion_Partei', party_mapping_ger, '/Users/leonmoik/Documents/RevisionData/germany_politician_Data.csv')



#Mapping UK parties
uk = pd.read_csv('/Users/leonmoik/Documents/RevisionData/uk_politician_data.csv')
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
map_party(uk, 'party', party_mapping_uk, '/Users/leonmoik/Documents/RevisionData/uk_politician_data.csv')


#Mapping US Represantatives Parties
us1 = pd.read_csv('/Users/leonmoik/Documents/RevisionData/us_rep_politician_data.csv')
party_mapping_us1 = {
    'D': 'Democratic Party', 
    'R': 'Republican Party',
}
map_party(us1, 'party', party_mapping_us1, '/Users/leonmoik/Documents/RevisionData/us_rep_politician_data.csv')



#Mapping US Senat Parties 
us2 = pd.read_csv('/Users/leonmoik/Documents/RevisionData/us_sen_politician_data.csv')
party_mapping_us2 = {
    'Republican': 'Republican Party', 
    'R': 'Republican Party', 
    'Democratic': 'Democratic Party', 
    'D': 'Democratic Party',
    'Independent[10]': 'Independent', 
    'Independent': 'Independent', 
    'I': 'Independent',
}
map_party(us2, 'party', party_mapping_us2, '/Users/leonmoik/Documents/RevisionData/us_sen_politician_data.csv')
