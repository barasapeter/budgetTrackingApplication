from datetime import date, datetime
from typing import Type


def classmethods(cls):
    """Decorate all methods with @classmethod in a class."""
    for name, value in vars(cls).items():
        if callable(value):
            if not getattr(value, "__call__"):
                setattr(cls, name, classmethod(value))
    return cls


@classmethods
class CustomCalendar:
    return_type: Type[str]

    def date_today():
        """Returns date in YYYY-MM-DD"""
        return date.today().strftime("%Y-%m-%d")

    def time_now():
        """Returns time in H:M:S"""
        return datetime.now().strftime("%H:%M:%S")

    def week_day_name(date_YYYY_MM_DD: str):
        """Be sure to supply date in YYYY-MM-DD. Returns a day name of the week."""
        return datetime.strptime(date_YYYY_MM_DD, "%Y-%m-%d").strftime("%A")

    def day_name_today():
        """Returns today's day name"""
        return CustomCalendar.week_day_name(CustomCalendar.date_today())

tips_string = \
"""Alright mate, listen up! It's time to get that money sorted, innit? First off, you gotta make a sick 
budget to keep an eye on them expenses and suss out where you can cut back, you get me?\n\nSet them savings 
goals high to stay gassed and focused, bruv. Automate that ting by setting up regular transfers to your 
savings account, fam. Cut out them unnecessary spendings like eating out and subscription services, 
and put that cash towards your stash instead, init? Cook at home more often and save them bills on grub. 
Limit that credit card use, blud, or you'll be drowning in debt, know what I mean? Shop smart by hunting 
for them deals and using vouchers, my guy.\n\nExplore ways to boost that income, like a side hustle or freelancing, you feel me? Don't get caught up 
in that lifestyle inflation trap, keep increasing that savings rate as that income grows, fam. 
Prioritize building an emergency fund to cover them unexpected expenses, bruv. Invest wisely once you 
got that emergency fund sorted, init? Regularly review that budget and savings plan, and switch it up as 
needed, yeah? Follow these tips and stay on top of that savings game, and you'll be stacking that paper in no time, for real!"""

if __name__ == "__main__":
    print(CustomCalendar.time_now())
