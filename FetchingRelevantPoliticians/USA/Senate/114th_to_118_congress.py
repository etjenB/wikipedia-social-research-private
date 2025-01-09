import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URLs for the Congresses
urls = {
    "114th": "https://en.wikipedia.org/wiki/List_of_United_States_senators_in_the_114th_Congress",
    "115th": "https://en.wikipedia.org/wiki/List_of_United_States_senators_in_the_115th_Congress",
    "116th": "https://en.wikipedia.org/wiki/List_of_United_States_senators_in_the_116th_Congress",
    "117th": "https://en.wikipedia.org/wiki/List_of_United_States_senators_in_the_117th_Congress",
    "118th": "https://en.wikipedia.org/wiki/List_of_United_States_senators_in_the_118th_Congress"
}

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

        # Adjust based on the number of columns in the table
        if len(cells) >= 2:  # Ensure the row has enough cells for name, party, and state
            # Senator's name and wiki tag
            senator_cell = cells[0]  # The 1st column contains the senator's name
            senator_link = senator_cell.find("a", href=True, title=True)
            if senator_link and "wiki" in senator_link["href"] and "redlink=1" not in senator_link["href"]:
                senator_name = senator_link.get_text(strip=True)
                wiki_tag = senator_link["href"].split("/wiki/")[-1]

                # Party (2nd column)
                party = cells[1].get_text(strip=True)

                # State (3rd column)
                state_cell = cells[2]
                state_link = state_cell.find("a", href=True, title=True)
                state = state_link.get_text(strip=True) if state_link else state_cell.get_text(strip=True)

                data.append({
                    "name": senator_name,
                    "wiki_tag": wiki_tag,
                    "party": party,
                    "state": state
                })

    return data

def save_to_csv(data, congress):
    if not data:
        print(f"No data to save for {congress}.")
        return

    # Ensure proper encoding when saving to CSV
    df = pd.DataFrame(data)
    os.makedirs("senators_data", exist_ok=True)
    file_path = os.path.join("senators_data", f"senators_{congress}_congress.csv")
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"Data saved to {file_path}.")

def main():
    for congress, url in urls.items():
        print(f"Processing data for the {congress} Congress...")
        data = fetch_senators_data(url)
        save_to_csv(data, congress)

if __name__ == "__main__":
    main()
