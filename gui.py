class GUI:

    def printing(self, schedule, preferences):
        """Used to print the information of the above-mentioned function"""
        if schedule:  # If there are tasks
            print("STUDY SCHEDULE")
            for i in range(0, len(schedule)):  # Iterate though each day in the schedule
                if schedule[i]:  # If the day has tasks
                    if i == 0:
                        print("- Today")
                    elif i == 1:
                        print("- Tomorrow")
                    else:
                        print(f"- Day {i + 1}")
                    for j in range(len(schedule[i])):  # Print the task and the respective time to study
                        if schedule[i][j][0] != "Done":
                            if preferences.frequency == "long":
                                print(
                                    f"\t{schedule[i][j][0]}: {schedule[i][j][1]} sessions of 1 hour ({schedule[i][j][1] * 60} min)")
                            else:
                                print(
                                    f"\t{schedule[i][j][0]}: {schedule[i][j][1] * 2} sessions of 30 minutes ({schedule[i][j][1] * 60} min)")

    def what_to_do(self, schedule, preferences, error_type):
        """Ask the user what to do"""
        self.clean_console()
        self.printing(schedule, preferences)
        error = {
            0: "",
            1: "\n\nPlease enter an integer and try again.",
            2: "\n\nPlease enter a number in the range from 1 to 6.",
            3: "\n\nSomething went wrong. Try again.",
            4: "\n\nPlease enter a number in the range from 1 to 3."
        }

        if schedule:
            out = "\nWhat do you want to do:\n\t1) Exit\n\t2) Add task\n\t3) Change preferences\n\t4) See a task\n\t5) Mark as done\n\t6) Delete a Task " + error.get(error_type) + "\n\n: "
            return input(out)

        else:
            out = "\nWhat do you want to do:\n\t1) Exit\n\t2) Add task\n\t3) Change preferences" + error.get(error_type) + "\n\n: "
            return input(out)

    def check_done(self, tasks):
        '''Checks whether a task is done or not'''
        if tasks[0].title != "Done":
            return 1
        else:
            return 0

    def show_tasks(self, tasks, done):
        '''Prints all the tasks is a neat way'''
        print("List of tasks:")
        for i in range(0, len(tasks)):
            if tasks[i].title != "Done":
                print(
                    f"{i + done}) {tasks[i].title}: Due to {tasks[i].year}-{tasks[i].month}-{tasks[i].day}. You estimate {tasks[i].hoursToComplete} hours to complete the task")
        print()

    def choose_task(self):
        '''Print "which tasks to choose" method with error checking'''
        choice = input("\nWhich task (to exit type 0): ")
        while True:
            try:
                int(choice)
            except ValueError:
                print("You must enter a number, please try again!")
                choice = input("\nWhich task (to exit type 0): ")
                continue
            except:
                print("Something went wrong. Please try again!")
                choice = input("\nWhich task (to exit type 0): ")
                continue

            return int(choice)

    def clean_console(self):
        '''Cleans console by printing many spaces'''
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
