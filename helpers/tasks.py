from datetime import date, datetime
import Levenshtein as lvn
import json
class Tasks:
    """
        The tasks module created to list and filter tasks
    """
    tasks = []
    task_index = 0
    def __init__(self):
        """
            Initialize the tasks object and push it to current task list
        """
        try:
            with open('tasks_dict.json', 'r') as f:
                tasks_dict = json.load(f)
                for each_task in tasks_dict['tasks']:
                    temp_task = {}
                    temp_task['task_id'] = int(each_task['task_id'])
                    temp_task['description'] = str(each_task['description'])
                    self.tasks.append(each_task)
                    self.task_index = each_task['task_id']
        except Exception as e:
            print('no tasks dict found')
        # temp_task = {}
        # temp_task['task_id'] = int(task_object['task_id'])
        # temp_task['description'] = str(task_object['description'])
        # temp_task['datetime'] = datetime.fromisoformat(task_object['datetime'])
        # temp_task['status'] = 'tod'
        # self.tasks.append(temp_task)

    @classmethod
    def add(cls, task_object):
        temp_task = {}
        temp_task['task_id'] = int(cls.task_index + 1)
        temp_task['description'] = str(task_object['description'])
        temp_task['datetime'] = datetime.fromisoformat(task_object['datetime'])
        temp_task['status'] = 'tod'
        cls.tasks.append(temp_task)
        cls.task_index = cls.tasks[-1]['task_id']

    @classmethod
    def remove(cls, task_id):
        for each_task in cls.tasks:
            if each_task['task_id'] == task_id:
                cls.tasks.remove(each_task)
        cls.task_index = cls.tasks[-1]['task_id']

    @classmethod
    def list(cls):
        """
            List current tasks
        """
        for each_task in cls.tasks:
            print(each_task)
    
    @classmethod
    def json_serializer(self, object_class):
        """
            Serialize object to json, transform datetime object to json
        """
        if isinstance(object_class, (date, datetime)):
            return object_class.isoformat()
    
    @classmethod
    def save(cls, tasks_dict):
        """
            Save the tasks to persistent file system
        """
        with open('tasks_dict.json', 'w') as f:
            json.dump(tasks_dict, f, default=cls.json_serializer)

    @classmethod
    def filter(cls, filter_type, min_date=None, max_date=None, sub_string=None):
        """
            Different filter implementations that can be used to filter tasks
        """
        filtered_tasks = []
        if filter_type == 'date_range':
            for each_task in cls.tasks:
                min_time_delta = each_task['datetime'] - datetime.fromisoformat(min_date)
                max_time_delta = datetime.fromisoformat(max_date) - each_task['datetime']
                if min_time_delta > 0 and max_time_delta > 0:
                    filtered_tasks.append(each_task)
            return filtered_tasks
        elif filter_type == 'sub_string':
            for each_task in cls.tasks:
                ratio = lvn.ratio(each_task['description'], sub_string)
                print(ratio)

