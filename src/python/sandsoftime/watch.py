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
    subprocess_output = subprocess.check_output(subprocess_cmd, shell=True)
    subprocess_output = subprocess_output.decode("utf8")
    subprocess_output = subprocess_output.strip()
    print(subprocess_output)
    print("")
    time.sleep(int(time_interval))

    run_index = run_index + 1
