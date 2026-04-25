from config import MANAGERS
import logging


def Route_decision(decision):
    DEPARTMENT = decision["department"]
    if DEPARTMENT in MANAGERS:
        return MANAGERS[DEPARTMENT]
    else:
        logging.error("no department matched")

