"""
Download DrungCombDB data
"""

import requests
import os


def download_file(dir, url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(os.path.join(dir, local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


if __name__ == '__main__':
    print("Downloading DrugComb data, it can take a while...")
    if not os.path.exists("Data/DrugComb"):
        os.makedirs("Data/DrugComb")
    download_file("Data/DrugComb", "http://drugcombdb.denglab.org/download/drugcombs_scored.csv")
    download_file("Data/DrugComb", "http://drugcombdb.denglab.org/download/drugcombs_response.csv")
    download_file("Data/DrugComb", "http://drugcombdb.denglab.org/download/cell_Line.csv")
    download_file("Data/DrugComb", "http://drugcombdb.denglab.org/download/drug_chemical_info.csv")
    download_file("Data/DrugComb", "http://drugcombdb.denglab.org/download/drug_protein_links.rar")
    download_file("Data/DrugComb", "http://drugcombdb.denglab.org/download/protein_protein_links.rar")

