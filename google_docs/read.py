def read():
    from pathlib import Path
    
    script_path = Path(__file__).resolve().parent
    companies_txt_file = script_path.parent / "companies.csv"
    list_of_companies = []
    with open(companies_txt_file, "r") as fhand:
        lines = fhand.readlines()
        for lin in lines:
            list_of_companies += lin.strip().split(",")
    print(list_of_companies)
    return list_of_companies


if __name__ == "__main__":
    read()