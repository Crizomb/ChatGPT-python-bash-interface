import bs4
from collections import namedtuple


CodeBloc = namedtuple('CodeBloc', ['language', 'code'])

def remove_trailing_newline(s):
    if s.endswith('\n'):
        return s[:-1]
    return s

def isolate_code_bloc(soup):
    """Get codes bloc from the raw html of chatgpt website return a CodeBloc"""
    pre_tab = soup.find_all("pre")
    code_bloc = []
    for code in pre_tab:
        #print(code.text)
        motif = "Copy code"
        finding = code.text.find(motif)
        code_content = code.text[finding+len(motif):]
        language = code.text[:finding]
        code_bloc.append(CodeBloc(language.strip(), remove_trailing_newline(code_content)))

    print(code_bloc)
    return code_bloc

