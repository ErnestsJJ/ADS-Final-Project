import datetime


class Preferences:

    def __init__(self):
        self.frequency = "long"
        self.distribution = "fill"
        self.study_time = 3
        self.created = datetime.date.today()
        self.done = 0
        self.max_len = self.study_time

    def change_created(self):
        '''Updates the time when a change was created'''
        self.created = datetime.date.today()

    def compare_time(self):
        '''Compares time with previous time to manage mark as done'''
        today = datetime.date.today()
        if today != self.created:
            days = (self.created - today).days * -1
            for _ in range(days):
                if self.done >= self.study_time:
                    self.done -= self.study_time
                else:
                    self.done = 0
                    break

    def initializing_preferences(self, frequency, distribution, study_time, created, done):
        '''Takes preferences from JSON and initializes them'''
        self.frequency = frequency
        self.distribution = distribution
        self.study_time = study_time
        self.created = datetime.datetime.strptime(created, "%Y-%m-%d").date()
        self.done = done
        self.max_len = study_time

    def change_study_time(self):
        '''Changes study time preference (print statements included)'''
        while True:
            try:
                new_study_time = int(input("New study time per day: "))
            except ValueError:
                print("Please enter an integer.")
                continue
            except:
                print("Something went wrong. Please try again!")
                continue

            if new_study_time <= 0:
                print("Study time is unrealistic (less or equal to zero). Please try again!")
                continue
            elif new_study_time >= 24:
                print("Unrealistic study time. Please try again!")
                continue
            self.study_time = new_study_time
            break

    def change_frequency(self):
        '''Change frequency preference (print statements included)'''
        new_frequency = input("New frequency (short/long): ").lower()
        while new_frequency not in ["short", "long"]:
            new_frequency = input("Invalid. New frequency (short/long): ").lower()
        self.frequency = new_frequency

    def change_distribution(self):
        '''Change distribution preference (print statements included)'''
        new_distribution = input("New distribution (fill/spread): ")
        while new_distribution not in ["fill", "spread"]:
            new_distribution = input("Invalid. New frequency (fill/spread): ").lower()
        self.distribution = new_distribution

    def json_preferences_converter(self):
        '''Converts preferences to JSON format'''
        preferences_dict = {
            "frequency": self.frequency,
            "distribution": self.distribution,
            "study_time": self.study_time,
            "created": str(self.created),
            "done": self.done
        }
        return preferences_dict

    def what(self):
        """Prints preferences and asks the user what to change about the current preferences"""
        print(
            f"Your actual preferences:\n\tStudy time per day: {self.study_time} hours\n\tFrequency: {self.frequency}\n\tSessions distribution: {self.distribution}\n")
        option = input("What do you want to change:\n\t1) Study time per day\n\t2) Sessions frequency (long/short)\n\t3) Sessions distribution\n\t4) Nothing\n\n: ")

        while True:
            try:
                int(option)
            except ValueError:
                print("You must enter a number, please try again!")
                option = input(": ")
                continue
            except:
                print("Something went wrong. Please try again!")
                option = input(": ")
                continue

            if int(option) > 4 or int(option) < 0:
                print("Invalid number, please choose one in the range from 1 to 3")
                option = input(": ")
                continue

            return int(option)
