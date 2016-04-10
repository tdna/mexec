import requests
from collections import namedtuple, deque


MESOS_TASK_LIMIT = 10000
MesosTask = namedtuple('mesos_task', ['slave_id', 'task_id'])


class Mesos(object):

    def __init__(self, hosts):
        self.hosts = hosts

    def get_slave_hostnames(self, slave_ids):
        return {slave['id']: slave['hostname'] for slave
                in self._call_endpoint('slaves').get('slaves', [])
                if slave['id'] in slave_ids}

    def get_mesos_tasks(self, name):
        def find(tasks):
            return [MesosTask(task['slave_id'], task['id'])
                    for task in tasks
                    if task['name'] == name and
                    task['state'] == 'TASK_RUNNING']

        def get_tasks(tasks=None, offset=0):
            if not tasks:
                tasks = []

            endpoint_entity = ('tasks?offset={}&limit={}'
                               .format(offset, MESOS_TASK_LIMIT))
            tasks_chunk = self._call_endpoint(endpoint_entity)
            if len(tasks_chunk.get('tasks', [])):
                return get_tasks(tasks + find(tasks_chunk['tasks']),
                                 offset + MESOS_TASK_LIMIT)
            else:
                return tasks

        return get_tasks()

    def _call_endpoint(self, endpoint):
        def loop(hosts):
            try:
                r = requests.get('http://{}/{}'.format(hosts.pop(), endpoint))
                result = r.json()
                if not len(list(result.values())[0]):
                    return loop(hosts)
                else:
                    return result
            except IndexError:
                return {}
            except requests.exceptions.ConnectionError:
                return {}

        return loop(deque(self.hosts))
