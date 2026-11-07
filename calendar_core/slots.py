"""Tiny day-planning helpers. Times are minutes after midnight (0-1440).

Rules (the contract every change must keep):

* An Event covers the half-open interval [start, end): it includes its start
  minute and excludes its end minute. start < end is required.
* Two events overlap only if they share at least one minute. Back-to-back
  events (one ends exactly when the next starts) do not overlap.
* free_slots(events, day_start, day_end, min_minutes) returns the gaps inside
  [day_start, day_end) not covered by any event, as (start, end) tuples sorted
  by start. Events may arrive in any order and may overlap each other. Only
  gaps of at least min_minutes are returned. Events partly outside the day
  are clipped to it.
* parse_time turns "HH:MM" (24-hour) or 12-hour times like "9am" and
  "2:30pm" into minutes. Anything it cannot parse raises ValueError.
* fmt_duration(minutes) renders "Xh YYm" (e.g. 65 -> "1h 05m", 45 -> "0h 45m").
"""

from __future__ import annotations

import re
from dataclasses import dataclass

MINUTES_PER_DAY = 1440

_12_HOUR_RE = re.compile(r"^(\d{1,2})(?::(\d{2}))?\s*(am|pm)$", re.IGNORECASE)


@dataclass(frozen=True)
class Event:
    start: int
    end: int
    title: str = ""

    def __post_init__(self):
        if not (0 <= self.start < self.end <= MINUTES_PER_DAY):
            raise ValueError(f"bad event times {self.start}-{self.end}")


def parse_time(text: str) -> int:
    """Parse "HH:MM" (24-hour) or 12-hour times like "9am"/"2:30pm" into minutes after midnight."""
    cleaned = text.strip()
    match = _12_HOUR_RE.match(cleaned)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) is not None else 0
        if not (1 <= hour <= 12 and 0 <= minute < 60):
            raise ValueError(f"bad time {text!r}")
        # General conversion: 12 wraps to 0, and the pm half of the day
        # starts twelve hours after the am half.
        is_pm = match.group(3).lower() == "pm"
        hour_24 = hour % 12 + (12 if is_pm else 0)
        return hour_24 * 60 + minute
    try:
        hours, minutes = cleaned.split(":")
        hour, minute = int(hours), int(minutes)
    except ValueError:
        raise ValueError(f"bad time {text!r}") from None
    if not (0 <= hour < 24 and 0 <= minute < 60):
        raise ValueError(f"bad time {text!r}")
    return hour * 60 + minute


def overlaps(a: Event, b: Event) -> bool:
    """True if the two events share at least one minute."""
    return a.start < b.end and b.start < a.end


def free_slots(events: list[Event], day_start: int, day_end: int, min_minutes: int = 1) -> list[tuple[int, int]]:
    """Gaps of at least min_minutes inside [day_start, day_end) not covered by any event."""
    clipped = []
    for ev in events:
        s = max(ev.start, day_start)
        e = min(ev.end, day_end)
        if s < e:
            clipped.append((s, e))
    clipped.sort()
    slots = []
    cursor = day_start
    for s, e in clipped:
        if s > cursor:
            slots.append((cursor, s))
        if e > cursor:
            cursor = e
    if cursor < day_end:
        slots.append((cursor, day_end))
    return [(s, e) for s, e in slots if e - s >= min_minutes]


def fmt_duration(minutes: int) -> str:
    """Render minutes as "Xh YYm"."""
    return f"{minutes // 60}h {minutes % 60:02d}m"
