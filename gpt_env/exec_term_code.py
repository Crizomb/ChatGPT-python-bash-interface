import os
import subprocess
import time

class Shell:
    def __init__(self):
        self.cwd = os.getcwd()
        self.env = os.environ.copy()
        if os.name == 'nt':
            self.env['PATH'] += os.pathsep + os.getcwd()

    def run_command(self, command_string, input=None):
        exit_code, stdout, stderr = 1, 'error', 'error'
        if input is not None:
            input = input.encode('utf-8')

        commands = command_string.split('\n')
        results = []
        for command in commands:
            command = command.strip()
            args = command.split(" ")

            if args[0] == 'cd':
                if len(args) > 1:
                    path = os.path.join(self.cwd, args[1])
                    if os.path.exists(path) and os.path.isdir(path):
                        self.cwd = os.path.abspath(path)
                        exit_code, stdout, stderr = 0, '', ''
                    else:
                        exit_code, stdout, stderr = 1, '', f"cd: {path}: No such file or directory"

            elif os.name == 'nt':
                result = subprocess.run(command, cwd=self.cwd, env=self.env, input=input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=False)
                exit_code, stdout, stderr = result.returncode, result.stdout.decode('utf-8', errors='ignore'), result.stderr.decode('utf-8', errors='ignore')
            else:
                result = subprocess.run(args, cwd=self.cwd, env=self.env, input=input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=False)
                exit_code, stdout, stderr = result.returncode, result.stdout.decode('utf-8',errors='ignore'), result.stderr.decode('utf-8', errors='ignore')

            results.append((command, exit_code, stdout, stderr))



        str_results = ""
        for result in results:
            command,exit_code, stdout, stderr = result
            str_results += f"result for command: {command} :\n exit_code: {exit_code}\n stdout: {stdout}\n stderr: {stderr}\n---------\n"

        return str_results

shell = Shell()

def run_shell_command(command_string, input=None):
    return shell.run_command(command_string, input)

def test():
    a = run_shell_command("cd ..\n\ndir")
    print(type(a))
    print(a)

if __name__ == '__main__':
    test()




