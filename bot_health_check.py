import psutil
import os
import time
import subprocess


def is_script_running(script_name):
    current_pid = os.getpid()
    for process in psutil.process_iter(['pid', 'cmdline']):
        if process.info['pid'] != current_pid and process.info['cmdline'] and script_name in ' '.join(process.info['cmdline']):
            return True
    return False

def run_script_in_new_process(script_path):
    try:
        process = subprocess.Popen(['python', script_path])
        #process.wait()  # Wait for the script to complete (optional)
    except FileNotFoundError:
        print(f"Error: Script not found at path: {script_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

script_name_to_check = "bot.py"
while True:
    if is_script_running(script_name_to_check):
        print(f"[HEALTH CHECKER] The script '{script_name_to_check}' is running.")
    else:
        print(f"[HEALTH CHECKER] The script '{script_name_to_check}' is not running, trying to restart.")
        run_script_in_new_process(script_name_to_check)
    #check every 30 seconds
    time.sleep(30)