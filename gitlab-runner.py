from __future__ import print_function
import signal
import sys
import os
import subprocess
from time import sleep

GITLAB_URL = os.environ['GITLAB_URL']
GITLAB_REGISTRATION_TOKEN = os.environ['GITLAB_REGISTRATION_TOKEN']
DOCKER_IMAGE_DESCRIPTION = os.environ['DOCKER_IMAGE_DESCRIPTION']
DOCKER_IMAGE = os.environ['DOCKER_IMAGE']


def run_cmd(cmd):
    p = subprocess.call(cmd, shell=True)
    if p != 0:
        raise Exception("Error running command {}".format(cmd))


def sigterm_handler(_signo, _stack_frame):
    print("Attempting to unregister runner...")
    # get token
    cmd = "cat /etc/gitlab-runner/config.toml | grep -Po 'token = \"\K[0-9a-z]+'"
    token = subprocess.check_output(cmd, shell=True)
    cmd = "/usr/bin/gitlab-runner unregister -u {} -t {}".format(GITLAB_URL, token.strip())
    run_cmd(cmd)

    sys.exit(0)


def run():
    signal.signal(signal.SIGINT, sigterm_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)

    # register the runner
    cmd = "gitlab-runner register " \
          "--non-interactive " \
          "--url {} " \
          "--registration-token {} " \
          "--description {} " \
          "--executor docker " \
          "--docker-image {}".format(GITLAB_URL, GITLAB_REGISTRATION_TOKEN, DOCKER_IMAGE_DESCRIPTION, DOCKER_IMAGE)
    run_cmd(cmd)

    # start the runner
    cmd = "/usr/bin/gitlab-runner run &"
    run_cmd(cmd)

    while True:
        # wait for a sigterm or sigint
        # print("sleeping...")
        sleep(1)

if __name__ == '__main__':
    run()
