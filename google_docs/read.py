def read():
    """ It will read from both company files and return a list of unique companies."""
    from pathlib import Path

    script_path = Path(__file__).resolve().parent
    companies_file = script_path.parent / "companies.csv"
    companies_owned_file = script_path.parent / "companies_owned.csv"
    list_of_companies = []

    # Read from companies.csv
    if companies_file.exists():
        with open(companies_file, "r") as fhand:
            lines = fhand.readlines()
            for lin in lines:
                list_of_companies.extend(lin.strip().split(","))

    # Read from companies_owned.csv
    if companies_owned_file.exists():
        with open(companies_owned_file, "r") as fhand:
            lines = fhand.readlines()
            for lin in lines:
                list_of_companies.extend(lin.strip().split(","))

    print(list_of_companies)
    return list(set(list_of_companies))
if __name__ == "__main__":
    read()
