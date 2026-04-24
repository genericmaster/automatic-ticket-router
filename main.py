from ollama_client import Route_email
from router import  Route_decision
from notifier import handler
from config import MANAGERS

email = " Subject: Critical system failure backup not responding. Body: Hi our primary database went down this morning and the backup system is not responding. We are unable to access any student records"

DECISION=Route_email(email)
HANDLER=Route_decision(DECISION)
print(handler(HANDLER,DECISION))

