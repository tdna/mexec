from mexec.docker import Docker


class TestDocker(object):

    def test_logs(self, mocker):
        log_msg = 'some logs'
        cli = mocker.Mock()
        cli.logs = mocker.Mock(return_value=log_msg)

        docker = Docker(cli)

        assert log_msg == docker.logs('containerdata')
        cli.logs.assert_called_once_with('containerdata')
