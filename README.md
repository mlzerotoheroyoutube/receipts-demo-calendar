# receipts-demo-calendar

Small day-planning helpers (overlaps, free slots, time parsing), used to test
[Receipts](https://github.com/mlzerotoheroyoutube/receipts): its agents pick up the issues here,
fix them, and open PRs only after independent checks and a SubQ judge approve.
The rules every change must follow are in the docstring of `calendar_core/slots.py`.

```bash
python -m pytest -q
```

Built at the AIE Code Summit Hackathon, Nov 7 2026. MIT licensed.
