from snaptrade.snaptrade_api import list_account_holdings 


def populate_companies_file(): 
    """ This function would populate a companies.csv with my current holdings."""

    import csv
    lst_of_companies = list_account_holdings()
    with open("companies_owned.csv", "w") as fhand:
        write = csv.writer(fhand)
        write.writerow(lst_of_companies)

if __name__ == "__main__":
    populate_companies_file()
    print("the main body is executed.")