import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URL for the 2015 election
url_2015 = "https://en.wikipedia.org/wiki/List_of_MPs_elected_in_the_2015_United_Kingdom_general_election"

def fetch_mps_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

    # Decode content with proper encoding
    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), "html.parser")
    table = soup.find("table", {"id": "elected-mps"})

    if not table:
        print("No table found.")
        return None

    rows = table.find_all("tr")[1:]  # Skip header row

    data = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 5:  # Adjust based on the number of columns
            constituency = cells[0].get_text(strip=True)
            party = cells[2].get_text(strip=True)

            mp_cell = cells[4]  # MP info is in the 5th cell (index 4)
            mp_name = None
            wiki_tag = None

            # Look for the MP's name and link explicitly
            mp_name_link = mp_cell.find("a", href=True, title=True)
            if mp_name_link and "wiki" in mp_name_link["href"]:
                mp_name = mp_name_link.get_text(strip=True)
                wiki_tag = mp_name_link["href"].split("/wiki/")[-1]

            if mp_name and wiki_tag:
                data.append({
                    "constituency": constituency,
                    "party": party,
                    "name": mp_name,
                    "wiki_tag": wiki_tag,
                })

    return data

def save_to_csv(data):
    if not data:
        print("No data to save.")
        return

    # Ensure proper encoding when saving to CSV
    df = pd.DataFrame(data)
    os.makedirs("election_data", exist_ok=True)
    file_path = os.path.join("election_data", "mps_2015.csv")
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"Data saved to {file_path}.")

def main():
    print("Processing data for 2015...")
    data = fetch_mps_data(url_2015)
    save_to_csv(data)

if __name__ == "__main__":
    main()
