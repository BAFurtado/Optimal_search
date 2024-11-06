''' Program to find three periods of vacation of varying length that does not start in a weekend or holiday'''

import copy
from datetime import date
from random import randint, choice
import pandas as pd
from pandas.tseries.holiday import Holiday, AbstractHolidayCalendar


# Define Brazilian public holidays for 2025
class BrazilHolidayCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday("Ano Novo", month=1, day=1),  # New Year's Day
        Holiday("Carnaval - Segunda", month=3, day=3),  # Carnival Monday (ponto facultativo)
        Holiday("Carnaval - Terça", month=3, day=4),  # Carnival Tuesday (ponto facultativo)
        Holiday("Quarta-feira de Cinzas", month=3, day=5),  # Ash Wednesday (ponto facultativo, partial)
        Holiday("Sexta-Feira Santa", month=4, day=18),  # Good Friday
        Holiday("Tiradentes", month=4, day=21),  # Tiradentes Day
        Holiday("Dia do Trabalho", month=5, day=1),  # Labor Day
        Holiday("Corpus Christi", month=6, day=19),  # Corpus Christi (ponto facultativo)
        Holiday("Independência do Brasil", month=9, day=7),  # Independence Day
        Holiday("Nossa Senhora Aparecida", month=10, day=12),  # Our Lady of Aparecida
        Holiday("Finados", month=11, day=2),  # All Souls' Day
        Holiday("Proclamação da República", month=11, day=15),  # Republic Day
        Holiday("Consciência Negra", month=11, day=20),  # Black Awareness Day (regional)
        Holiday("Natal", month=12, day=25)  # Christmas Day
    ]


class Working:
    def __init__(self, start, end):
        self.cal = BrazilHolidayCalendar()
        self.df = pd.DataFrame()
        # Generate a date range and convert to datetime.date format
        self.df['date'] = pd.date_range(start=start, end=end).date
        # Store holidays as a set of datetime.date objects
        self.holidays = set(self.cal.holidays(start=start, end=end).date)
        # Calculate 'not_working' by checking if the day is a weekend or holiday
        self.df['not_working'] = self.df['date'].apply(
            lambda x: x.weekday() in [5, 6] or x in self.holidays
        )
        self.starting_days = []

    def total_working_days(self):
        # Counts total working days (not marked as not_working)
        return (self.df['not_working'] == False).sum()

    def apply_vacation(self, d, offset=0):
        # Marks the vacation days as 'not_working'
        for i in range(offset + 1):  # Include the start day
            date_to_mark = d + pd.Timedelta(days=i)
            if date_to_mark in self.df['date'].values:
                self.df.loc[self.df['date'] == date_to_mark, 'not_working'] = True

    def find_starting_day(self):
        # Finds a random 'not_working' day set to False which means a good day to start the vacation
        valid_start_days = self.df[self.df['not_working'] == False]['date'].tolist()
        if not valid_start_days:
            raise ValueError("No valid starting days available.")
        return choice(valid_start_days)

    def schedule(self, pack):
        # Distributes vacation days within three different periods
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
    iterator = 1000
    minimorum = Working(first, final)
    days = None, None, None

    while iterator > 0:
        leisure = Working(first, final)
        a, b, c = three_periods()
        leisure.schedule((a, b, c))

        if leisure.total_working_days() < minimorum.total_working_days():
            minimorum = copy.deepcopy(leisure)
            days = a, b, c

        iterator -= 1

    print('Total working days for this configuration is {} days'.format(minimorum.total_working_days()))
    for i in range(3):
        print('Vacation period starts on {} and lasts for {} days'.format(minimorum.starting_days[i], days[i]))


if __name__ == "__main__":
    first_day = date(2025, 1, 1)
    final_day = date(2025, 12, 31)
    main(first_day, final_day)

    my_holidays = Working(first_day, final_day)
    a, b, c = (5, 9, 16)
    d1 = date(2025, 1, 6)
    d2 = date(2025, 7, 7)
    d3 = date(2025, 12, 8)
    y = d1, d2, d3
    my_holidays.apply_vacation(d1, a)
    my_holidays.apply_vacation(d2, b)
    my_holidays.apply_vacation(d3, c)

    print('')
    print(f'Total working days for this configuration is {my_holidays.total_working_days()} days')
    x = a, b, c
    for i in range(3):
        print('Vacation period starts on {} and lasts for {} days'.format(y[i], x[i]))
