import pytest

from calendar_core import Event, free_slots, fmt_duration, overlaps, parse_time


def test_parse_time_24h():
    assert parse_time("09:30") == 570
    assert parse_time("00:00") == 0


def test_parse_time_rejects_out_of_range():
    with pytest.raises(ValueError):
        parse_time("24:00")


def test_overlapping_events():
    assert overlaps(Event(540, 600), Event(570, 630))


def test_separate_events():
    assert not overlaps(Event(540, 600), Event(660, 720))


def test_free_slots_simple_day():
    events = [Event(540, 600), Event(720, 780)]
    assert free_slots(events, 480, 1020) == [(480, 540), (600, 720), (780, 1020)]


def test_free_slots_min_length():
    events = [Event(540, 600), Event(610, 700)]
    assert free_slots(events, 540, 760, min_minutes=30) == [(700, 760)]


def test_free_slots_unsorted_events():
    events = [Event(720, 780), Event(540, 600)]
    assert free_slots(events, 480, 1020) == [(480, 540), (600, 720), (780, 1020)]


def test_free_slots_overlapping_events():
    events = [Event(540, 700), Event(600, 650)]
    assert free_slots(events, 480, 800) == [(480, 540), (700, 800)]


def test_free_slots_unsorted_overlapping_events_respect_min_minutes():
    events = [Event(610, 700), Event(540, 620)]
    assert free_slots(events, 540, 760, min_minutes=30) == [(700, 760)]


def test_free_slots_clips_events_partly_outside_day():
    events = [Event(1000, 1200), Event(300, 540)]
    assert free_slots(events, 480, 1020) == [(540, 1000)]


def test_free_slots_ignores_events_entirely_outside_day():
    events = [Event(1020, 1200), Event(0, 480), Event(540, 600)]
    assert free_slots(events, 480, 1020) == [(480, 540), (600, 1020)]


def test_free_slots_event_covering_whole_day():
    assert free_slots([Event(0, 1440)], 480, 1020) == []


def test_free_slots_back_to_back_events_leave_no_gap():
    events = [Event(600, 720), Event(540, 600)]
    assert free_slots(events, 480, 800) == [(480, 540), (720, 800)]


def test_fmt_duration():
    assert fmt_duration(65) == "1h 05m"
    assert fmt_duration(45) == "0h 45m"


def test_event_needs_positive_length():
    with pytest.raises(ValueError):
        Event(600, 600)
