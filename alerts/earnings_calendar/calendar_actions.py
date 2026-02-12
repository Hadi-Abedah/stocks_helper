# calendar_reminders.py
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Iterable, Optional, Dict, Any, List
import os
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
DEFAULT_CALENDAR_ID = "primary"
DEFAULT_TZ = "Asia/Nicosia"  # adjust if you prefer

# ---------- Auth / Service ----------


import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(BASE_DIR, "credentials.json")
token_path = os.path.join(BASE_DIR, "token.json")

def _get_service(
    scopes: List[str] = SCOPES,
    credentials_path: str = credentials_path,
    token_path: str = token_path,
):
    """
    Returns an authenticated Google Calendar service client.
    First run opens a browser for consent and saves token.json.
    """
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Lazy import to avoid heavy deps at import time
            from google.auth.transport.requests import Request
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


# ---------- Helpers ----------

def _rfc3339(dt: datetime) -> str:
    """
    Ensure an aware datetime → RFC3339 string with timezone offset.
    """
    if dt.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")
    return dt.isoformat()

def _event_time_payload(
    start_dt: Optional[datetime] = None,
    end_dt: Optional[datetime] = None,
    all_day_date: Optional[str] = None,
    tz: str = DEFAULT_TZ,
) -> Dict[str, Any]:
    """
    Build the 'start' and 'end' payload for an event.
    - Timed event: provide start_dt and end_dt (aware datetimes).
    - All-day: provide all_day_date = 'YYYY-MM-DD' (end is exclusive).
    """
    if all_day_date:
        # For all-day, end.date is the next day (exclusive)
        from datetime import date
        d = datetime.strptime(all_day_date, "%Y-%m-%d").date()
        end_date = (d + timedelta(days=1)).isoformat()
        return {
            "start": {"date": d.isoformat(), "timeZone": tz},
            "end": {"date": end_date, "timeZone": tz},
        }
    if not (start_dt and end_dt):
        raise ValueError("Provide either (start_dt, end_dt) or all_day_date")
    return {
        "start": {"dateTime": _rfc3339(start_dt), "timeZone": tz},
        "end": {"dateTime": _rfc3339(end_dt), "timeZone": tz},
    }

def _reminders_payload(
    minutes_list: Iterable[int] = (10,),
    email_minutes_list: Iterable[int] = (),
) -> Dict[str, Any]:
    """
    Build reminders overrides:
      - popup → device/app notifications
      - email → email reminders
    """
    overrides = [{"method": "popup", "minutes": m} for m in minutes_list]
    overrides += [{"method": "email", "minutes": m} for m in email_minutes_list]
    return {"useDefault": False, "overrides": overrides}


# ---------- CRUD ----------

def create_event(
    summary: str,
    description: Optional[str] = None,
    start_dt: Optional[datetime] = None,
    end_dt: Optional[datetime] = None,
    all_day_date: Optional[str] = None,
    tz: str = DEFAULT_TZ,
    reminder_minutes: Iterable[int] = (10,),
    email_reminder_minutes: Iterable[int] = (),
    location: Optional[str] = None,
    recurrence_rrules: Optional[List[str]] = None,
    calendar_id: str = DEFAULT_CALENDAR_ID,
    transparency: Optional[str] = None,  # "opaque" or "transparent"
    guests: Optional[Iterable] = None,   # Iterable[str] or Iterable[dict] like {"email": "...", ...}
) -> Dict[str, Any]:
    """
    Create an event (timed or all-day) with reminders and optional guests.
    guests may be an iterable of email strings or attendee dicts (e.g. {"email": "a@b.com", "displayName": "A"}).
    Returns the created event resource (includes 'id' and 'htmlLink').
    """
    service = _get_service()
    body = {
        "summary": summary,
        "description": description or "",
        **_event_time_payload(start_dt, end_dt, all_day_date, tz),
        "reminders": _reminders_payload(reminder_minutes, email_reminder_minutes),
    }

    if guests:
        attendees: List[Dict[str, Any]] = []
        for g in guests:
            if isinstance(g, str):
                attendees.append({"email": g})
            elif isinstance(g, dict) and "email" in g:
                attendees.append(g)
            else:
                raise ValueError("guests must be iterable of email strings or attendee dicts with an 'email' key")
        body["attendees"] = attendees

    if location:
        body["location"] = location
    if recurrence_rrules:
        # Example: ["RRULE:FREQ=DAILY;COUNT=5"] or ["RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR"]
        body["recurrence"] = recurrence_rrules
    if transparency in ("opaque", "transparent"):
        body["transparency"] = transparency

    try:
        created = service.events().insert(calendarId=calendar_id, body=body).execute()
        return created
    except HttpError as e:
        raise RuntimeError(f"Calendar insert failed: {e}")

