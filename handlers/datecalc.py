import time
from datetime import date
from typing import List


def __to_int(*argv) -> List[int]:
    """
    Simple function to convert all args into ints and return
    """
    _new_ints: List[int] = []
    for arg in argv:
        _new_ints.append(int(arg))
    return _new_ints


def __subtract_one(*argv) -> List[int]:
    """
    Subtracts one from all args
    """
    _subtracted: List[int] = []
    for arg in argv:
        _subtracted.append(int(arg) - 1)
    return _subtracted


def __calc_week(week, nr) -> int:
    week: int
    nr: int
    # calculate calender week in dependence of years (cw > 52)
    return (week + nr) % 52


def __calc_year(year_using, beginning_year) -> int:
    year_using: int
    beginning_year: int
    return year_using + beginning_year


def __calc_week_year(week, nr, years_using, beginning_year):
    week: int
    nr: int
    year_using: int
    beginning_year: int
    week = __calc_week(week, nr)
    year = __calc_year(years_using, beginning_year)
    return week, year


def __calc_start_date(week, year):
    week: int
    year: int
    """
    They're all itegers already, no need to convert again

    get the start date of the week using isocalender and
    reformat to yyyy-mm-dd format (for html)
    """
    return date.fromisocalendar(year, week, 1).strftime("%Y-%m-%d")


def __calc_end_date(week, year):
    week: int
    year: int
    """
    Same as __calc_start_date, but for the end of the week
    """
    return date.fromisocalendar(year, week, 5).strftime("%Y-%m-%d")


def __calc_sign_date():
    return time.strftime("%Y-%m-%d")


def __calc_beginning_year():
    # this could also be in defines.config.py, but we'll leave it here for now
    return int(time.strftime("%Y"))


def __pre_format(week, nr, years_using, beginning_year):
    # make sure everythink is an int
    week, nr, years_using, beginning_year = __to_int(week, nr, years_using, beginning_year)

    # decrease number and year (0 index)
    nr, years_using = __subtract_one(nr, years_using)

    return week, nr, years_using, beginning_year


# non private functions


def calc_all(week, nr, years_using, beginning_year):
    # preformat (convert to int, subtract stuff)
    week, nr, years_using, beginning_year = __pre_format(week, nr, years_using, beginning_year)

    # take the beginning year and add the period of years using, to get the total years
    total_year = beginning_year + years_using

    # get the calender week of the current number
    week = __calc_week(week, nr)

    # TODO: find an alternative to isocalender that works for pyhton 3.7 or lower
    return __calc_start_date(week, total_year), __calc_end_date(week, total_year), __calc_sign_date()


def calc_start(week, nr, years_using, beginning_year):
    week, nr, years_using, beginning_year = __pre_format(week, nr, years_using, beginning_year)
    week, year = __calc_week_year(week, nr, years_using, beginning_year)
    return __calc_start_date(week, year)


def calc_end(week, nr, years_using, beginning_year):
    week, nr, years_using, beginning_year = __pre_format(week, nr, years_using, beginning_year)
    week, year = __calc_week_year(week, nr, years_using, beginning_year)
    return __calc_end_date(week, year)


def calc_sign():
    return __calc_sign_date()


def calc_beginning_year():
    return __calc_beginning_year()
