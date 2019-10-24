import sqlite3

from backend.config import DB_FILE
from backend.utils import create_path


CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS events (
    id INT,
    day TEXT,
    start TEXT,
    datetime_start TIMESTAMP,
    end TEXT,
    datetime_end TIMESTAMP,
    room TEXT,
    title TEXT,
    subtitle TEXT,
    abstract TEXT,
    description TEXT,
    persons TEXT,
    lecture_checked BOOL
)"""

INSERT_EVENT = """
INSERT INTO events VALUES (
    :id,
    :day,
    :start,
    :datetime_start,
    :end,
    :datetime_end,
    :room,
    :title,
    :subtitle,
    :abstract,
    :description,
    :persons,
    :lecture_checked
)"""

DELETE_EVENT = "DELETE FROM events WHERE id=:id"
DELETE_ALL_EVENTS = "DELETE FROM events"
SELECT_EVENT = "SELECT * FROM events WHERE id=:id"
SELECT_IDS_EVENT = "SELECT id FROM events"
SELECT_ALL_EVENT = "SELECT * FROM events ORDER BY datetime_start"
XSELECT_ALL_EVENT = """
SELECT
    id,
    day,
    start,
    datetime_start
    end,
    datetime_end
    room,
    title,
    subtitle,
    abstract,
    description,
    persons,
    lecture_checked
FROM events"""


def open_db():
    create_path(DB_FILE)
    con = sqlite3.connect(DB_FILE)
    # con.set_trace_callback(print)

    with con:
        cur = con.cursor()
        cur.execute(CREATE_TABLE)

    return con


def insert(event):
    con = open_db()

    with con:
        cur = con.cursor()
        cur.execute(INSERT_EVENT, dict(
            id=event.id,
            day=event.day,
            start=event.start,
            datetime_start=event.datetime_start,
            end=event.end,
            datetime_end=event.datetime_end,
            room=event.room,
            title=event.title,
            subtitle=event.subtitle,
            abstract=event.abstract,
            description=event.description,
            persons=event.persons,
            lecture_checked=True
        ))


def delete(event_id):
    con = open_db()

    with con:
        cur = con.cursor()
        cur.execute(DELETE_EVENT, dict(id=event_id))


def delete_all():
    con = open_db()

    with con:
        cur = con.cursor()
        cur.execute(DELETE_ALL_EVENTS)


def toggle(event):
    con = open_db()

    with con:
        cur = con.cursor()
        cur.execute(SELECT_EVENT, dict(id=int(event.id)))
        data = cur.fetchone()
        ret = False
        if data:
            delete(event.id)
        else:
            ret = True
            insert(event)
        return ret


def select_ids():
    con = open_db()

    with con:
        cur = con.cursor()
        cur.execute(SELECT_IDS_EVENT)
        data = cur.fetchall()
        return [x[0] for x in data]


def select_all():
    def dict_factory(cursor, row):
        d = {}
        for idx,col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    con = open_db()
    con.row_factory = dict_factory

    with con:
        cur = con.cursor()
        cur.execute(SELECT_ALL_EVENT)
        data = cur.fetchall()
        return data
