import argparse
from datetime import date, datetime
import json
import logging
from os.path import exists
import traceback
from helpers.tasks import Tasks
from helpers.utils import Utils
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S', level=logging.INFO)
#
parser = argparse.ArgumentParser('Lets process some command inputs')
task_interaction_type_group = parser.add_mutually_exclusive_group()
parser.add_argument('-d', '--description', help='description body of the task to be added', type=str)
parser.add_argument('-tid', '--task_id', help='id of the task to be removed', type=int)
task_interaction_type_group.add_argument('-a', '--add', help='add a task to existing tasks list', action='store_true')
task_interaction_type_group.add_argument('-rm', '--remove', help='remove a task from existing task list', action='store_true')
task_interaction_type_group.add_argument('-l', '--list', help='list all the tasks from existing list', action='store_true')
task_interaction_type_group.add_argument('-f', '--filter', help='list all the tasks from existing list', action='store_true')
parser.add_argument('-t', '--type', help='type of filter to be used 0=date_range | required fields (min_date, max_date), 1=sub_string | required fields (substring)', type=int)
parser.add_argument('-substr', '--sub_string', help='substring to be used for filter ', type=str)
parser.add_argument('-md', '--min_date', help='substring to be used for filter ', type=str)
parser.add_argument('-mxd', '--max_date', help='substring to be used for filter ', type=str)
logger = logging.getLogger('Tasker')



util_object = Utils()

class App:
    """
        Application module responsible for initializing and handling tasks
    """
    def __init__(self, description):
        try:
            tasks_dict = util_object.get_tasks_dict()
            self.task_id=int(tasks_dict['last_task_id']) + 1
        except Exception as e:
            logger.error(e)
            self.task_id = 1
        # defination for each task goes here
        self.description = description
        self.datetime = datetime.now()
    def show_task_description(self):
        print(self.description)
        print(self.datetime)

    def add_task(self):
        """
            Add a task to existing task list
        """
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
        """
            Save the added task
        """
        tasks_dict = self.add_task()
        util_object.save_tasks_to_file(tasks_dict)

if __name__ == '__main__':
    args = parser.parse_args()
    task_object = Tasks()
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
    elif args.filter:
        if args.type == 0:
            # date range filter call
            try:
                if args.max_date:
                    args.max_date = datetime.fromisoformat(args.max_date)
                    logger.info('maxdate {}'.format(args.max_date))
                else:
                    args.max_date = datetime.now()

                print('date range filter mindate :- {} | maxdate :- {}'.format(datetime.fromisoformat(args.min_date), datetime.fromisoformat(args.max_date)))
            except Exception as e:
                logger.error('min_date is a mandatory field')
                logger.error(e)
        elif args.type == 1:
            # substring filter call
            print('substring filter {}'.format(args.sub_string))
        else:
            logger.error('please choose a correct filter type use -h for more details')
    else:
        logger.error('Please select one of the task flags from add/remove/list (-a, -rm, -l), see help for usage description')
