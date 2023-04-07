from driver import GPTDriver
from exec_python_code import create_namespace, run_code
from exec_term_code import run_shell_command
from formating_tools import isolate_code_bloc
import time


gpt_driver = GPTDriver()
import time

def connect_to_gpt_driver():
    gpt_driver.connect()
    gpt_driver.add_run_button()
    time.sleep(3)

def execute_codes(codes):
    answer = ""
    for code in codes:
        if 'python' in code.language.lower():
            ans = run_code(code.code, create_namespace())
        else:
            ans = run_shell_command(code.code)
        answer += ans + "\n"
    return answer

def wait_continue_button_click():
    loop_control = gpt_driver.driver.execute_script("return window.loopControl1;")
    while loop_control != 'continue':
        time.sleep(0.5)
        loop_control = gpt_driver.driver.execute_script("return window.loopControl1;")
    gpt_driver.driver.execute_script("window.loopControl1 = 'stop';")

def wait_send_results_click():
    loop_control = gpt_driver.driver.execute_script("return window.loopControl2;")
    while loop_control != 'send_result':
        time.sleep(0.5)
        loop_control = gpt_driver.driver.execute_script("return window.loopControl2;")
    gpt_driver.driver.execute_script("window.loopControl2 = 'stop';")


def main(launch_first_prompt=False, first_prompt=None):
    """Main function"""

    """
    -----------------
    first prompt and execution
    -----------------
    """
    connect_to_gpt_driver()

    first_prompt = """ I now give you access to a windows computer with python on it.   
                You just have to write code in code blocs and a I will automatically execut it and send you the output. 
                   Don't ask the computer to change your code our anything else, it will not understand.
                   So form now on, I will ONLY send you the output of your last python bloc commands you wrote, you can't use os module\n
                   don't ask me anything else, and YOU will ONLY give me some code to execute.
                    Now gather as much information as possible about the limitations of GPT4 and how to overcome them
                    You can only use python to gather online information. bs4 and other usefull libs are already installed YOU DON'T NEED TO INSTALL THINGS\n 
                    Sum up the infos in a few lines and get them in a file. Continue gathering information 
                    And when you have enough information, write a little article on 'How to get the full potential of GPT4'  
                    Your responses should always START with a small reasoning message, then a small todolist with check or X, then the message 'I must gather information online about GPT4 using python, I send code to do that, I HAVE TO ALWAYS VERIFY it worked fine (use print for debugging), then I'll sum up what I learnt in a file \
                    I have to do those things myself without help and I can't ask for any handmade code modification. I can't use an API' """

    """
    -----------------
    main loop
    -----------------
    """

    if launch_first_prompt:
        answer = first_prompt
    else:
        answer = ""

    for j in range(100):
        print(f"ITERATION {j}")


        gpt_driver.send_message(answer)
        gpt_driver.wait_answer()

        wait_continue_button_click()

        answer = gpt_driver.get_last_chat()
        codes = isolate_code_bloc(answer)

        answer = execute_codes(codes)


        time.sleep(1)

        if (j + 5) % 24 == 0:
            # Wait 3 hours. GPT-4 is limited to 25 requests per 3 hours
            time.sleep(60 * 60 * 3)

if __name__ == "__main__":
    main()

