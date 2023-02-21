import argparse
from datetime import date, datetime
import json
import logging
from os.path import exists
import traceback

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S', level=logging.INFO)
#
parser = argparse.ArgumentParser('Lets process some command inputs')
task_interaction_type_group = parser.add_mutually_exclusive_group()
parser.add_argument('-d', '--description', help='description body of the task to be added', type=str)
parser.add_argument('-tid', '--task_id', help='id of the task to be removed', type=int)
task_interaction_type_group.add_argument('-a', '--add', help='add a task to existing tasks list', action='store_true')
task_interaction_type_group.add_argument('-rm', '--remove', help='remove a task from existing task list', action='store_true')
task_interaction_type_group.add_argument('-l', '--list', help='list all the tasks from existing list', action='store_true')
logger = logging.getLogger('Tasker')

class Utils:
    def json_serializer(self, object_class):
        if isinstance(object_class, (date, datetime)):
            return object_class.isoformat()
    def remove_task(self, task_id):
        try:
            tasks_dict = self.get_tasks_dict()
            del tasks_dict['tasks'][str(task_id)]
            self.save_tasks_to_file(tasks_dict)
        except Exception as e:
            logger.info('no tasks to delete')
            logger.error(e)
            traceback.print_exc()
    def get_tasks_dict(self):
        with open('tasks_dict', 'r') as f:
            return json.load(f)
    def save_tasks_to_file(self, tasks_dict):
        with open('tasks_dict', 'w') as f:
            json.dump(tasks_dict, f, default=self.json_serializer)
    def list_tasks(self):
        try:
            tasks_dict = self.get_tasks_dict()
            all_tasks = tasks_dict['tasks']
            logger.info('listing tasks')
            logger.info('task_id | task description | created_at')
            for each_task_id in tasks_dict['tasks']:
                logger.info('{} | {} | {}'.format(all_tasks[each_task_id]['task_id'], all_tasks[each_task_id]['description'], datetime.fromisoformat(all_tasks[each_task_id]['datetime'])))
        except Exception as e:
            logger.error('No tasks to list')
            traceback.print_exc()

util_object = Utils()

class App:
    def __init__(self, description):
        try:
            tasks_dict = util_object.get_tasks_dict()
            self.task_id=int(tasks_dict['last_task_id']) + 1
        except Exception as e:
            logger.error(e)
            self.task_id = 1
        self.description = description
        self.datetime = datetime.now()
    def show_task_description(self):
        print(self.description)
        print(self.datetime)
    def add_task(self):
        try:
            # execute if tasks_dict file is present
            tasks_dict = util_object.get_tasks_dict()
            tasks_dict['last_task_id'] = self.task_id
            tasks_dict['tasks'][self.task_id] = self.__dict__
            return tasks_dict
        except Exception as e:
            # execute if tasks_dict file is absent
            logger.error(e)
            current_task_dict = self.__dict__
            tasks_dict = {}
            tasks_dict['last_task_id'] = 1
            tasks_dict['tasks'] = {}
            tasks_dict['tasks'][self.task_id] = current_task_dict
            return tasks_dict
    def save_added_task(self):
        tasks_dict = self.add_task()
        util_object.save_tasks_to_file(tasks_dict)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.add:
        if args.description:
            logger.info('adding task')
            app_object = App(args.description)
            app_object.show_task_description()
            app_object.save_added_task()
        else:
            logger.error('Please insert description with flag -d')
    elif args.remove:
        logger.info('removing task')
        if args.task_id:
            util_object.remove_task(args.task_id)
        else:
            logger.error('Please insert the task id to be deleted with flag -tid')
    elif args.list:
        util_object.list_tasks()
    else:
        logger.error('Please select one of the task flags from add/remove/list (-a, -rm, -l), see help for usage description')
