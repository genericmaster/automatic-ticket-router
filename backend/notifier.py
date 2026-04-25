import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content



sg =sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")

def handler(managers,decision):
    from_email = Email(SENDER_EMAIL)
    to_email= To(managers["email"])
    subject = "new ticket routed to you"
    body="Department: " + decision['department'] +"\nproblem: "+ decision['original_email_text'] +"\nReason: " + decision['reason']+"\nCONFIDENCE LEVEL: " + decision['confidence_rating']
    content = Content("text/plain",body)
    mail = Mail(from_email, to_email, subject, content)
    mail_json = mail.get()
    response = sg.client.mail.send.post(request_body=mail_json)
    return response