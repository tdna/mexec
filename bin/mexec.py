#!/usr/bin/env python

import argparse

if __name__ == '__main__':
    desc = 'Execute commands inside docker containers run by marathon.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('marathon_id', help='Marathon app id')
    parser.add_argument('-c', '--cmd', required=True,
                        help='Command to execute inside the container')

    args = parser.parse_args()

    print(args.marathon_id)
    print(args.cmd)
