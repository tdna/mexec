

class Docker(object):
    def __init__(self, cli):
        self.cli = cli

    def containers_by_env_variable(self, env_variable, callback):
        def have_env(container):
            env_vars = self.cli.inspect_container(container)['Config']['Env']
            return env_variable in set(env_vars)

        return [callback(container['Id'])
                for container in self.cli.containers()
                if have_env(container['Id'])]
