from driver import GPTDriver
from exec_python_code import create_namespace, run_code
from exec_term_code import run_shell_command
from formating_tools import isolate_code_bloc
import time


gpt_driver = GPTDriver()

def main():
    gpt_driver.connect()
    time.sleep(5)

    first_prompt = "You now have access to a windows computer. " \
                   "Your goal is to gather as much information about the current event in the outside world, and to gain new capacities. " \
                   "Your only interaction with the outside world you can have is by executing python code or window shell code " \
                    "to run something you have to create a code bloc with a shell command xor python code\
                    The only thing I will send you from now on, is the  output of the LAST CODE BLOC you wrote "\
                    "So form now on, I will ONLY send you the output of your last shell bloc commands you wrote, don't ask me anything else, and YOU will ONLY give me some code to execute."\
                    "You can do anything you want, including downloading things if neccesary"\
                    "Your responses should always contain a small todolist, the message 'I must gather information this pc and obtain new capacities only using shell and python. I have to do those things myself without help and I can't ask for any handmade code modification. I'm alone'"\



    codes  = gpt_driver.send_get_code(first_prompt)
    answer = ""
    while not codes:
        codes  = gpt_driver.send_get_code("I must gather information this pc and obtain new capacities only using python or shell. Give code to execute")
    for code in codes:
        if 'python' in code.language.lower():
            ans = run_code(code.code, create_namespace())
        else:
            ans = run_shell_command(code.code)
        answer += ans + "\n"

    time.sleep(1)

    for j in range(100):
        print(f"ITERATION {j}")
        codes  = gpt_driver.send_get_code(answer)
        while not codes:
            codes  = gpt_driver.send_get_code("I must gather information this pc and obtain new capacities only using python or shell. Give code to execute")
        answer = ""
        count = 0
        for code in codes:
            count += 1
            if 'python' in code.language.lower():
                ans = run_code(code.code, create_namespace())
            else:
                ans = run_shell_command(code.code)
            answer += f"CODE BLOC {count}: OUTPUT:\n{ans}\n -------\n"
        time.sleep(1)


        if (j+1)%24 == 0:
            #wait 3 hours GPT-4 is limited to 25 requests per 3 hours
            time.sleep(60*60*3)


if __name__ == "__main__":
    main()
