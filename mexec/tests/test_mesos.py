import pytest

from mexec.mesos import Mesos, MesosTask


@pytest.fixture
def mesos():
    return Mesos(['master-1:5050', 'master-2:5050'])


@pytest.fixture
def slaves():
    return {
        'slaves': [
            {
                'id': 'slave1',
                'hostname': 'slave_host_1'
            },
            {
                'id': 'slave2',
                'hostname': 'slave_host_2'
            },
            {
                'id': 'slave3',
                'hostname': 'slave_host_3'
            }
        ]
    }


@pytest.fixture
def tasks():
    return [
        {
            'tasks': [
                {
                    'name': 'task1',
                    'id': 'taskid_1',
                    'slave_id': 'slave_id_1',
                    'state': 'TASK_RUNNING'
                },
                {
                    'name': 'task2',
                    'id': 'taskid_2',
                    'slave_id': 'slave_id_1',
                    'state': 'TASK_RUNNING'
                },
                {
                    'name': 'task1',
                    'id': 'taskid_3',
                    'slave_id': 'slave_id_2',
                    'state': 'TASK_KILLED'
                }
            ]
        },
        {
            'tasks': [
                {
                    'name': 'task3',
                    'id': 'taskid_4',
                    'slave_id': 'slave_id_2',
                    'state': 'TASK_RUNNING'
                },
                {
                    'name': 'task1',
                    'id': 'taskid_5',
                    'slave_id': 'slave_id_2',
                    'state': 'TASK_RUNNING'
                }
            ]
        },
        {
            'tasks': []
        }
    ]


class TestMesos(object):

    def test_get_slave_hostnames(self, mocker, mesos, slaves):
        mesos._call_endpoint = mocker.Mock(return_value=slaves)

        expected = {'slave1': 'slave_host_1', 'slave3': 'slave_host_3'}

        assert mesos.get_slave_hostnames({'slave1', 'slave3'}) == expected

    def test_get_mesos_tasks(self, mocker, mesos, tasks):
        mesos._call_endpoint = mocker.Mock()
        mesos._call_endpoint.side_effect = tasks

        expected = [MesosTask(slave_id='slave_id_1', task_id='taskid_1'),
                    MesosTask(slave_id='slave_id_2', task_id='taskid_5')]

        assert mesos.get_mesos_tasks('task1') == expected

    def test_call_endpoint(self, mocker, mesos):
        expected = {'key': ['val1', 'val2']}

        mocked_get = mocker.patch('requests.get')
        requests_res = mocker.Mock()
        requests_res.json = mocker.Mock(side_effect=[{'key': []}, expected])
        mocked_get.return_value = requests_res

        assert mesos._call_endpoint('slaves') == expected
