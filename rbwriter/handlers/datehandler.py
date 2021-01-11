
# system modules
import datetime
import time

# internal modules
from ..defines import configs


def __current_year():
    return int(time.strftime("%Y"))


def __calc_start(week: int, year: int) -> str:
    """
    Calculates the start date using an iso calender
    """
    start_date = datetime.datetime.strptime(f"{str(year)}-W{str(week)}-D1",
                                            "%G-W%V-D%w")
    # return in yyyy-mm-dd (html) format
    return start_date.strftime("%Y-%m-%d")


def __calc_end(week: int, year: int) -> str:
    """
    Almost same as above, but D5 instead of D1 (Friday instead of Monday)
    """
    start_date = datetime.datetime.strptime(f"{str(year)}-W{str(week)}-D5",
                                            "%G-W%V-D%w")
    return start_date.strftime("%Y-%m-%d")


def __calc_year(entered_year: int, beginning_year: int) -> int:
    """
    Calculates the year as a single digit (0 for first year, 2 for 3rd year)
    (+1 because it's zero indexed)
    """
    return entered_year - beginning_year + 1


def __calc_nr(entered_week: int, beginning_week: int, year: int) -> int:
    """
    Calculates the nr (number). This is more or less the count of how many report booklets are done!
    (+1 because it's also zero indexed)
    """
    return (year - 1) * 52 + entered_week - beginning_week + 1


def __start_date_edge_cases(start_date):

    # first edge case:
    # first week of apprenticeship is only 4 days long, beginning on tuesday!
    year, month, day = start_date.split("-")
    part_date = "-".join([month, day])
    if part_date == "08-31":
        start_date = year + "-09-01"

    return start_date


def calc_sign_date():
    return time.strftime("%Y-%m-%d")


def get_current_year():
    return __current_year()


def calc_beginning_year():
    return __current_year()


def get_current_week():
    return time.strftime("%V")


def calc_all(entered_year: int,
             entered_week: int,
             beginning_year: int = __current_year(),
             start_week: int = configs.START_WEEK):
    """
    Unified function to calculate pdf params either from config or from given values
    """

    # calculate start and end date (strptime format is: year-calender_week-week_day(1-7))
    start_date = datetime.datetime.strptime(f"{entered_year}-{entered_week}-{configs.START_OF_WEEK}",
                                            "%G-%V-%w").strftime("%Y-%m-%d")
    end_date = datetime.datetime.strptime(f"{entered_year}-{entered_week}-{configs.END_OF_WEEK}",
                                          "%G-%V-%w").strftime("%Y-%m-%d")
    # some edge cases for the start_date
    start_date = __start_date_edge_cases(start_date)
    
    # calculate single digit year
    year = __calc_year(entered_year, beginning_year)

    # calculate number (see description)
    nr = __calc_nr(entered_week, start_week, year)

    return {
        "start": start_date,
        "end": end_date,
        "nr": nr,
        "year": year
    }


def calc_user_defaults(year_from_db: int):
    year = __current_year() + year_from_db

    return {
        "sign": calc_sign_date(),
        "year": year
    }
