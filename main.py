from config import *
from db import db_session
from tui import App
from threading import Thread

action_on_exit = None
args = []
kwargs = {}


def set_act_on_exit(func, a_args, a_kwargs):
    global action_on_exit
    global args
    global kwargs
    action_on_exit = func
    args = a_args
    kwargs = a_kwargs


def main():
    global action_on_exit
    db_session.global_init(db_file=db_file)
    application = App()
    application.set_var_actOnExit(set_act_on_exit)
    application.run()


if __name__ == "__main__":
    try:
        tui_thread = Thread(target=main)
        tui_thread.start()
        tui_thread.join()
        if action_on_exit is not None:
            action_on_exit(*args, **kwargs)
    except KeyboardInterrupt:
        exit()
