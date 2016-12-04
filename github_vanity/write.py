import time

from datetime import date, timedelta
from random import randint
from sys import stdout

from .font import get_char_grid, get_char_width

SPACE_WIDTH = 5


def get_root_date(today=date.today()):
    weekday = today.weekday()
    last_sunday = today if weekday == 6 else today - timedelta(days=weekday + 1)
    return last_sunday - timedelta(weeks=53)


def get_date(start_date, x, y):
    if x < 0 or x > 52 or y < 0 or y > 6:
        raise Exception("Out of bounds")

    return start_date + timedelta(weeks=x) + timedelta(days=y)


def write_pixel(repo, start_date, x, y, commits):
    date = get_date(start_date, x, y)
    datetime = "%sT12:00:00" % str(date)

    for i in range(commits):
        msg = "Pixel at (%d, %d), commit %d" % (x, y, i)
        repo.index.commit(msg, commit_date=datetime, author_date=datetime)


def write_char(repo, char, start_date, offset, commits):
    grid = get_char_grid(char)
    for y, row in enumerate(grid):
        for x, pixel in enumerate(row):
            if pixel != ' ':
                stdout.write(".")
                stdout.flush()
                write_pixel(repo, start_date, x + offset, y, commits)


def write_text(text, repo, start_date=get_root_date(), offset = 0, spacing=1, commits=50):
    for char in text:
        if char == ' ':
            offset += SPACE_WIDTH
            continue

        width = get_char_width(char)

        print "\nWriting '%s' at offset %d" % (char, offset)
        write_char(repo, char, start_date, offset, commits)

        offset += width + spacing

    print "\nDone"
