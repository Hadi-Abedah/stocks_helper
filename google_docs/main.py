from . import read, write, nxt_ear, clean, populate_companies
from datetime import datetime
import re


def extract_date_from_line(line):
    try:
        match = re.search(r"is:\s*([\d]{4}-[\d]{2}-[\d]{2})", line)
        if match:
            return datetime.strptime(match.group(1), "%Y-%m-%d")
        else:
            raise ValueError("No date found in line.")
    except Exception:
        print(f"Warning: Invalid or missing date in line: {line.strip()}")
        return datetime.max




def main():
    '''Write the next earnings dates to a file and google docs
        the file is dates.json will be by alerts/calendar/main.py to create or modify calendar events.   
    '''
    # remove previously added info.
    clean.clean()
    # poulate the companies_owned file with companies owned shares
    populate_companies.populate_companies_file()
    list_of_companies = read.read()
    lines_to_be_written = []
    json_to_be_written = {}

    for company in list_of_companies:
        ticker, date, eps, revenue = nxt_ear.get_next_earnings_date(company)
        if date:
            json_data = {ticker: str(date)} 
            json_to_be_written.update(json_data)
        line_to_be_written = f"The next expected financial statement date for {ticker.upper()} is: {date}. The average EPS is: {eps}, with an average Revenue of {revenue} million dollars\n"
        lines_to_be_written.append(line_to_be_written)
        
    # Write the JSON data to dates.json
    with open("dates.json", "w") as f:
        import json
        json.dump(json_to_be_written, f, indent=4)

    # Sort the lines based on the date extracted
    ordered_lines_by_date = sorted(lines_to_be_written, key=extract_date_from_line, reverse=True)
    
    # Write the sorted lines
    for line in ordered_lines_by_date:
        write.write(line)

if __name__ == '__main__':
    main()
    print("the main body is executed.")