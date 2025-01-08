import os
import pandas as pd
import time
import requests

input_dir = "Germany_Austria_data"
output_dir = "Revisions"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def fetch_revisions(title):
    url = "https://de.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": title,
        "rvlimit": "max",
        "rvprop": "timestamp|size|user|tags|comment",
        "continue": ""
    }
    all_revisions = []
    session = requests.Session()
    try:
        while True:
            response = session.get(url, params=params)
            data = response.json()
            
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                if page_id == "-1":  # Invalid or non-existent page
                    print(f"Invalid or non-existent page: {title}")
                    return []
                revisions = page_data.get("revisions", [])
                all_revisions.extend(revisions)
            
            if "continue" in data:
                params.update(data["continue"])
            else:
                break
    except Exception as e:
        print(f"Error fetching revisions for {title}: {e}")
    return all_revisions

def save_wiki_revisions(article_title):
    try:
        revisions = fetch_revisions(article_title)
        if not revisions:
            print(f"No revisions fetched for: {article_title}")
            return
        
        revision_data = []
        for i in range(len(revisions)):
            prev_size = revisions[i + 1].get("size", 0) if i < len(revisions) - 1 else 0
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

        # Sanitize the filename to avoid invalid characters
        sanitized_title = article_title.replace("?", "").replace(":", "").replace("/", "").replace("\\", "").replace("&", "and")
        output_file = os.path.join(output_dir, f"{sanitized_title}_revisions.csv")
        pd.DataFrame(revision_data).to_csv(output_file, index=False)
        print(f"Revisions saved to '{output_file}'")
    except Exception as e:
        print(f"Error saving revisions for {article_title}: {e}")

def main():
    for csv_file in os.listdir(input_dir):
        if csv_file.endswith(".csv"):
            input_file = os.path.join(input_dir, csv_file)
            print(f"Processing file: {input_file}")
            
            try:
                df = pd.read_csv(input_file)
            except Exception as e:
                print(f"Error reading file {input_file}: {e}")
                continue

            for link in df.get('link', []):
                try:
                    article_title = link.split('/')[-1]
                    print(f"Fetching revisions for: {article_title}")
                    save_wiki_revisions(article_title)
                    time.sleep(1)
                except Exception as e:
                    print(f"Error processing link {link}: {e}")

if __name__ == "__main__":
    main()
