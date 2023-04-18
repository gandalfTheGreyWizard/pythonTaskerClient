import traceback
from helpers.tasks import Tasks
import json
from datetime import date, datetime

class Utils:
    """
        Utility module consists for multiple helper functions
    """
    def json_serializer(self, object_class):
        """
            Serialize object to json, transform datetime object to json
        """
        if isinstance(object_class, (date, datetime)):
            return object_class.isoformat()
    def remove_task(self, task_id):
        """
            Remove a task from task list against provided task id
        """
        try:
            tasks_dict = self.get_tasks_dict()
            del tasks_dict['tasks'][str(task_id)]
            self.save_tasks_to_file(tasks_dict)
        except Exception as e:
            traceback.print_exc()
    def get_tasks_dict(self):
        """
            Return all the tasks in the current task list
        """
        with open('tasks_dict', 'r') as f:
            return json.load(f)
    def save_tasks_to_file(self, tasks_dict):
        """
            Save the tasks to persistent file system
        """
        with open('tasks_dict', 'w') as f:
            json.dump(tasks_dict, f, default=self.json_serializer)
    def list_tasks(self):
        """
            List all the tasks from the current task list
        """
        try:
            tasks_dict = self.get_tasks_dict()
            all_tasks = []
            for each_task_id, eachTask in tasks_dict['tasks'].items():
                Tasks(eachTask)
            # logger.info('listing tasks')
            # logger.info('task_id | task description | created_at')
            Tasks.list()
            # for each_task_id in tasks_dict['tasks']:
                # logger.info('{} | {} | {}'.format(all_tasks[each_task_id]['task_id'], all_tasks[each_task_id]['description'], datetime.fromisoformat(all_tasks[each_task_id]['datetime'])))
        except Exception as e:
            traceback.print_exc()

