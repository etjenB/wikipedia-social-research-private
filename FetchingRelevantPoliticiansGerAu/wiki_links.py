import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

output_dir = "Germany_Austria_data"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

## GERMANY------------------------------------------------------------------------------------------------

## deutscher bundestag
import pandas as pd
from bs4 import BeautifulSoup
import requests

link = 'https://de.wikipedia.org/wiki/Liste_der_Mitglieder_des_Deutschen_Bundestages_(20._Wahlperiode)'
html = requests.get(link).text
soup = BeautifulSoup(html,'html.parser')
links = []
name = []
tabel = soup.find('table','wikitable sortable tabelle-kopf-fixiert')
for row in tabel.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) >3:
        links.append(cells[1].find('a')['href'])
        name.append(cells[1].find('a').text)
        #print(cells[1].find('a')['href'])
links_df = pd.DataFrame({'Name':name, 'link':links})
df = pd.read_html(link)[2]
df = df.merge(links_df)
df.to_csv(os.path.join(output_dir, 'geram_20.csv'), index=None)

link = 'https://de.wikipedia.org/wiki/Liste_der_Mitglieder_des_Deutschen_Bundestages_(19._Wahlperiode)'
html = requests.get(link).text
soup = BeautifulSoup(html,'html.parser')
links = []
name = []
tabel = soup.find('table','wikitable sortable')
for row in tabel.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) >3:
        links.append(cells[1].find('a')['href'])
        name.append(cells[1].find('a').text)
links_df = pd.DataFrame({'Name':name, 'link':links})
df = pd.read_html(link)[3]
df = df.merge(links_df)
df.to_csv(os.path.join(output_dir, 'geram_19.csv'), index=None)

link = 'https://de.wikipedia.org/wiki/Liste_der_Mitglieder_des_Deutschen_Bundestages_(18._Wahlperiode)'
html = requests.get(link).text
soup = BeautifulSoup(html,'html.parser')
links = []
name = []
tabel = soup.find('table','wikitable zebra sortable')
for row in tabel.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) >3:
        links.append(cells[0].find('a')['href'])
        name.append(cells[0].find('a').text)
links_df = pd.DataFrame({'Name':name, 'link':links})
links_df
df = pd.read_html(link)[1]
df = df.rename({'Mitglied des Bundestages':'Name'},axis=1)
df = df.merge(links_df)
df.to_csv(os.path.join(output_dir, 'geram_18.csv'), index=None)

## AUSTRIA------------------------------------------------------------------------------------------------

link = 'https://de.wikipedia.org/wiki/Liste_der_Abgeordneten_zum_%C3%96sterreichischen_Nationalrat_(XXVIII._Gesetzgebungsperiode)'
html = requests.get(link).text
soup = BeautifulSoup(html,'html.parser')
links = []
name = []
tabel = soup.find('table')
for row in tabel.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) >3:
        links.append(cells[0].find('a')['href'])
        name.append(cells[0].find('a').text)
links_df = pd.DataFrame({'Name':name, 'link':links})
links_df
df = pd.read_html(link)[0]
df = df.merge(links_df)
df.to_csv(os.path.join(output_dir, 'austrian_28.csv'), index=None)

link = 'https://de.wikipedia.org/wiki/Liste_der_Abgeordneten_zum_%C3%96sterreichischen_Nationalrat_(XXVII._Gesetzgebungsperiode)'
html = requests.get(link).text
soup = BeautifulSoup(html,'html.parser')
links = []
name = []
tabel = soup.find('table')
for row in tabel.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) >3:
        links.append(cells[0].find('a')['href'])
        name.append(cells[0].find('a').text)
links_df = pd.DataFrame({'Name':name, 'link':links})
links_df
df = pd.read_html(link)[0]
df = df.merge(links_df)
df
df.to_csv(os.path.join(output_dir, 'austrian_27.csv'), index=None)

link = 'https://de.wikipedia.org/wiki/Liste_der_Abgeordneten_zum_%C3%96sterreichischen_Nationalrat_(XXVI._Gesetzgebungsperiode)'
html = requests.get(link).text
soup = BeautifulSoup(html,'html.parser')
links = []
name = []
tabel = soup.find('table')
for row in tabel.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) >3:
        links.append(cells[0].find('a')['href'])
        name.append(cells[0].find('a').text)
links_df = pd.DataFrame({'Name':name, 'link':links})
links_df
df = pd.read_html(link)[0]
df = df.merge(links_df)
df
df.to_csv(os.path.join(output_dir, 'austrian_26.csv'), index=None)

link = 'https://de.wikipedia.org/wiki/Liste_der_Abgeordneten_zum_%C3%96sterreichischen_Nationalrat_(XXV._Gesetzgebungsperiode)'
html = requests.get(link).text
soup = BeautifulSoup(html,'html.parser')
links = []
name = []
tabel = soup.find('table')
for row in tabel.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) >3:
        links.append(cells[0].find('a')['href'])
        name.append(cells[0].find('a').text)
links_df = pd.DataFrame({'Name':name, 'link':links})
links_df
df = pd.read_html(link)[0]
df = df.merge(links_df)
df
df.to_csv(os.path.join(output_dir, 'austrian_25.csv'), index=None)
