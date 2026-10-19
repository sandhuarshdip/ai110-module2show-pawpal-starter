from datetime import date
from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_completing_daily_task_removes_today_and_shows_tomorrow() -> None:
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(str(app_path)).run(timeout=10)

    assert date.today().strftime("%A, %B %d, %Y") in [
        caption.value for caption in app.caption
    ]

    app.button[0].click().run(timeout=10)
    app.checkbox[0].check().run(timeout=10)
    app.button[1].click().run(timeout=10)
    app.button[2].click().run(timeout=10)

    assert not app.exception
    assert app.table[0].value.iloc[0]["Status"] == "Complete"
    assert app.table[1].value.iloc[0]["Task"] == "Morning walk"
    assert "No incomplete tasks due today." in [item.value for item in app.info]


def test_duplicate_task_requires_confirmation_before_adding() -> None:
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(str(app_path)).run(timeout=10)

    app.button[0].click().run(timeout=10)
    app.button[1].click().run(timeout=10)
    assert len(app.table[0].value) == 1

    app.button[1].click().run(timeout=10)
    assert [item.value for item in app.error] == [
        "Duplicate task detected! If not a mistake click Add Task again."
    ]
    assert len(app.table[0].value) == 1

    app.button[1].click().run(timeout=10)
    assert not app.exception
    assert not app.error
    assert len(app.table[0].value) == 2
