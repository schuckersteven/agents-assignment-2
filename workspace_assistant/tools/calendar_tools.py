"""
Option A: Calendar Assistant Tools

Implement at least 3 tools for Google Calendar operations.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from tools.auth import get_calendar_service


def _parse_datetime(value: Optional[str]) -> datetime:
    """Parse an ISO 8601 datetime string into a timezone-aware datetime."""
    if not value:
        return datetime.now(timezone.utc)

    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Datetime must be provided as an ISO 8601 string.") from exc


def list_upcoming_events(max_results: int = 10) -> dict:
    """List upcoming calendar events.

    Args:
        max_results: Maximum number of events to return.

    Returns:
        dict with 'status' and 'events' keys.
    """
    try:
        service = get_calendar_service()
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return {"status": "success", "events": events_result.get("items", [])}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def find_available_slots(
    duration_minutes: int = 60, days_ahead: int = 7, start_from: Optional[str] = None
) -> dict:
    """Find open calendar slots for a meeting within the next N days.

    Args:
        duration_minutes: Length of the requested meeting in minutes.
        days_ahead: Number of days to search ahead from the start time.
        start_from: Optional ISO 8601 datetime to begin searching from.

    Returns:
        dict with 'status' and a list of available slots.
    """
    try:
        if duration_minutes <= 0:
            raise ValueError("duration_minutes must be greater than 0")
        if days_ahead <= 0:
            raise ValueError("days_ahead must be greater than 0")

        service = get_calendar_service()
        start_dt = _parse_datetime(start_from)
        end_dt = start_dt + timedelta(days=days_ahead)

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_dt.isoformat(),
                timeMax=end_dt.isoformat(),
                singleEvents=True,
                orderBy="startTime",
                maxResults=50,
            )
            .execute()
        )

        events = events_result.get("items", [])
        busy_intervals = []
        for event in events:
            start = event.get("start", {}).get("dateTime") or event.get(
                "start", {}
            ).get("date")
            end = event.get("end", {}).get("dateTime") or event.get("end", {}).get(
                "date"
            )
            if not start or not end:
                continue
            try:
                busy_start = _parse_datetime(start)
                busy_end = _parse_datetime(end)
            except ValueError:
                continue
            busy_intervals.append((busy_start, busy_end))

        slots = []
        current = start_dt
        increment = timedelta(minutes=30)
        while current + timedelta(minutes=duration_minutes) <= end_dt:
            slot_end = current + timedelta(minutes=duration_minutes)
            is_free = True
            for busy_start, busy_end in busy_intervals:
                if current < busy_end and slot_end > busy_start:
                    is_free = False
                    break
            if is_free:
                slots.append(
                    {
                        "start": current.isoformat(),
                        "end": slot_end.isoformat(),
                    }
                )
            current += increment

        return {"status": "success", "slots": slots}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def create_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: Optional[str] = None,
    location: Optional[str] = None,
) -> dict:
    """Create a calendar event with the provided details.

    Args:
        summary: Title of the event.
        start_time: ISO 8601 start datetime for the event.
        end_time: ISO 8601 end datetime for the event.
        description: Optional event description.
        location: Optional event location.

    Returns:
        dict with 'status' and the created event data.
    """
    try:
        if not summary or not summary.strip():
            raise ValueError("summary is required")

        start_dt = _parse_datetime(start_time)
        end_dt = _parse_datetime(end_time)
        if end_dt <= start_dt:
            raise ValueError("end_time must be after start_time")

        service = get_calendar_service()
        event_body = {
            "summary": summary,
            "start": {"dateTime": start_dt.isoformat(), "timeZone": "UTC"},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": "UTC"},
        }
        if description:
            event_body["description"] = description
        if location:
            event_body["location"] = location

        created_event = (
            service.events().insert(calendarId="primary", body=event_body).execute()
        )
        return {"status": "success", "event": created_event}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def check_conflicts(start_time: str, end_time: str, max_results: int = 10) -> dict:
    """Check whether a proposed time range conflicts with existing calendar events.

    Args:
        start_time: ISO 8601 start datetime for the proposed meeting.
        end_time: ISO 8601 end datetime for the proposed meeting.
        max_results: Maximum number of events to inspect.

    Returns:
        dict with 'status', 'conflicts', and 'has_conflicts' keys.
    """
    try:
        start_dt = _parse_datetime(start_time)
        end_dt = _parse_datetime(end_time)
        if end_dt <= start_dt:
            raise ValueError("end_time must be after start_time")

        service = get_calendar_service()
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_dt.isoformat(),
                timeMax=end_dt.isoformat(),
                singleEvents=True,
                orderBy="startTime",
                maxResults=max_results,
            )
            .execute()
        )

        conflicts = []
        for event in events_result.get("items", []):
            event_start = event.get("start", {}).get("dateTime") or event.get(
                "start", {}
            ).get("date")
            event_end = event.get("end", {}).get("dateTime") or event.get(
                "end", {}
            ).get("date")
            if not event_start or not event_end:
                continue
            try:
                event_start_dt = _parse_datetime(event_start)
                event_end_dt = _parse_datetime(event_end)
            except ValueError:
                continue
            if start_dt < event_end_dt and end_dt > event_start_dt:
                conflicts.append(event)

        return {
            "status": "success",
            "has_conflicts": bool(conflicts),
            "conflicts": conflicts,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


calendar_tools = [
    list_upcoming_events,
    find_available_slots,
    create_event,
    check_conflicts,
]
