#contains business logic such as routing decsion and confifrnce logic
from router import Route_decision
from ollama_client import Route_email
from config import CONFIDENCE_THRESHOLD
from database import save_to_db
from notifier import handler

def  is_flagged(confidence):
       return not (int(confidence) >= CONFIDENCE_THRESHOLD and int(confidence) <= 100)
     
def process_ticket(email,client_email):
        DECISION = Route_email(email)
        HANDLER = Route_decision(DECISION)
        flagged=is_flagged(DECISION["confidence_rating"])
        if not flagged:
            subject = "new ticket routed to you"    
        else:
            subject = "⚠️ LOW CONFIDENCE — Please verify this routing"
        save_to_db(DECISION,HANDLER,flagged,client_email)
        handler(HANDLER,DECISION,subject)
        return  "Ticket routed successfully"

         
    

     