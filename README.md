[![Build Status](https://travis-ci.org/tdna/mexec.svg?branch=master)](https://travis-ci.org/tdna/mexec)

# Mexec

Mexec is a Python module for execute commands inside docker containers run on Mesos.

The mexec package works on Python versions:

* 2.7.x and greater
* 3.4.x and greater

## Installation

The easiest way to install mexec is to use pip:

```sh
$ pip install mexec
```

Install via setup.py

```sh
$ python setup.py install
```

## Getting Started

Make sure your docker daemons can be access with TCP (eg: docker daemon started with -H=tcp://0.0.0.0:2375)
Set MEXEC_MESOS_MASTER environmental variable separated by commas and MEXEC_DOCKER_PORT (or you can set them with a cli argument):

```sh
# with env var
$ export MEXEC_MESOS_MASTER=master-1:5050,master-2:5050,master-3:5050
$ export MEXEC_DOCKER_PORT=2375

# or with cli arg
$ mexec --mesos-master master-1:5050,master-2:5050,master-3:5050 --docker-port 2375 ...
```

### Inspect container

Inspect container. Identical to the `docker inspect` command.

```sh
$ mexec --docker-port 2375 YOUR_TASK_NAME inspect
```

### Container logs

Inspect container. Identical to the `docker logs` command.

```sh
$ mexec --docker-port 2375 --arg "timestamps=True" --arg "tail=5" YOUR_TASK_NAME logs
```

See other args [here] [logs].

### Container processes

Display the running processes of a container.

```sh
$ mexec --docker-port 2375 --arg "ps_args=aux" YOUR_TASK_NAME top
```

See other args [here] [top].

### Exec container

Run a command in a running container.

```sh
$ mexec --docker-port 2375 --arg "cmd=ls -l /" YOUR_TASK_NAME exec_container
```

[//]:

[logs]: <https://docker-py.readthedocs.org/en/stable/api/#logs>
[top]: <https://docker-py.readthedocs.org/en/stable/api/#top>