def list_upcoming(
    max_results: int = 10,
    time_min: Optional[datetime] = None,
    calendar_id: str = DEFAULT_CALENDAR_ID,
    q: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    List upcoming events (default: now → future), optionally filtered by search query q.
    """
    service = _get_service()
    if time_min is None:
        time_min = datetime.now(timezone.utc)
    try:
        resp = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=_rfc3339(time_min),
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
                q=q,
            )
            .execute()
        )
        return resp.get("items", [])
    except HttpError as e:
        raise RuntimeError(f"Calendar list failed: {e}")


def update_event(
    event_id: str,
    updates: Dict[str, Any],
    calendar_id: str = DEFAULT_CALENDAR_ID,
) -> Dict[str, Any]:
    """
    Patch an existing event with partial updates (e.g., change time, reminders, summary).
    Example updates:
      {"summary": "New title"}
      {"start": {...}, "end": {...}}
      {"reminders": _reminders_payload([5, 30])}
    """
    service = _get_service()
    try:
        updated = (
            service.events()
            .patch(calendarId=calendar_id, eventId=event_id, body=updates)
            .execute()
        )
        return updated
    except HttpError as e:
        raise RuntimeError(f"Calendar patch failed: {e}")


def delete_event(event_id: str, calendar_id: str = DEFAULT_CALENDAR_ID) -> None:
    """
    Delete an event by ID.
    """
    service = _get_service()
    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    except HttpError as e:
        raise RuntimeError(f"Calendar delete failed: {e}")


# ---------- Convenience builders ----------

def build_timed_event_updates(
    start_dt: datetime,
    end_dt: datetime,
    tz: str = DEFAULT_TZ,
) -> Dict[str, Any]:
    """Handy helper to build 'start'/'end' patch payload."""
    return _event_time_payload(start_dt, end_dt, None, tz)

def build_all_day_updates(all_day_date: str, tz: str = DEFAULT_TZ) -> Dict[str, Any]:
    """Handy helper to switch an event into an all-day entry."""
    return _event_time_payload(None, None, all_day_date, tz)

def build_rrule(
    freq: str,
    interval: Optional[int] = None,
    count: Optional[int] = None,
    until: Optional[datetime] = None,
    byday: Optional[Iterable[str]] = None,
    bymonthday: Optional[Iterable[int]] = None,
) -> str:
    """
    Compose an RRULE string. e.g.,
      build_rrule("WEEKLY", byday=["MO","WE","FR"])
      build_rrule("DAILY", count=10)
      build_rrule("MONTHLY", bymonthday=[1], interval=1)
    """
    parts = [f"FREQ={freq.upper()}"]
    if interval:
        parts.append(f"INTERVAL={interval}")
    if count:
        parts.append(f"COUNT={count}")
    if until:
        # UNTIL MUST be in UTC in YYYYMMDDTHHMMSSZ form (Calendar is lenient, but this is standard)
        until_utc = until.astimezone(timezone.utc)
        parts.append("UNTIL=" + until_utc.strftime("%Y%m%dT%H%M%SZ"))
    if byday:
        parts.append("BYDAY=" + ",".join(byday))
    if bymonthday:
        parts.append("BYMONTHDAY=" + ",".join(str(d) for d in bymonthday))
    return "RRULE:" + ";".join(parts)
