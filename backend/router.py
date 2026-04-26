from database import get_managers
import logging


def Route_decision(decision):
    DEPARTMENT = decision["department"]
    manager_list=get_managers()
    manager = next((m for m in manager_list if m['DEPARTMENT'] == DEPARTMENT), None)
    if manager:
     return manager
    else:
     logging.error("no department matched")
