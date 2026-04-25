from firebase_admin import credentials,firestore,initialize_app

Service_account = credentials.Certificate('backend/serviceAccountKey.json')
app = initialize_app(Service_account)
db = firestore.client(app)

def save_to_db(decision,manager):
     db.collection('tickets').add({
        "DEPARTMENT": decision["department"],
        "MANAGER": decision["manager"],
        "MANAGER_EMAIL": manager["email"],
        "ACTUAL_TICKET": decision["original_email_text"],
        "REASON": decision["reason"],
        "CONFIDENCE": decision["confidence_rating"],
        "timestamp": firestore.SERVER_TIMESTAMP,
        "feedback": None
    })

def redirect_ticket_db(ticket_id, new_manager, new_department):
    current = db.collection('tickets').document(ticket_id).get().to_dict()
    original_dept = current.get('DEPARTMENT', 'UNKNOWN')
    db.collection('tickets').document(ticket_id).update({
        "MANAGER": new_manager["name"],
        "DEPARTMENT": new_department,
        "MANAGER_EMAIL": new_manager["email"],
        "redirected": True,
        "original_department": original_dept
    })
    ticket_data = db.collection('tickets').document(ticket_id).get().to_dict()
    return ticket_data