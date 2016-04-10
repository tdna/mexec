

class Docker(object):

    def __init__(self, cli):
        self.cli = cli

    def logs(self, container, **kwargs):
        return self.cli.logs(container, **kwargs)

    def top(self, container, **kwargs):
        return self.cli.top(container, **kwargs)

    def inspect(self, container):
        return self.cli.inspect_container(container)

    def exec_container(self, container, cmd):
        return self.cli.exec_start(self.cli.exec_create(container, cmd))

    def exec_by_env_variable(self, env_variable, callback):
        def have_env(container):
            env_vars = self.cli.inspect_container(container)['Config']['Env']
            return env_variable in set(env_vars)

        return [callback(container['Id'])
                for container in self.cli.containers()
                if have_env(container['Id'])]
