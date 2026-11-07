import pytest

from calendar_core import Event, free_slots, fmt_duration, overlaps, parse_time


def test_parse_time_24h():
    assert parse_time("09:30") == 570
    assert parse_time("00:00") == 0


def test_parse_time_rejects_out_of_range():
    with pytest.raises(ValueError):
        parse_time("24:00")


def test_parse_time_24h_still_works():
    assert parse_time("23:59") == 1439
    assert parse_time("9:30") == 570


@pytest.mark.parametrize(
    "text, expected",
    [
        ("9am", 540),
        ("9 AM", 540),
        ("9AM", 540),
        ("9aM", 540),
        ("2:30pm", 870),
        ("2:30 PM", 870),
        ("12pm", 720),
        ("12am", 0),
        ("12:15am", 15),
        ("12:15pm", 735),
        ("12:00am", 0),
        ("12:00pm", 720),
        ("9:30am", 570),
        ("11:59pm", 1439),
        ("1am", 60),
    ],
)
def test_parse_time_12h(text, expected):
    assert parse_time(text) == expected


@pytest.mark.parametrize(
    "text",
    ["13pm", "0am", "9:60am", "9", "pm", "", "13:30pm", "0:30am", "9:60pm", "am", "12:60pm"],
)
def test_parse_time_rejects_invalid_12h(text):
    with pytest.raises(ValueError):
        parse_time(text)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("3pm", 900),
        ("10:05am", 605),
        ("6:07 Pm", 1087),
        ("12:01am", 1),
        ("12:01pm", 721),
        (" 11:45PM ", 1425),
    ],
)
def test_parse_time_12h_additional_general_cases(text, expected):
    assert parse_time(text) == expected


@pytest.mark.parametrize("text", ["14pm", "8:70am", "9:30xm", "24pm"])
def test_parse_time_rejects_additional_invalid(text):
    with pytest.raises(ValueError):
        parse_time(text)


def test_overlapping_events():
    assert overlaps(Event(540, 600), Event(570, 630))


def test_separate_events():
    assert not overlaps(Event(540, 600), Event(660, 720))


def test_back_to_back_events_do_not_overlap():
    assert not overlaps(Event(540, 600), Event(600, 660))
    assert not overlaps(Event(600, 660), Event(540, 600))


def test_free_slots_simple_day():
    events = [Event(540, 600), Event(720, 780)]
    assert free_slots(events, 480, 1020) == [(480, 540), (600, 720), (780, 1020)]


def test_free_slots_min_length():
    events = [Event(540, 600), Event(610, 700)]
    assert free_slots(events, 540, 760, min_minutes=30) == [(700, 760)]


def test_free_slots_unordered_overlapping_and_clipped():
    events = [Event(720, 780), Event(570, 630), Event(1000, 1100), Event(540, 600), Event(420, 500)]
    assert free_slots(events, 480, 1020) == [(500, 540), (630, 720), (780, 1000)]


def test_fmt_duration():
    assert fmt_duration(65) == "1h 05m"
    assert fmt_duration(45) == "0h 45m"


def test_event_needs_positive_length():
    with pytest.raises(ValueError):
        Event(600, 600)
