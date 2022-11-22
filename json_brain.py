import json


class JSON_Brain:

    def read_files(self, file):
        with open(file, 'r') as file:
            data = json.load(file)
        return data

    def save_tasks(self, sorted_tasks):
        all_tasks = []
        for task in sorted_tasks:
            task_json = task.json_converter()
            all_tasks.append(task_json)
        # Saving the data
        json_object = json.dumps(all_tasks, indent=4)
        with open("tasks_json.json", "w") as outfile:
            outfile.write(json_object)

    def save_preferences(self, preferences_json):
        json_object = json.dumps(preferences_json, indent=4)
        with open("preferences_json.json", "w") as outfile:
            outfile.write(json_object)
