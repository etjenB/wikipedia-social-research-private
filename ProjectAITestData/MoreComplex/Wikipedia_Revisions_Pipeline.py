import requests
import pandas as pd
import os
from datetime import datetime

# Function to fetch revisions for a single article
def fetch_revisions(title, lang="en", start_date=None, end_date=None):
    url = f"https://{lang}.wikipedia.org/w/api.php"  # Use language-specific Wikipedia
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

# Function to save revisions to CSV
def save_revisions_to_csv(revisions, article_title, country):
    if len(revisions) < 50:
        print(f"Skipping {article_title} ({country}) due to insufficient revisions (< 50).")
        return  # Skip saving if less than 50 revisions

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
        for article, lang in articles:
            print(f"Fetching revisions for {article} ({country}) from {lang}.wikipedia.org...")
            revisions = fetch_revisions(article, lang)
            save_revisions_to_csv(revisions, article, country)

if __name__ == "__main__":
    # Expanded list of countries and their politicians
    politicians = {
        "Germany": [
            ("Angela_Merkel", "de"), ("Olaf_Scholz", "de"), ("Annalena_Baerbock", "de"),
            ("Christian_Lindner", "de"), ("Friedrich_Merz", "de"), ("Robert_Habeck", "de"),
            ("Wolfgang_Schäuble", "de"), ("Horst_Seehofer", "de"), ("Sigmar_Gabriel", "de"),
            ("Jens_Spahn", "de"), ("Ursula_von_der_Leyen", "de"), ("Alice_Weidel", "de"),
            ("Alexander_Gauland", "de"), ("Gregor_Gysi", "de"), ("Sahra_Wagenknecht", "de"),
            ("Markus_Söder", "de"), ("Armin_Laschet", "de"), ("Katrin_Göring-Eckardt", "de"),
            ("Norbert_Röttgen", "de"), ("Karl_Lauterbach", "de"), ("Annette_Schavan", "de"),
            ("Peter_Altmaier", "de"), ("Thomas_de_Maizière", "de"), ("Andrea_Nahles", "de"),
            ("Heiko_Maas", "de"), ("Renate_Künast", "de"), ("Klaus_Wowereit", "de"),
            ("Bärbel_Bas", "de"), ("Nils_Schmid", "de"), ("Ralf_Stegner", "de")
        ],
        "USA": [
            ("Joe_Biden", "en"), ("Donald_Trump", "en"), ("Kamala_Harris", "en"),
            ("Barack_Obama", "en"), ("Hillary_Clinton", "en"), ("Nancy_Pelosi", "en"),
            ("Mitch_McConnell", "en"), ("Ron_DeSantis", "en"), ("Alexandria_Ocasio-Cortez", "en"),
            ("Elizabeth_Warren", "en"), ("Ted_Cruz", "en"), ("Mike_Pence", "en"),
            ("Kevin_McCarthy", "en"), ("Bernie_Sanders", "en"), ("Amy_Klobuchar", "en"),
            ("Pete_Buttigieg", "en"), ("Chuck_Schumer", "en"), ("Lindsey_Graham", "en"),
            ("Marco_Rubio", "en"), ("Gavin_Newsom", "en"), ("Andrew_Yang", "en"),
            ("Tulsi_Gabbard", "en"), ("Beto_O'Rourke", "en"), ("Cory_Booker", "en"),
            ("George_W._Bush", "en"), ("Dick_Cheney", "en"), ("Condoleezza_Rice", "en"),
            ("Al_Gore", "en"), ("John_Kerry", "en"), ("Sarah_Palin", "en")
        ],
        "UK": [
            ("Rishi_Sunak", "en"), ("Boris_Johnson", "en"), ("Theresa_May", "en"),
            ("Keir_Starmer", "en"), ("Nicola_Sturgeon", "en"), ("Jeremy_Corbyn", "en"),
            ("David_Cameron", "en"), ("Ed_Miliband", "en"), ("Tony_Blair", "en"),
            ("Gordon_Brown", "en"), ("Michael_Gove", "en"), ("Priti_Patel", "en"),
            ("Sajid_Javid", "en"), ("Matt_Hancock", "en"), ("Liz_Truss", "en"),
            ("Nadine_Dorries", "en"), ("Amber_Rudd", "en"), ("Dominic_Raab", "en"),
            ("Rory_Stewart", "en"), ("Jacob_Rees-Mogg", "en"), ("Jo_Swinson", "en"),
            ("Caroline_Lucas", "en"), ("Ian_Blackford", "en"), ("John_McDonnell", "en"),
            ("Harriet_Harman", "en"), ("Ken_Clarke", "en"), ("Margaret_Thatcher", "en"),
            ("Nigel_Farage", "en"), ("Vince_Cable", "en"), ("Alistair_Darling", "en")
        ],
        "France": [
            ("Emmanuel_Macron", "fr"), ("Marine_Le_Pen", "fr"), ("Jean-Luc_Mélenchon", "fr"),
            ("François_Hollande", "fr"), ("Nicolas_Sarkozy", "fr"), ("Édouard_Philippe", "fr"),
            ("Ségolène_Royal", "fr"), ("Alain_Juppé", "fr"), ("François_Bayrou", "fr"),
            ("Xavier_Bertrand", "fr"), ("Arnaud_Montebourg", "fr"), ("Manuel_Valls", "fr"),
            ("Bruno_Le_Maire", "fr"), ("Jean-Pierre_Raffarin", "fr"), ("Laurent_Wauquiez", "fr"),
            ("Christine_Lagarde", "fr"), ("Nathalie_Kosciusko-Morizet", "fr"), ("Anne_Hidalgo", "fr"),
            ("Jean-François_Copé", "fr"), ("Dominique_de_Villepin", "fr"), ("Dominique_Strauss-Kahn", "fr"),
            ("Philippe_Martinez", "fr"), ("Hervé_Morin", "fr"), ("Jean-Yves_Le_Drian", "fr"),
            ("Marisol_Touraine", "fr"), ("Michel_Barnier", "fr"), ("Patrick_Balkany", "fr"),
            ("Rachida_Dati", "fr"), ("Claude_Guéant", "fr"), ("Éric_Zemmour", "fr")
        ],
        "India": [
            ("Narendra_Modi", "en"), ("Rahul_Gandhi", "en"), ("Amit_Shah", "en"),
            ("Sonia_Gandhi", "en"), ("Manmohan_Singh", "en"), ("Yogi_Adityanath", "en"),
            ("Arvind_Kejriwal", "en"), ("Pranab_Mukherjee", "en"), ("Sushma_Swaraj", "en"),
            ("Atal_Bihari_Vajpayee", "en"), ("Mamata_Banerjee", "en"), ("Lalu_Prasad_Yadav", "en"),
            ("Nitish_Kumar", "en"), ("Sharad_Pawar", "en"), ("Mayawati", "en"),
            ("Jayalalithaa", "en"), ("Karunanidhi", "en"), ("Jyotiraditya_Scindia", "en"),
            ("Shashi_Tharoor", "en"), ("Piyush_Goyal", "en"), ("Nitin_Gadkari", "en"),
            ("Smriti_Irani", "en"), ("Rajnath_Singh", "en"), ("Venkaiah_Naidu", "en"),
            ("Vajubhai_Vala", "en"), ("Bhupendra_Patel", "en"), ("Devendra_Fadnavis", "en"),
            ("Ashok_Gehlot", "en"), ("Chandrababu_Naidu", "en"), ("K._Chandrashekar_Rao", "en")
        ],
        "Japan": [
            ("Fumio_Kishida", "ja"), ("Shinzo_Abe", "ja"), ("Yoshihide_Suga", "ja"),
            ("Taro_Aso", "ja"), ("Yuriko_Koike", "ja"), ("Shigeru_Ishiba", "ja"),
            ("Naoto_Kan", "ja"), ("Yukio_Hatoyama", "ja"), ("Junichiro_Koizumi", "ja"),
            ("Nobuteru_Ishihara", "ja"), ("Seiko_Noda", "ja"), ("Toshimitsu_Motegi", "ja"),
            ("Tetsuro_Fukuyama", "ja"), ("Akira_Amari", "ja"), ("Tadamori_Oshima", "ja"),
            ("Ichiro_Ozawa", "ja"), ("Katsuya_Okada", "ja"), ("Shinjiro_Koizumi", "ja"),
            ("Makiko_Tanaka", "ja"), ("Yasuo_Fukuda", "ja"), ("Shintaro_Ishihara", "ja"),
            ("Takeshi_Noda", "ja"), ("Keizo_Obuchi", "ja"), ("Tomomi_Inada", "ja"),
            ("Hiromi_Takatsuka", "ja"), ("Taro_Kono", "ja"), ("Koichi_Hagino", "ja"),
            ("Seiji_Maezawa", "ja"), ("Ryutaro_Hashimoto", "ja"), ("Takashi_Shiota", "ja")
        ],
        "Spain": [
            ("Pedro_Sánchez", "es"), ("Mariano_Rajoy", "es"), ("Santiago_Abascal", "es"),
            ("Pablo_Iglesias_Turrión", "es"), ("Inés_Arrimadas", "es"), ("Alberto_Núñez_Feijóo", "es"),
            ("José_Luis_Rodríguez_Zapatero", "es"), ("Felipe_González", "es"), ("Manuela_Carmena", "es"),
            ("Cristina_Cifuentes", "es"), ("Isabel_Díaz_Ayuso", "es"), ("Rosa_Díez", "es"),
            ("Miguel_Arias_Cañete", "es"), ("Esperanza_Aguirre", "es"), ("Ana_Botella", "es"),
            ("José_María_Aznar", "es"), ("Albert_Rivera", "es"), ("Artur_Mas", "es"),
            ("Quim_Torra", "es"), ("Ada_Colau", "es"), ("Carme_Forcadell", "es"),
            ("Oriol_Junqueras", "es"), ("Jordi_Pujol", "es"), ("Pere_Aragonès", "es"),
            ("Enrique_Tierno_Galván", "es"), ("Carles_Puigdemont", "es"), ("José_Bono", "es"),
            ("Javier_Maroto", "es"), ("María_Dolores_de_Cospedal", "es"), ("Soraya_Sáenz_de_Santamaría", "es")
        ],
        "Brazil": [
            ("Luiz_Inácio_Lula_da_Silva", "pt"), ("Jair_Bolsonaro", "pt"), ("Dilma_Rousseff", "pt"),
            ("Fernando_Haddad", "pt"), ("Ciro_Gomes", "pt"), ("Michel_Temer", "pt"),
            ("Aécio_Neves", "pt"), ("Eduardo_Cunha", "pt"), ("Geraldo_Alckmin", "pt"),
            ("Marina_Silva", "pt"), ("José_Serra", "pt"), ("João_Doria", "pt"),
            ("Renan_Calheiros", "pt"), ("Rodrigo_Maia", "pt"), ("Fernando_Henrique_Cardoso", "pt"),
            ("Romário", "pt"), ("Sérgio_Moro", "pt"), ("Alexandre_de_Moraes", "pt"),
            ("Jaques_Wagner", "pt"), ("Tarcísio_de_Freitas", "pt"), ("Flávio_Bolsonaro", "pt"),
            ("Eduardo_Bolsonaro", "pt"), ("Davi_Alcolumbre", "pt"), ("Randolfe_Rodrigues", "pt"),
            ("Humberto_Costa", "pt"), ("José_Dirceu", "pt"), ("Gleisi_Hoffmann", "pt"),
            ("Gilberto_Kassab", "pt"), ("Paulo_Guedes", "pt"), ("Henrique_Meirelles", "pt")
        ]
    }

    # Run the pipeline
    main_pipeline(politicians)