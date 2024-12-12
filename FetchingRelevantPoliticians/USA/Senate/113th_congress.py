import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URL for the 113th Congress
url_113th = "https://en.wikipedia.org/wiki/List_of_United_States_senators_in_the_113th_Congress"

def fetch_senators_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

    # Decode content with proper encoding
    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), "html.parser")

    # Locate the heading with id="U.S._Senate_seniority_list" and find the table after it
    heading = soup.find(id="U.S._Senate_seniority_list")
    if not heading:
        print("No heading with id 'U.S._Senate_seniority_list' found.")
        return None

    table = heading.find_next("table", class_="wikitable")
    if not table:
        print("No table found after the specified heading.")
        return None

    rows = table.find_all("tr")[1:]  # Skip header row

    data = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 1:  # Ensure the row has enough cells
            senator_cell = cells[0]  # Assuming the senator info is in the 1st column
            senator_link = senator_cell.find("a", href=True, title=True)
            if senator_link and "wiki" in senator_link["href"] and "redlink=1" not in senator_link["href"]:
                senator_name = senator_link.get_text(strip=True)
                wiki_tag = senator_link["href"].split("/wiki/")[-1]

                # Extract party and state if available
                party_link = senator_cell.find_all("a", href=True, title=True)[1]
                state_link = senator_cell.find_all("a", href=True, title=True)[2]
                party = party_link.get_text(strip=True) if party_link else None
                state = state_link.get_text(strip=True) if state_link else None

                data.append({
                    "name": senator_name,
                    "wiki_tag": wiki_tag,
                    "party": party,
                    "state": state
                })

    return data

def save_to_csv(data):
    if not data:
        print("No data to save.")
        return

    # Ensure proper encoding when saving to CSV
    df = pd.DataFrame(data)
    os.makedirs("senators_data", exist_ok=True)
    file_path = os.path.join("senators_data", "senators_113th_congress.csv")
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"Data saved to {file_path}.")

def main():
    print("Processing data for the 113th Congress...")
    data = fetch_senators_data(url_113th)
    save_to_csv(data)

if __name__ == "__main__":
    main()