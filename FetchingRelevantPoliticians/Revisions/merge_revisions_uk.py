import requests
import pandas as pd
import os
from datetime import datetime
import glob

# Run in the docment where theres csvs
def fetch_revisions(title, lang="en", start_date=None, end_date=None):
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": title,
        "rvlimit": "max",
        "rvprop": "timestamp|size|user|tags|comment",
        "rvstart": start_date,
        "rvend": end_date,
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

def save_revisions_to_csv(revisions, article_title):
    if len(revisions) < 50:
        print(f"Skipping {article_title} due to insufficient revisions (< 50).")
        return

    revision_data = []
    for i in range(len(revisions)):
        prev_size = revisions[i+1].get("size", 0) if i < len(revisions)-1 else 0
        curr_size = revisions[i].get("size", 0)
        revision_data.append({
            "Date": revisions[i]["timestamp"][:10],
            "Time": revisions[i]["timestamp"],
            "User": revisions[i].get("user", "Unknown"),
            "Size": curr_size,
            "Changes": curr_size - prev_size,
            "Comment": revisions[i].get("comment", "No comment"),
            "Tags": ", ".join(revisions[i].get("tags", [])) if revisions[i].get("tags") else "None"
        })

    # Create directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "UK_Politicians")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, f"{article_title}_revisions.csv")
    df = pd.DataFrame(revision_data)
    df.to_csv(file_path, index=False)
    print(f"Saved revisions for '{article_title}' to '{file_path}'")

def main():
    # Find all CSV files starting with representatives_
    csv_files = glob.glob("mps_*.csv")

    # If no such files found, just return
    if not csv_files:
        print("No CSV files found matching 'representatives_*.csv'. Exiting.")
        return

    # Read and concatenate all CSVs into a single DataFrame
    all_df = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)

    # Extract unique wiki_tags
    unique_wiki_tags = all_df["wiki_tag"].unique()

    print(f"Found {len(unique_wiki_tags)} unique politicians to fetch.")

    # Fetch revisions for each unique politician
    for wiki_tag in unique_wiki_tags:
        print(f"Fetching revisions for {wiki_tag} (en.wikipedia.org)...")
        revisions = fetch_revisions(wiki_tag, lang="en")
        save_revisions_to_csv(revisions, wiki_tag)

if __name__ == "__main__":
    main()
