from termcolor import colored


def print_success(text):
    print(colored(text, "green"))

def print_error(text):
    print(colored(text, "red"))

def print_warning(text):
    print(colored(text, "yellow"))