""" Dagger of Time script """
from pyutils.cli.flags import verify_flag

import os
import sys
import json
import time
import datetime
import subprocess


def get_jobs_data_path():
    data_file_path = os.path.join(os.environ["SANDSOFTIME_DIR"], "data.json")

    if 'SANDSOFTIME_DATAFILE' in os.environ:
        data_file_path = os.environ["SANDSOFTIME_DATAFILE"]

    return data_file_path


def load_data():
    data_file_path = get_jobs_data_path()

    jobs_data = {}

    if not os.path.exists(data_file_path):
        return jobs_data

    with open(data_file_path, 'r') as f:
        jobs_data = json.load(f)

    return jobs_data


def save_data(jobs_data):
    data_file_path = get_jobs_data_path()

    with open(data_file_path, 'w') as f:
        json.dump(jobs_data, f)


def save_command(interval_minutes, command):
    new_command_data = {
        "interval":   int(interval_minutes),
        "command":    command,
        "start_time": datetime.datetime.today().strftime('%Y.%m.%d-%Hh%mm')
    }
    jobs_data = load_data()

    if 'commands' not in jobs_data:
        jobs_data['commands'] = []
    jobs_data['commands'].append(new_command_data)

    save_data(jobs_data)


def run_command(target_command):
    print("# Dagger of Time - Running command: \n%s" % (target_command))
    print("########################################")
    subprocess_cmd = target_command
    subprocess_output = subprocess.check_output(subprocess_cmd, shell=True)
    subprocess_output = subprocess_output.decode("utf8")
    subprocess_output = subprocess_output.strip()
    print(subprocess_output)
    print("")


def verify_commands_to_run():
    jobs_data = load_data()
    today = datetime.datetime.today()

    for jobtask in jobs_data['commands']:
        start_time = datetime.datetime.strptime(jobtask["start_time"], "%Y.%m.%d-%Hh%Mm")
        minutes = int((today - start_time).seconds / 60)

        if minutes % jobtask["interval"] == 0:
            run_command(jobtask["command"])


def list_scheduled_commands():
    jobs_data = load_data()

    if 'commands' not in jobs_data:
        print("No command was saved yet!")
        return

    for commands in jobs_data["commands"]:
        print("- %s (%s)" % (commands["command"], commands["interval"]))


def run_commands_loop():
    min_verification_time = 60

    while True:
        verify_commands_to_run()
        time.sleep(min_verification_time)


if __name__ == "__main__":
    if verify_flag("-l") or verify_flag("--list"):
        list_scheduled_commands()
    elif len(sys.argv) == 3:
        interval_minutes = sys.argv[1]
        command = sys.argv[2]
        save_command(interval_minutes, command)
    else:
        run_commands_loop()
