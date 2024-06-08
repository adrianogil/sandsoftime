from pyutils.cli.clitools import run_cmd

import sys
import time
import subprocess


time_interval = sys.argv[1]
target_command = sys.argv[2]

run_index = 1

while True:
    print("# Watch tool, running command: (%s) \n%s" % (
        run_index, target_command))
    print("########################################")
    subprocess_cmd = target_command
    subprocess_output = run_cmd(target_command, load_bashrc=True, live_log=True)
    print(subprocess_output)
    print("")
    time.sleep(int(time_interval))

    run_index = run_index + 1
