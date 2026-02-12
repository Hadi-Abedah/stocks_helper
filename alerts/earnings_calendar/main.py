import json
from pathlib import Path
from alerts.earnings_calendar.calendar_actions import create_event, update_event, delete_event, DEFAULT_TZ, DEFAULT_CALENDAR_ID
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo  
from stock_actions.watch_list.main import read as read_watch_list
from stock_actions.earnings import nxt_ear
TZ = ZoneInfo(DEFAULT_TZ)

def _parse_local_window(date_str: str):
    """Return (start_dt, end_dt) as tz-aware datetimes in DEFAULT_TZ.
       Start at 09:00 local, end at 10:00 local on the same day."""
    day = datetime.fromisoformat(date_str).date()
    start = datetime.combine(day, datetime.min.time()).replace(tzinfo=TZ) + timedelta(hours=9)
    end   = start + timedelta(hours=1)
    return start, end

def main() -> None:
    """Compare dates.json with calendar_dates.json; create/update Google Calendar events as needed.
    dates.json file format: { "TICKER": "YYYY-MM-DD", ... } (mirror of upstream earnings data)
    calendar_dates.json file format: { "TICKER": { "YYYY-MM-DD": "event_id" }, ... } (mirror of calendar state)
    1. For each TICKER in dates.json:
       a. If TICKER not in calendar_dates.json, create event and add to calendar_dates.json.
       b. If TICKER in calendar_dates.json, compare dates:
          i. If dates differ and stored date is in the future, update event date.
          ii. If dates differ and stored date is in the past, create new event.
    2. Save updated calendar_dates.json.
    """
    # the script dir path 
    file_path = Path(__file__).resolve().parent
    # update dates.json with the latest earnings dates
    list_of_companies = read_watch_list() 
    json_to_be_written = {}
    for company in list_of_companies:
        ticker, date, eps, revenue = nxt_ear.get_next_earnings_date(company)
        if date:
            print("adta ")
            json_data = {ticker: str(date)} 
            json_to_be_written.update(json_data)
    with open(file_path / "dates.json", "w") as f:
        json.dump(json_to_be_written, f, indent=4)
    # Load upstream dates: { "TICKER": "YYYY-MM-DD", ... }
    with open(file_path / "dates.json", "r") as f:
        dates: Dict[str, str] = json.load(f)

    # Load or initialize calendar mirror: { "TICKER": { "YYYY-MM-DD": "event_id" } }
    try:
        with open(file_path / "calendar_dates.json", "r") as f:
            calendar_dates: Dict[str, Dict[str, str]] = json.load(f)
    except FileNotFoundError:
        calendar_dates = {}
        with open(file_path / "calendar_dates.json", "w") as f:
            json.dump(calendar_dates, f, indent=4)

    changes_to_calendar_dates = {}
    for stock, date_str in dates.items():
        if not date_str:
            continue  # skip None/empty
        start_dt, end_dt = _parse_local_window(date_str)

        if stock not in calendar_dates:
            # we have not recoreded any event for this stock yet: create it
            event = create_event(
                summary=f"{stock} Earnings Call",
                start_dt=start_dt,
                end_dt=end_dt,
                tz=DEFAULT_TZ,
                reminder_minutes=[
                    60*24*5,  # 5 days
                    60*24*2,  # 2 days
                    60*24*1,  # 1 day
                ],
                calendar_id=DEFAULT_CALENDAR_ID,
                guests=["cyberpenguinization@gmail.com"]
            )
            changes_to_calendar_dates[stock] ={ date_str : event["id"] }
            #calendar_dates[stock] = {date_str: event["id"]}
            print(f"Created event for {stock}")
            

        else:
            # we have an existing event for this stock; check if date changed
            assert len(calendar_dates[stock]) == 1, "Expected exactly one date per stock in calendar_dates.json"
            stored_date_str = next(iter(calendar_dates[stock].keys()))
            stored_date = datetime.fromisoformat(stored_date_str).date()
            # compare dates
            if stored_date_str != date_str: 
                # date has changed and it is still in the future
                if stored_date> datetime.today().date():
                    # Event date changed: update existing event
                    existing_event_id = next(iter(calendar_dates[stock].values()))
                    try:
                        event = update_event(
                            event_id=existing_event_id,
                            updates={
                                # If your update_event expects RFC3339 strings instead of datetimes, use start_dt.isoformat()
                                "start": {"dateTime": start_dt.isoformat(), "timeZone": DEFAULT_TZ},
                                "end": {"dateTime": end_dt.isoformat(), "timeZone": DEFAULT_TZ},
                                # optionally: "start": {"timeZone": DEFAULT_TZ}, "end": {"timeZone": DEFAULT_TZ},
                            },
                        )
                    except Exception as e:
                        print(f"Error updating event for {stock}: {e}")
                        continue
                    changes_to_calendar_dates[stock] ={ date_str : event["id"] }
                    #calendar_dates[stock] = {date_str: event["id"]}
                    print(f"Updated event for {stock}")
                elif stored_date < datetime.today().date():
                    # Event has passed, delete entry from calendar_date and  create a new event, old event stays in calendar
                    #delete old entry
                    del calendar_dates[stock]
                    
                    #create new event
                    event = create_event(
                    summary=f"{stock} Earnings Call",
                    start_dt=start_dt,
                    end_dt=end_dt,
                    tz=DEFAULT_TZ,
                    reminder_minutes=[
                        60*24*5,  # 5 days
                        60*24*2,  # 2 days
                        60*24*1,  # 1 day
                    ],
                    calendar_id=DEFAULT_CALENDAR_ID,
                    guests=["cyberpenguinization@gmail.com"]
                    )
                    changes_to_calendar_dates[stock] ={ date_str : event["id"] }
                    #calendar_dates[stock] = {date_str: event["id"]}
                    print(f"Created new event for {stock}")

  
    calendar_dates.update(changes_to_calendar_dates)

    # Persist mirror
    with open(file_path /"calendar_dates.json", "w") as f:
        json.dump(calendar_dates, f, indent=4)
    print("Calendar sync complete.", datetime.now().isoformat())
if __name__ == "__main__":
    main()
