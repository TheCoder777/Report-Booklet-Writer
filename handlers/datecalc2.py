# MIT License
#
# Copyright (c) 2020 TheCoder777
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# load system modules
import time
import datetime


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


def __calc_year(current_year: int, beginning_year: int) -> int:
    """
    Calculates the year as a single digit (0 for first year, 2 for 3rd year)
    """
    return current_year - beginning_year + 1


def __calc_nr(current_week: int, beginning_week: int, year: int) -> int:
    """
    Calculates the nr (number). This is more or less the count of how many Berichtshefte are done!
    """
    return (year - 1) * 52 + current_week - beginning_week
