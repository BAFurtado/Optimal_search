''' Program to find three periods of vacation of varying length that does not start in a weekend or holiday'''

import copy
from datetime import date
from random import randint, choice

import pandas as pd
from pandas.tseries.holiday import Holiday, AbstractHolidayCalendar


class Brazil(AbstractHolidayCalendar):
    # Brazilian official holidays for 2018
    rules = [Holiday('Universal', year=2018, month=1, day=1), Holiday('Carnaval', year=2018, month=2, day=12),
             Holiday('Carnaval', year=2018, month=2, day=13), Holiday('Carnaval', year=2018, month=2, day=14),
             Holiday('Paixão', year=2018, month=3, day=30), Holiday('Tiradentes', year=2018, month=4, day=21),
             Holiday('Trabalho', year=2018, month=5, day=1), Holiday('Christi', year=2018, month=5, day=31),
             Holiday('Independência', year=2018, month=9, day=7), Holiday('Aparecida', year=2018, month=10, day=12),
             Holiday('Servidor', year=2018, month=10, day=28), Holiday('Finados', year=2018, month=11, day=2),
             Holiday('República', year=2018, month=11, day=15), Holiday('Natal', year=2018, month=12, day=25)]


class Working:
    # Initiates a calendar for 2018 as a pandas DataFrame. Includes holidays and weekends as 'not_working' = True
    def __init__(self, start, end):
        self.cal = Brazil()
        self.df = pd.DataFrame()
        self.df['date'] = pd.date_range(start=start, end=end)
        self.holidays = self.cal.holidays(start=start, end=end)
        self.df['not_working'] = self.df.date.apply(lambda x: x.dayofweek == 5 or x.dayofweek == 6
                                                              or x in self.holidays)
        self.starting_days = []

    def total_working_days(self):
        # Calculates total working days
        return sum(self.df['not_working'] == False)

    def apply_vacation(self, d, offset=0):
        # Turns sequential number of days of 'not_working' into True
        self.df.loc[self.df['date'] == d, 'not_working'] = True
        if offset != 0:
            for i in range(offset):
                self.df.loc[self.df['date'] == (d + pd.Timedelta(days=(i))), 'not_working'] = True

    def find_starting_day(self):
        # Finds a random 'not_working' day set to False which means a good day to start the vacation.
        selected = choice(self.df['date']).date()
        if self.df.loc[self.df['date'] == selected, 'not_working'].iloc[0] == True:
            return self.find_starting_day()
        else:
            return selected

    def schedule(self, pack):
        # Distributes 30 days of vacation within three different periods
        for each in pack:
            d = self.find_starting_day()
            self.starting_days.append(d)
            self.apply_vacation(d, each)


def three_periods():
    # Selects three periods that add up to 30 days
    a = randint(1, 28)
    b = randint(1, 29 - a)
    c = 30 - a - b
    return a, b, c


def main(first, final):
    # iterator = 0
    iterator = 10000
    minimorum = Working(first, final)
    days = None, None, None
    while iterator > 0:
    # while minimorum.total_working_days() > 223:
        leisure = Working(first, final)
        a, b, c = three_periods()
        leisure.schedule((a, b, c))
        if leisure.total_working_days() < minimorum.total_working_days():
            minimorum = copy.copy(leisure)
            days = a, b, c
        iterator -= 1
    print('Total working days for this configuration is {} days'.format(sum(minimorum.df['not_working'] == False)))
    for i in range(3):
        print('Vacation period starts on {} and lasts for {} days'.format(minimorum.starting_days[i], days[i]))
    print(iterator)


if "__main__" == __name__:
    first_day = date(2018, 1, 1)
    final_day = date(2018, 12, 31)
    main(first_day, final_day)

    # my_holidays = Working(first_day, final_day)
    # a, b, c = 5, 12, 13
    # d1 = date(2018, 1, 15)
    # d2 = date(2018, 7, 9)
    # d3 = date(2018, 12, 11)
    # my_holidays.apply_vacation(d1, a)
    # my_holidays.apply_vacation(d2, b)
    # my_holidays.apply_vacation(d3, c)
    # print('Total working days for this configuration is {} days'.format(sum(my_holidays.df['not_working'] == False)))
