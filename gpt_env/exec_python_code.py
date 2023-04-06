import sys
import importlib.util
import io
import contextlib

def create_namespace():
    module_name = "__main__"
    module_spec = importlib.util.spec_from_loader(module_name, loader=None)
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_name] = module
    return module.__dict__

def run_code(code_str, namespace):
    # redirect stdout to a buffer to capture output
    if "import os" in code_str:
        return "Error: import os is not allowed. use direct shell command instead."
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        try:
            # compile the code
            code = compile(code_str, "<string>", "exec")

            # execute the code in the given namespace
            exec(code, namespace)
        except Exception as e:
            # print any errors to the buffer
            print(f"Error: {e}", file=buffer)

    # return the captured output or error message as a string
    result = buffer.getvalue().strip()
    if result:
        return result
    else:
        return "No output, maybe an error? maybe not."




def test():
    code_str1 = '''import numpy as np\nimport matplotlib.pyplot as plt'''
    code_str2 = '''x = np.linspace(0, 10, 100)\ny = np.sin(x)\nplt.plot(x, y)\nplt.show()'''
    code_str3 = '''tab = [0, 1, 2, 3]\nprint(tab[5])'''


    namespace = create_namespace()
    result1 = execute_code(code_str1, namespace)
    result2 = execute_code(code_str2, namespace)
    result3 = execute_code(code_str3, namespace)
    print(result1, result2, result3)

def test2():
    code_str1 = '''import os'''

    result = run_code(code_str1, create_namespace())
    print(result)

if __name__ == "__main__":
    test2()
