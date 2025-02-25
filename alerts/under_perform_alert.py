

def main():

    import yfinance as yf 
    import pandas as pd 
    from pathlib import Path 
    from percentage_change.daily_perc_chng import compute_daily_prec


    script_dir = Path(__file__).parent
    companies = []
    target_companies = []
    df1 = pd.read_csv(f"{script_dir}/nasdaq_screener_1724268381610.csv")
    df2 = pd.read_csv(f"{script_dir}/nasdaq_screener_1724268475973.csv")
    companies = df1["Symbol"].tolist() + df2["Symbol"].tolist()
    print(f"there are {len(companies)} companies in my list.")
    
    for comp in companies[:]:
        perc_chng = compute_daily_prec(comp)
        try:
            perc_value = float(str(perc_chng).strip("%"))
            print(perc_value)
            if perc_value <= -6:
                target_companies.append(comp)
        except ValueError: 
            pass

    # the alert part
    print(target_companies)

if __name__ == "__main__":
    #target_perc = float(input("Enter Your daily percentahe target, example: 0.5: "))
    main()
