import requests
from collections import namedtuple


MesosTask = namedtuple('mesos_slave', ['slave_id', 'task_id'])


class Mesos(object):
    def __init__(self, hosts):
        self.hosts = hosts

    def get_slave_hostnames(self, slave_ids):
        return {slave['id']: slave['hostname'] for slave
                in self._call_endpoint('slaves')['slaves']
                if slave['id'] in slave_ids}

    def get_mesos_task_by_name(self, name):
        return [MesosTask(task['slave_id'], task['id']) for task
                in self._call_endpoint('tasks?limit=20000')['tasks']
                if task['name'] == name and task['state'] == 'TASK_RUNNING']

    def _call_endpoint(self, endpoint):
        r = requests.get('http://{}/{}'.format(self.hosts[0], endpoint))
        return r.json()
