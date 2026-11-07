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


def test_back_to_back_events_do_not_overlap():
    assert not overlaps(Event(540, 600), Event(600, 660))
    assert not overlaps(Event(600, 660), Event(540, 600))


def test_events_sharing_a_minute_overlap():
    assert overlaps(Event(540, 600), Event(599, 660))
    assert overlaps(Event(599, 660), Event(540, 600))


def test_contained_and_identical_events_overlap():
    assert overlaps(Event(540, 660), Event(570, 600))
    assert overlaps(Event(570, 600), Event(540, 660))
    assert overlaps(Event(540, 600), Event(540, 600))


def test_free_slots_simple_day():
    events = [Event(540, 600), Event(720, 780)]
    assert free_slots(events, 480, 1020) == [(480, 540), (600, 720), (780, 1020)]


def test_free_slots_min_length():
    events = [Event(540, 600), Event(610, 700)]
    assert free_slots(events, 540, 760, min_minutes=30) == [(700, 760)]


def test_fmt_duration():
    assert fmt_duration(65) == "1h 05m"
    assert fmt_duration(45) == "0h 45m"


def test_event_needs_positive_length():
    with pytest.raises(ValueError):
        Event(600, 600)
