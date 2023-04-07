# ChatGPT-python-interface
You don't need API key, this simple project use selenium to communicate beetwen chatgpt website and your pc.
install all libs in requierements.txt.
This code work on window11. On linux only "exec_term_code" doesn't work well. 
When using the code for the first time, go to main change last line by:

if __name__ == "__main__":
    gpt_driver.create_user_data()

run the code, connect to chatgpt and then wait 60s the code to stop. then change back the code and run again.
You can chose manually GPT4 before the first prompt got sent.
