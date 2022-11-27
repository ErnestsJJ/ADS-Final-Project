from brain import Brain
from gui import GUI
from task import Task
from preferences import Preferences
from json_brain import JSON_Brain


def main():
    json_brain = JSON_Brain()
    brain = Brain()
    gui = GUI()

    # User program
    while True:
        preferences_data = json_brain.read_files("preferences_json.json")
        if preferences_data:
            preferences = Preferences()
            preferences.initializing_preferences(preferences_data[0]["frequency"], preferences_data[0]["distribution"],
                                                 preferences_data[0]["study_time"], preferences_data[0]["created"], preferences_data[0]["done"])
        else:
            preferences = Preferences()
        tasks = []
        # Converting all JSON formatted tasks into python task objects
        tasks_data = json_brain.read_files("tasks_json.json")
        if tasks_data:
            for i in tasks_data:
                task = Task(i["title"], i["year"], i["month"], i["day"], i["hoursToComplete"])
                if task.valid_deadline():
                    tasks.append(task)
        if preferences.done != 0:
            preferences.compare_time()
            preferences.change_created()
            sorted_tasks = brain.sort_tasks(tasks, preferences.done)

        else:
            sorted_tasks = brain.sort_tasks(tasks, 0)
        schedule = brain.how_much(sorted_tasks, preferences)
        gui.clean_console()
        error_type = 0
        while True:
            what = gui.what_to_do(schedule, preferences, error_type)
            try:
                what = int(what)
            except ValueError:
                error_type = 1
                continue

            if not sorted_tasks and what > 3 or what < 1:
                error_type = 4
                continue

            elif what == 1:
                return

            elif what == 2:
                while True:
                    gui.clean_console()
                    task = Task(0, 2022, 11, 24, 5)
                    task.initializing()
                    sorted_tasks.append(task)
                    cont = input("Do you want to add another task? (yes/no): ").lower()
                    while cont not in ["yes", "no"]:
                        cont = input("Invalid Answer. Do you want to add another task? (yes/no): ")
                    if cont == "no":
                        # Converting all tasks objects into a JSON compatible format
                        break
                break

            elif what == 3:
                gui.clean_console()
                what1 = preferences.what()
                if what1 == 1:
                    preferences.change_study_time()
                elif what1 == 2:
                    preferences.change_frequency()
                elif what1 == 3:
                    preferences.change_distribution()
                break

            elif what == 4:
                gui.clean_console()
                gui.show_tasks(sorted_tasks, gui.check_done(sorted_tasks))
                selected_task = gui.choose_task()
                if selected_task != 0:
                    while True:
                        selected_task = gui.choose_task()
                        if selected_task > len(sorted_tasks) or selected_task < 0:
                            print("Please enter a valid number")
                        else:
                            break
                    task_index = selected_task - gui.check_done(sorted_tasks)
                    task = sorted_tasks.pop(task_index)
                    gui.clean_console()
                    what2 = task.edit_task()

                    if what2 == 1:
                        task.change_title()
                        sorted_tasks.append(task)
                    elif what2 == 2:
                        task.check_deadline()
                        sorted_tasks.append(task)
                    elif what2 == 3:
                        task.check_hours_to_complete()
                        sorted_tasks.append(task)
                    else:
                        sorted_tasks.append(task)
                    break

            elif what == 5:
                gui.clean_console()
                gui.show_tasks(sorted_tasks, gui.check_done(sorted_tasks))
                selected_task = gui.choose_task()
                if selected_task != 0:
                    while True:
                        if selected_task > len(sorted_tasks) or selected_task < 0:
                            print("Please enter a valid number")
                            selected_task = gui.choose_task()
                        else:
                            break
                task_index = selected_task - gui.check_done(sorted_tasks)
                if selected_task != 0:
                    if task_index != 0 - gui.check_done(sorted_tasks):
                        task = sorted_tasks.pop(task_index)
                        new_done = task.mark_as_done()
                        preferences.done += new_done
                        if task.hoursToComplete != 0:
                            sorted_tasks.append(task)
                    break

            elif what == 6:
                gui.clean_console()
                gui.show_tasks(sorted_tasks, gui.check_done(sorted_tasks))
                while True:
                    selected_task = gui.choose_task()
                    if selected_task > len(sorted_tasks) or selected_task < 0:
                        print("Please enter a valid number")
                    else:
                        break
                if selected_task != 0:
                    sorted_tasks.pop(selected_task - gui.check_done(sorted_tasks))
                    sure = input("Are you sure? (yes/no): ").lower()
                    while sure not in ["yes", "no"]:
                        sure = input("Are you sure? (yes/no): ").lower()
                    if sure == "yes":
                        json_brain.save_tasks(sorted_tasks)
                    break

            elif what > 6 or what < 1:
                error_type = 2
                continue

            else:
                error_type = 3

        if brain.check_done(sorted_tasks):
            sorted_tasks.pop(0)
        json_brain.save_tasks(sorted_tasks)
        preferences_json = [preferences.json_preferences_converter()]
        json_brain.save_preferences(preferences_json)


if __name__ == '__main__':
    main()
