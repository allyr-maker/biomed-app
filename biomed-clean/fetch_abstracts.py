# string -> file
# fetch abstracts from PubMed

from Bio import Entrez
import pandas as pd

Entrez.email = "allysonrichard39@gmail.com"  # required by NCBI

def search_pubmed(query, max_results=10):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]

def fetch_abstracts(id_list):
    ids = ",".join(id_list)
    handle = Entrez.efetch(db="pubmed", id=ids, rettype="abstract", retmode="text")
    data = handle.read()
    return data

if __name__ == "__main__":
    query = "breast cancer gene expression"
    ids = search_pubmed(query)
    abstracts = fetch_abstracts(ids)
    print(abstracts)

# save abstracts to a text file
with open("abstracts.txt", "w", encoding="utf-8") as f:
    f.write(abstracts)