from database import get_managers,redirect_ticket_db
from notifier import handler

def find_manager_by_department(manager_list, new_department):
    return next((m for m in manager_list if m['DEPARTMENT'] == new_department), None)

def redirect_ticket_service(ticket_id,new_department):
        manager_list = get_managers()
        new_manager = find_manager_by_department(manager_list,new_department)
        ticket_data = redirect_ticket_db(ticket_id, new_manager, new_department)
        mapped_data = {
            "department": ticket_data["DEPARTMENT"],
            "reason": ticket_data["REASON"],
            "original_email_text": ticket_data["ACTUAL_TICKET"],
            "confidence_rating": ticket_data["CONFIDENCE"]
            }   
        handler(new_manager, mapped_data) 

        return "success"