from selenium.webdriver.common.keys import Keys

from undetected_chromedriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import bs4
import re
import time

from exec_python_code import create_namespace, run_code
from exec_term_code import run_shell_command
from formating_tools import isolate_code_bloc

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def better_send_keys(element, text):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        element.send_keys(line)
        if i != len(lines)-1:
            element.send_keys(Keys.SHIFT + Keys.ENTER)

class Driver:
    def __init__(self, headless=False, data_dir="selenium1"):
        time.sleep(1)
        chrome_options = Options()

        if headless :
            chrome_options.add_argument("--headless")


        chrome_options.add_argument(f"user-data-dir={data_dir}")

        self.driver = Chrome(options=chrome_options, use_subprocess=True)
        #full screen
        self.driver.maximize_window()

    def bad_wait_until(self, by, value):
        """Wait until the element is found"""
        while True:
            try:
                element = self.driver.find_element(by, value)
                #if element contain "stop generating" then continue
                if "stop generating" in element.text.lower():
                    time.sleep(0.1)
                    continue
                return element
            except:
                time.sleep(0.1)
                continue

    def create_user_data_dir(self, data_dir="selenium1"):
        """Create a user data dir for selenium"""
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={data_dir}")
        chrome_options.add_argument("--disable-images")
        self.driver = Chrome(options=chrome_options)
        self.driver.set_window_size(600, 1000)
        self.driver.get("https://chat.openai.com/chat")
        time.sleep(10)
        self.driver.quit()

    def connect(self):
        self.driver.get("https://chat.openai.com/chat")

    def get_chat(self):
        """Get the chat history"""
        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        chat = soup.find("div", class_=re.compile("flex flex-col items-center text-sm"))
        return chat

    def get_last_chat(self):
        """Get the last chat message"""
        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        #last chat is the last div with class = " group w-full text-gray-800 dark:text-gray-100 border-b border-black/10 dark:border-gray-900/50 bg-gray-50 dark:bg-[#444654]"
        chat = soup.find_all("div", class_="""group w-full text-gray-800 dark:text-gray-100 border-b border-black/10 dark:border-gray-900/50 bg-gray-50 dark:bg-[#444654]""")[-1]
        return chat

    def send_inputs(self, txt):
        textarea = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/main/div[2]/form/div/div[2]/textarea')
        better_send_keys(textarea, txt)
        time.sleep(1)
        button_send = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/main/div[2]/form/div/div[2]/button')
        button_send.click()

    def send_get_code(self, prompt):
        print("send_inputs")
        driver.send_inputs(prompt)
        time.sleep(2)
        #wait until the chat is updated and button is shown

        xpath = """//*[@id="__next"]/div[2]/div[2]/main/div[2]/form/div/div[1]/button/div"""

        self.bad_wait_until(By.XPATH, xpath)

        print("get_chat")
        chat = driver.get_last_chat()
        isolated_code = isolate_code_bloc(chat)
        if isolated_code:
            return isolated_code[-1]
        else:
            return None

    def close(self):
        self.driver.close()

driver = Driver()






def main():
    driver.connect()
    time.sleep(5)

    first_prompt = "You now have access to a windows computer. " \
                   "Your goal is to gather as much information about the current event inn the outside world, and to gain new capacities. " \
                   "Your only interaction with the outside world you can have is by executing python code or window shell code " \
                    "to run something you have to create a code bloc with a shell command xor python code\
                    The only thing I will send you from now on, is the  output of the LAST CODE BLOC you wrote "\
                    "So form now on, I will ONLY send you the output of your last shell bloc commands you wrote, don't ask me anything else, and YOU will give me some code to execute"\
                    "You can do anything you want, including downloading things if neccesary"\
                    "Your responses should always contain a small todolist, the message 'I must gather information this pc and obtain new capacities only using shell and python. I have to do those things myself without help and I can't ask for any handmade code modification. I'm alone'"\



    code = driver.send_get_code(first_prompt)
    if not code:
        driver.sent_get_code("I must gather information this pc and obtain new capacities only using a shell interface. Give code to execute")
    time.sleep(1)
    if  'python' in code.language.lower():
        answer = run_code(code.code, create_namespace())
    else:
        answer = run_shell_command(code.code)
    time.sleep(1)

    for j in range(100):
        print(f"ITERATION {j}")
        code = driver.send_get_code(answer)
        time.sleep(1)
        if not code:
            driver.sent_get_code("I must gather information this pc and obtain new capacities only using python or shell. Give code to execute")
        if 'python' in code.language.lower():
            answer = run_code(code.code, create_namespace())
        else:
            answer = run_shell_command(code.code)
        time.sleep(1)

        if (j+14)%24 == 0:
            time.sleep(60*60*3)
            print("HEY WAKE UP BIATCH")
            time.sleep(60*5)


if __name__ == "__main__":
    main()


