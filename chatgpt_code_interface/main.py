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

def main(launch_first_prompt=False, first_prompt=None):
    """Main function"""

    connect_to_gpt_driver()

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
           
 
def create_user_data():
    GPTDriver.create_user_data_dir()

if __name__ == "__main__":
    main()

