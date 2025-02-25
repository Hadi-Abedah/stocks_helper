from . import read, write, nxt_ear, clean
from datetime import datetime


def extract_date_from_line(line):
    ''' Helper function to sort the earnings report by date before writing them.'''
    try:
        date_str = line.split("is: ")[-1]
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        print(f"Warning: Invalid date format encountered in line: {line.strip()}")
        # Return a date far in the past for invalid dates so they are sorted last
        return datetime.max




def main():
    # remove previously added info.
    clean.clean()
    list_of_companies = read.read()
    lines_to_be_written = []

    for company in list_of_companies:
        line_to_be_written = nxt_ear.get_next_earnings_date(company)
        lines_to_be_written.append(line_to_be_written)

    # Sort the lines based on the date extracted
    ordered_lines_by_date = sorted(lines_to_be_written, key=extract_date_from_line, reverse=True)
    
    # Write the sorted lines
    for line in ordered_lines_by_date:
        write.write(line)

if __name__ == '__main__':
    main()
    print("the main body is executed.")