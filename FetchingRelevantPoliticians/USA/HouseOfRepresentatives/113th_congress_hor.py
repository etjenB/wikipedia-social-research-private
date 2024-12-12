import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URLs for the House of Representatives
urls = {
    "113th": "https://en.wikipedia.org/wiki/List_of_members_of_the_United_States_House_of_Representatives_in_the_113th_Congress_by_seniority"
}

def fetch_representatives_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), "html.parser")

    # Attempt to locate the heading using multiple possible IDs
    heading_ids = ["Complete_seniority_list", "Seniority_list"]
    heading = None
    for heading_id in heading_ids:
        heading = soup.find(id=heading_id)
        if heading:
            break

    if not heading:
        print("No valid heading found with the expected IDs.")
        return None

    # Find the first table element after the heading
    table = heading.find_next(lambda tag: tag.name == "table" and "wikitable" in tag.get("class", []))
    if not table:
        print("No table found after the specified heading.")
        return None

    rows = table.find_all("tr")[1:]  # Skip header row

    data = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 4:  # Ensure the row has enough cells for required data
            # Representative's name and wiki tag
            rep_cell = cells[1]
            rep_link = rep_cell.find("a", href=True, title=True)
            if rep_link and "wiki" in rep_link["href"] and "redlink=1" not in rep_link["href"]:
                rep_name = rep_link.get_text(strip=True)
                wiki_tag = rep_link["href"].split("/wiki/")[-1]

                # Party
                party = cells[2].get_text(strip=True)

                # District
                district_cell = cells[3]
                district_link = district_cell.find("a", href=True, title=True)
                district = district_link.get_text(strip=True) if district_link else district_cell.get_text(strip=True)

                data.append({
                    "name": rep_name,
                    "wiki_tag": wiki_tag,
                    "party": party,
                    "district": district
                })

    return data

def save_to_csv(data, congress):
    if not data:
        print(f"No data to save for {congress}.")
        return

    # Ensure proper encoding when saving to CSV
    df = pd.DataFrame(data)
    os.makedirs("representatives_data", exist_ok=True)
    file_path = os.path.join("representatives_data", f"representatives_{congress}_congress.csv")
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"Data saved to {file_path}.")

def main():
    for congress, url in urls.items():
        print(f"Processing data for the {congress} Congress...")
        data = fetch_representatives_data(url)
        save_to_csv(data, congress)

if __name__ == "__main__":
    main()