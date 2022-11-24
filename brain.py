from task import Task


class Brain:

    def sort_tasks(self, tasks, done):
        '''This method sorts tasks in terms of deadline'''
        if tasks:
            sorted_tasks = []
            if done != 0:
                task = Task("Done", 2028, 7, 30, done)
                sorted_tasks.append(task)
            for _ in range(0, len(tasks)):
                smallest = tasks[0].daysUntilDeadline
                smallest_task = 0
                for i in range(1, len(tasks)):
                    if tasks[i].daysUntilDeadline < smallest:
                        smallest = tasks[i].daysUntilDeadline
                        smallest_task = i
                sorted_tasks.append(tasks.pop(smallest_task))
            return sorted_tasks
        return []

    def longer_task(self, tasks):
        """Used to search for the task with the furthest deadline"""
        general_array = []  # Create an empty array
        highest = tasks[0].daysUntilDeadline # Take first element deadline as the furthest deadline
        for task in tasks[1:]:  # Iterate through each task deadline
            if task.daysUntilDeadline > highest:  # Is the deadline higher than the already set up highest?
                highest = task.daysUntilDeadline  # If so, change highest
        for _ in range(0, highest):
            # For each of the days in the furthest deadline create an array with inside arrays representing the days
            general_array.append([])
        return general_array  # return the general_empty array

    def shortest_day(self, general_array, deadline):
        '''Used to find the shortest day'''
        smallest = len(general_array[0])
        smallest_day = 0
        for i in range(1, deadline):
            if len(general_array[i]) < smallest:
                smallest = len(general_array[i])
                smallest_day = i
        return smallest_day

    def finish_count(self, task, general_array):
        """Used to finish placing task sessions even if days are full"""
        while True:
            if task.count > 0:
                for i in range(0, task.daysUntilDeadline):
                    day = self.shortest_day(general_array, task.daysUntilDeadline)
                    general_array[day].append(task.title)
                    task.count -= 1
            else:
                break

    def fill_days(self, tasks, preferences):
        """Algorithm that fills out the days with tasks sessions"""
        general_array = self.longer_task(tasks)
        for task in tasks:  # Iterate through every task in tasks array and calculate number of sessions per task
            for i in range(0, task.daysUntilDeadline):
                # For each day until deadline, check if the day is not full and count of sessions is not 0
                while len(general_array[i]) < preferences.max_len and task.count > 0:
                    general_array[i].append(task.title)  # If true, append one task session to a day
                    task.count -= 1  # Then reduce the task session count
            self.finish_count(task, general_array)
        return general_array  # When finished, return the general_array filled out

    def spread_out_tasks(self, tasks, preferences):
        '''Arranges tasks if the "spread" preference is selected'''
        general_array = self.longer_task(tasks)
        for task in tasks:
            if task.title == "Done":
                for i in range(0, task.daysUntilDeadline):
                    # For each day until deadline, check if the day is not full and count of sessions is not 0
                    while len(general_array[i]) < preferences.max_len and task.count > 0:
                        general_array[i].append(task.title)  # If true, append one task session to a day
                        task.count -= 1  # Then reduce the task session count
                self.finish_count(task, general_array)
            else:
                for i in range(0, task.daysUntilDeadline):
                    while True:
                        day = self.shortest_day(general_array, task.daysUntilDeadline)
                        if len(general_array[day]) < preferences.max_len and task.count > 0:
                            general_array[day].append(task.title)
                            task.count -= 1
                        else:
                            break
                self.finish_count(task, general_array)
        return general_array

    def how_much(self, tasks, preferences):
        """Creates a list to know what and how much study each day"""
        if tasks:
            schedule = []
            if preferences.distribution == "fill":
                calendar = self.fill_days(tasks, preferences)
            else:
                calendar = self.spread_out_tasks(tasks, preferences)
            for day in range(0, len(calendar)):  # Iterate through everyday inside the calendar
                schedule.append([])  # Creat a new array for each day to that will contain the info of the tasks
                for task in tasks:  # Iterate through each task
                    # Count the amount of times a task is repeated inside a day (same as every study session)
                    study = calendar[day].count(task.title)
                    if study:
                        # If there are study sessions of that task that day, then append the name and the count
                        schedule[day].append((task.title, study))
            return schedule  # return the schedule with each task, and it's time per day

    def check_done(self, tasks):
        '''checks if a task is done'''
        if tasks:
            return tasks[0].title == "Done"
