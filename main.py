from config import *
from db import db_session
from tui import App


def main():
    db_session.global_init(db_file=db_file)
    application = App()
    application.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
