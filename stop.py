import os

import psutil


def is_process_running():
    thread_pid = get_thread_pid()
    if thread_pid:
        return psutil.pid_exists(thread_pid)
    return False


def get_thread_pid():
    if os.path.exists("./process.pid"):
        with open("./process.pid", "r") as f:
            return int(f.read())
    return None


if __name__ == "__main__":
    if is_process_running():
        thread_pid = get_thread_pid()
        print("Process is running. Terminating it and all its children...")
        parent = psutil.Process(thread_pid)
        for child in parent.children(recursive=True):
            child.terminate()
        print("Terminating main thread...")
        parent.terminate()
        print("All processes have been terminated.")
    else:
        print("Process is not running.")
