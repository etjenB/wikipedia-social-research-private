import requests
import pandas as pd
import os

# Funktion, um alle Revisionen zu sammeln
def fetch_revisions(title):
    url = "https://de.wikipedia.org/w/api.php"
    params = {
    "action": "query",
    "format": "json",
    "prop": "revisions",
    "titles": title,
    "rvlimit": "max",  # Maximale Anzahl Revisionen pro Anfrage
    "rvprop": "timestamp|size|user|tags|comment",  # Wir brauchen Zeitstempel und Größe der Revision
    "continue": ""
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
        
        # Weiter paginieren, falls mehr Ergebnisse vorhanden sind
        if "continue" in data:
            params.update(data["continue"])
        else:
            break
    
    return all_revisions

def save_wiki_revisions(article_title):
    # Daten holen
    revisions = fetch_revisions(article_title)

    revision_data = []  # Hier speichern wir alle Details
    
    for i in range(0, len(revisions)):
        
        if i == len(revisions)-1:
            prev_size = 0
        else:
            prev_size = revisions[i + 1].get("size", 0)
        curr_size = revisions[i].get("size", 0)
        timestamp = revisions[i]["timestamp"][:10]  # Nur das Datum (YYYY-MM-DD)
        
        # Revision Details speichern
        revision_data.append({
            "Date": revisions[i]["timestamp"][:10],
            "Time": revisions[i]["timestamp"],
            "User": revisions[i].get("user", "Unknown"),
            "Size": curr_size,
            "changes": (curr_size - prev_size),
            "Comment": revisions[i].get("comment", "No comment"),
            "Tags": ", ".join(revisions[i].get("tags", [])) if revisions[i].get("tags") else "None"
        })

    # Revision Details speichern
    revision_df = pd.DataFrame(revision_data)
    # current dir
    current_dir = os.getcwd()
    filename = f"{article_title}_revisions.csv"
    file_path = os.path.join(current_dir, filename)
    revision_df.to_csv(file_path)
    print(f"Alle Revisionen gespeichert in '{file_path}_revisions.csv'")

data = save_wiki_revisions('Alexander_Thumfart')