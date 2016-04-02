

class Docker(object):
    def __init__(self, cli):
        self.cli = cli

    def containers_by_env_variable(self, env_variable, callback, **cb_kwargs):
        def have_env(container_id):
            return (env_variable in
                    set(self.cli.inspect_container(container_id)['Config']['Env']))

        return [callback(container['Id'], **cb_kwargs)
                for container in self.cli.containers()
                if have_env(container['Id'])]
