from preferences import Preferences
import datetime
from calendar import monthrange


class Task(Preferences):

    def __init__(self, title, year, month, day, hoursToComplete):
        super().__init__()
        self.new_day = None  # These 3 are here because PyCharm wants it!
        self.new_month = None
        self.new_year = None

        self.title = title
        self.year = year
        self.month = month
        self.day = day
        self.hoursToComplete = hoursToComplete
        self.daysUntilDeadline = self.days_until_deadline(self.year, self.month, self.day)
        self.count = self.hoursToComplete

    def initializing(self):
        self.title = input("Title: ").title()
        self.check_deadline()
        self.check_hours_to_complete()

    def check_deadline(self):
        while True:
            self.new_year = input("Year (<Enter> if this year): ")
            self.check_year_month(self.new_year, 1)

            self.new_month = input("Month (<Enter> if this month): ")
            self.check_year_month(self.new_month, 2)

            self.new_day = input("Day: ")
            self.check_day(self.new_day)

            if self.new_year == "":
                self.year = int(datetime.date.today().year)
            else:
                self.year = int(self.new_year)

            if self.new_month == "":
                self.month = int(datetime.date.today().month)
            else:
                self.month = int(self.new_month)

            self.day = int(self.new_day)

            set_deadline_str = str(self.year) + "-" + str(self.month) + "-" + str(self.day)
            set_deadline_dt = datetime.datetime.strptime(set_deadline_str, '%Y-%m-%d').date()
            if set_deadline_dt <= datetime.date.today():
                print("This deadline has already passed. Please try again!")
            else:
                break

    def check_hours_to_complete(self):
        while True:
            while True:
                try:
                    hours = int(input("Hours to complete: "))
                    break
                except:
                    print("Please enter a number!\n")
            if hours > 0:
                self.hoursToComplete = hours
                break

    def json_converter(self):
        task_dict = {
            "title": self.title,
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hoursToComplete": self.hoursToComplete,
        }
        return task_dict

    def edit_task(self):
        print(
            f"{self.title} details:\n\tDeadline: {self.year}-{self.month}-{self.day} ({self.daysUntilDeadline} days)\n\tTime to complete: {self.hoursToComplete} hours")
        return int(input(
            "\nWhat do you want to change:\n\t1) Task title\n\t2) Task deadline\n\t3) Task time to complete\n\t4) Nothing\n\n: "))

    def days_until_deadline(self, year, month, day):
        today = datetime.date.today()
        task_deadline = datetime.date(year, month, day)
        days = (task_deadline - today).days
        return days

    def change_title(self):
        new_title = input("New title: ")
        self.title = new_title

    # Error handling

    def check_year_month(self, year_month, option):  # Option is 1 if year, 2 if month
        while True:
            if year_month != "":
                try:
                    int(year_month)
                except ValueError:
                    print("You must enter a number, please try again!")
                    if option == 1:
                        year_month = input("Year (<Enter> if this year): ")
                    if option == 2:
                        year_month = input("Month (<Enter> if this month): ")
                    continue

                if option == 1:
                    if len(year_month) != 4:
                        print("The year was entered incorrectly. Please enter it correctly (e.g. 2002).")
                        year_month = input("Year (<Enter> if this year): ")
                        continue

                if option == 2:
                    if len(year_month) != 1 and len(year_month) != 2:
                        print("The month was entered incorrectly. Please enter it correctly (e.g. 02 or 2).")
                        year_month = input("Month (<Enter> if this year): ")
                        continue
            if option == 1:
                self.new_year = year_month
            if option == 2:
                self.new_month = year_month
            break

    def check_day(self, day):
        while True:
            try:
                int(day)
            except ValueError:
                print("You must enter a number, please try again!")
                day = input("Day: ")
                continue
            except:
                print("Something went wrong. Please try again!")
                day = input("Day: ")
                continue

            if len(day) != 1 and len(day) != 2:
                print("The day was entered incorrectly. Please enter it correctly (e.g. 02 or 2).")
                day = input("Day: ")
                continue

            if int(day) > monthrange(self.year, self.month)[1]:
                print("Invalid day. Please enter a valid one!")
                day = input("Day: ")
                continue

            self.new_day = day
            break

    def mark_as_done(self):
        sessions_done = input("How many hours have you completed: ")
        while True:
            try:
                int(sessions_done)
            except ValueError:
                print("You must enter a number, please try again!")
                sessions_done = input("How many hours have you completed: ")
                continue
            except:
                print("Something went wrong. Please try again!")
                sessions_done = input("How many hours have you completed: ")
                continue

            if int(sessions_done) > self.hoursToComplete or int(sessions_done) < 0:
                print(f"You don't have that many sessions on {self.title}. Please write a valid number")
                sessions_done = input("How many sessions have you completed: ")
                continue

            self.hoursToComplete -= int(sessions_done)
            return int(sessions_done)

    def valid_deadline(self):
        return self.daysUntilDeadline > 1
