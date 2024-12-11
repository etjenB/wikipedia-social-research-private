import requests
import pandas as pd
import os
from datetime import datetime

# Function to fetch revisions for a single article
def fetch_revisions(title, start_date=None, end_date=None):
    url = "https://de.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": title,
        "rvlimit": "max",
        "rvprop": "timestamp|size|user|tags|comment",
        "rvstart": start_date,  # Optional start date
        "rvend": end_date,      # Optional end date
    }
    all_revisions = []
    session = requests.Session()
    while True:
        response = session.get(url, params=params)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            revisions = page_data.get("revisions", [])
            all_revisions.extend(revisions)
        
        if "continue" in data:
            params.update(data["continue"])
        else:
            break
    return all_revisions

# Function to save revisions to CSV only if there are revisions
def save_revisions_to_csv(revisions, article_title, country):
    if not revisions:
        print(f"No revisions found for '{article_title}' in '{country}'. Skipping...")
        return  # Exit the function if there are no revisions

    revision_data = []
    for i in range(len(revisions)):
        prev_size = revisions[i + 1].get("size", 0) if i < len(revisions) - 1 else 0
        curr_size = revisions[i].get("size", 0)
        
        revision_data.append({
            "Country": country,
            "Article": article_title,
            "Date": revisions[i]["timestamp"][:10],
            "Time": revisions[i]["timestamp"],
            "User": revisions[i].get("user", "Unknown"),
            "Size": curr_size,
            "Changes": curr_size - prev_size,
            "Comment": revisions[i].get("comment", "No comment"),
            "Tags": ", ".join(revisions[i].get("tags", [])) if revisions[i].get("tags") else "None"
        })
    
    # Save to CSV
    df = pd.DataFrame(revision_data)

    # Create folder structure for country if it doesn't exist
    country_dir = os.path.join(os.getcwd(), country)
    if not os.path.exists(country_dir):
        os.makedirs(country_dir)

    # Create file path for the politician
    file_name = f"{article_title}_revisions.csv"
    file_path = os.path.join(country_dir, file_name)

    # Save the file
    df.to_csv(file_path, index=False)
    print(f"Saved revisions for '{article_title}' in '{file_path}'")

# Main pipeline to fetch revisions for multiple articles
def main_pipeline(politicians):
    for country, articles in politicians.items():
        for article in articles:
            print(f"Fetching revisions for {article} ({country})...")
            revisions = fetch_revisions(article)
            if revisions:  # Only save if there are revisions
                save_revisions_to_csv(revisions, article, country)
            else:
                print(f"No revisions found for {article} ({country}). Skipping...")

if __name__ == "__main__":
    # Define countries and their politicians
        politicians = {
        "Germany": [
            "Angela_Merkel", "Olaf_Scholz", "Annalena_Baerbock",
            "Christian_Lindner", "Friedrich_Merz", "Sahra_Wagenknecht"
        ],
        "USA": [
            "Joe_Biden", "Donald_Trump", "Kamala_Harris",
            "Bernie_Sanders", "Nancy_Pelosi", "Mitch_McConnell",
            "Alexandria_Ocasio-Cortez", "Ron_DeSantis"
        ],
        "Nigeria": [
            "Muhammadu_Buhari", "Goodluck_Jonathan", "Bola_Tinubu",
            "Atiku_Abubakar", "Peter_Obi", "Yemi_Osinbajo"
        ],
        "Austria": [
            "Sebastian_Kurz", "Alexander_Van_der_Bellen", "Karl_Nehammer",
            "Norbert_Hofer", "Herbert_Kickl", "Beate_Meinl-Reisinger"
        ],
        "Bosnia": [
            "Milorad_Dodik", "Bakir_Izetbegović", "Željko_Komšić",
            "Dragan_Čović", "Fahrudin_Radončić", "Elmedin_Konaković"
        ]
    }
        
"""
    politicians = {
    "Germany": ["Angela_Merkel", "Olaf_Scholz"],
    "USA": ["Joe_Biden", "Donald_Trump"],
    "Nigeria": ["Muhammadu_Buhari", "Goodluck_Jonathan"],
    "Austria": ["Sebastian_Kurz", "Alexander_Van_der_Bellen"],
    "Bosnia": ["Milorad_Dodik", "Bakir_Izetbegović"]
}
"""

# Run the pipeline
main_pipeline(politicians)
