def read():
    """
    This function reads the companies.csv and companies_owned.csv files and returns a list of unique companies.
    It first populates the companies_owned.csv file then reads both files and combines the companies into a single list, removing duplicates.
    """
    from pathlib import Path
    from . import populate_owned

    # First populate the companies_owned.csv file with the current holdings
    populate_owned.populate_companies_file()

    script_path = Path(__file__).resolve().parent
    # files live in the same `watch_list` directory
    companies_file = script_path / "companies.csv"
    companies_owned_file = script_path / "companies_owned.csv"
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