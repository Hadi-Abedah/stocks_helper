from .fetch_news import check_for_new_news
from pathlib import Path
import pandas as pd


script_dir = Path(__file__).resolve().parent
companies_file = script_dir.parent / "companies.csv"
list_of_companies = [] 
with open(companies_file, "r") as fhand:
    lines = fhand.readlines()
    for lin in lines:
        list_of_companies += lin.strip().split(",")
print(list_of_companies) 

for company in list_of_companies:
    check_for_new_news(f"{company} stock", "https://news.google.com/search")