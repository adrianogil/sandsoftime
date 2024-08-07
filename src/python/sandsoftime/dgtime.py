""" Dagger of Time script """
from pyutils.cli.clitools import run_cmd
from pyutils.cli.flags import verify_flag
from pyutils.utils.jsonutils import write_to_file, read_json_file

import os
import sys
import json
import time
import datetime


def get_jobs_data_path():
    data_file_path = os.path.join(os.environ["SANDSOFTIME_DIR"], "data.json")

    if 'SANDSOFTIME_DATAFILE' in os.environ:
        data_file_path = os.environ["SANDSOFTIME_DATAFILE"]

    return data_file_path


def load_data():
    data_file_path = get_jobs_data_path()

    jobs_data = {"commands": []}

    if not os.path.exists(data_file_path):
        return jobs_data

    jobs_data = read_json_file(data_file_path)

    return jobs_data


def save_data(jobs_data):
    data_file_path = get_jobs_data_path()

    with open(data_file_path, 'w') as f:
        json.dump(jobs_data, f)


def save_command(interval_minutes, command, target_directory):
    current_time  = datetime.datetime.today().strftime('%Y.%m.%d-%Hh%mm')
    new_command_data = {
        "interval":   int(interval_minutes),
        "command":    command,
        "start_time": current_time,
        "last_time": current_time,
        "target_directory": target_directory,
        "times_ran": 0,
        "errors": []
    }
    jobs_data = load_data()

    if 'commands' not in jobs_data:
        jobs_data['commands'] = []
    jobs_data['commands'].append(new_command_data)

    save_data(jobs_data)


def run_command(target_command, target_directory):
    print("# Dagger of Time - Running command: \n%s" % (target_command))
    print("########################################")
    target_command = 'cd "%s" && %s' % (target_directory, target_command)
    command_output = run_cmd(target_command, load_bashrc=True)
    print(command_output)
    print("")


def verify_commands_to_run():
    jobs_data_path = get_jobs_data_path()
    jobs_data = load_data()

    for jobtask in jobs_data['commands']:

        today = datetime.datetime.today()

        last_time = datetime.datetime.strptime(jobtask["last_time"], "%Y.%m.%d-%Hh%Mm")
        last_time_minutes = int((today - last_time).seconds / 60)

        if last_time_minutes > jobtask["interval"]:
            try:
                run_command(jobtask["command"], jobtask["target_directory"])
            except Exception as e:
                print("Error running command: %s" % jobtask["command"])
                print(e)
                jobtask["errors"].append(str(e))
            jobtask["last_time"] = today.strftime('%Y.%m.%d-%Hh%Mm')
            jobtask["times_ran"] += 1

    write_to_file(jobs_data_path, jobs_data)
    print("Update file %s" % jobs_data_path)


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


def print_usage():
    print("Usage: dgtime [interval_minutes] [command]")
    print("       dgtime -l | --list")


if __name__ == "__main__":
    if verify_flag(["-h", "--help"]):
        print_usage()
    elif verify_flag(["-l", "--list"]):
        list_scheduled_commands()
    elif len(sys.argv) >= 3:
        interval_minutes = sys.argv[1]
        command = sys.argv[2]
        if len(sys.argv) > 3:
            target_directory = sys.argv[3]
        else:
            target_directory = os.getcwd()
        save_command(interval_minutes, command, target_directory)
    else:
        run_commands_loop()
