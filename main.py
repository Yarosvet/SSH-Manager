from config import *
from db import db_session
from tui import App
from threading import Thread
from os import mkdir, path
import sys
import curses

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
    if not path.exists(db_dir):
        mkdir(db_dir)
    db_session.global_init(db_file=path.join(db_dir, db_file))
    application = App()
    application.set_var_actOnExit(set_act_on_exit)
    application.run()


if __name__ == "__main__":
    try:
        tui_thread = Thread(target=main, daemon=True)
        tui_thread.start()
        tui_thread.join()
        if action_on_exit is not None:
            action_on_exit(*args, **kwargs)
    except KeyboardInterrupt:
        curses.endwin()
        sys.exit()
