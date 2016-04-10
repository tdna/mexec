import pytest

from mexec.docker import Docker


@pytest.fixture
def container_data():
    return {
        'logs': 'some logs',
        'top': 'process1, process2',
        'inspect': [
            {
                'Config': {
                    'Env': ['SOME_VAR=val', 'MESOS_TASK_ID=12313']
                }
            },
            {
                'Config': {
                    'Env': ['SOME_VAR=val']
                }
            }
        ],
        'exec': 'exec result',
        'containers': [
            {
                'Id': 'container1'
            },
            {
                'Id': 'container2'
            }
        ]
    }


@pytest.fixture
def cli(mocker, container_data):
    m = mocker.Mock
    docker_cli = m()
    docker_cli.logs = m(return_value=container_data['logs'])
    docker_cli.top = m(return_value=container_data['top'])
    docker_cli.inspect_container = m(side_effect=container_data['inspect'])
    docker_cli.exec_start = m(return_value=container_data['exec'])
    docker_cli.exec_create = m(return_value='exec_create_result')
    docker_cli.containers = m(return_value=container_data['containers'])
    return docker_cli


@pytest.fixture
def docker(mocker, cli):
    return Docker(cli)


class TestDocker(object):

    def test_logs(self, mocker, docker, cli, container_data):
        assert container_data['logs'] == docker.logs('containerdata')
        cli.logs.assert_called_once_with('containerdata')

        assert container_data['logs'] == docker.logs('containerdata', tail=5)
        cli.logs.assert_called_with('containerdata', tail=5)

    def test_top(self, mocker, docker, cli, container_data):
        assert container_data['top'] == docker.top('containerdata')
        cli.top.assert_called_once_with('containerdata')

        assert container_data['top'] == docker.top('containerdata',
                                                   ps_args='aux')
        cli.top.assert_called_with('containerdata', ps_args='aux')

    def test_inspect(self, mocker, docker, cli, container_data):
        assert container_data['inspect'][0] == docker.inspect('containerdata')
        cli.inspect_container.assert_called_once_with('containerdata')

    def test_exec_container(self, mocker, docker, cli, container_data):
        assert container_data['exec'] == docker.exec_container('containerdata',
                                                               'ls -l')
        cli.exec_create.assert_called_once_with('containerdata', 'ls -l')
        cli.exec_start.assert_called_once_with('exec_create_result')

    def test_exec_by_env_variable(self, mocker, docker, cli):
        def callback(container):
            return container * 2

        env_var = 'MESOS_TASK_ID=12313'
        exec_result = docker.exec_by_env_variable(env_var, callback)
        assert exec_result == ['container1container1']
