import subprocess
import sys
import os

def get_script_directory():
    # Get the file path of the running script
    script_path = os.path.realpath(__file__)
    
    # Get the directory path of the script
    script_dir = os.path.dirname(script_path)
    
    return script_dir

def activate_and_run_detached(script_path, venv_path):
    # Determine the activation command based on the operating system
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
        command = f'{activate_script} && python {script_path}'
        creation_flags = subprocess.CREATE_NEW_CONSOLE
    else:  # macOS / Linux
        activate_script = os.path.join(venv_path, 'bin', 'activate')
        command = f'/bin/bash -c "source {activate_script} && python {script_path}"'
        creation_flags = 0
    
    # Run the command in a detached process
    proc = subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
        creationflags=creation_flags
    )

    # Detach by not waiting for process completion
    proc.stdin.close()
    proc.stdout.close()
    proc.stderr.close()

if __name__ == "__main__":
    # Replace these paths with your specific paths
    # script_dir = '/path/to/your/script_directory'  # Path where the script is located
    # venv_dir = '/path/to/your/venv_directory'     # Path where the venv is located
    script_dir = get_script_directory()
    venv_dir = script_dir
    script_to_run = os.path.join(script_dir, 'window_switcher.py')  # Script to run

    # Call the function to activate the virtualenv and run the script
    activate_and_run_detached(script_to_run, venv_dir)
