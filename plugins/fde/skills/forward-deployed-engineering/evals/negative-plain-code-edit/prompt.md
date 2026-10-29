---
tags: [fde]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

In utils/dates.py, `is_weekend` returns True for Fridays. Fix it so only Saturday and Sunday count.

```python
import datetime as dt
def is_weekend(d: dt.date) -> bool:
    return d.weekday() >= 4
```
