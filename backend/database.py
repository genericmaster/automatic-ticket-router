from firebase_admin import credentials,firestore,initialize_app

Service_account = credentials.Certificate('backend/serviceAccountKey.json')
app = initialize_app(Service_account)
db = firestore.client(app)

def save_to_db(decision,manager,flagged):
     db.collection('tickets').add({
        "DEPARTMENT": decision["department"],
        "MANAGER": decision["manager"],
        "MANAGER_EMAIL": manager["EMAIL"],
        "ACTUAL_TICKET": decision["original_email_text"],
        "REASON": decision["reason"],
        "CONFIDENCE": decision["confidence_rating"],
        "timestamp": firestore.SERVER_TIMESTAMP,
        "feedback": None,
        "flagged": flagged,
        "original_manager_email": manager["EMAIL"]
        
    })
     
def get_managers():
    managers=[]
    for doc in db.collection('manager').stream():
        managers.append(doc.to_dict())
     
    return managers

def redirect_ticket_db(ticket_id, new_manager, new_department):
    current = db.collection('tickets').document(ticket_id).get().to_dict()
    original_dept = current.get('DEPARTMENT', 'UNKNOWN')
    db.collection('tickets').document(ticket_id).update({
        "MANAGER": new_manager["NAME"],
        "DEPARTMENT": new_department,
        "MANAGER_EMAIL": new_manager["EMAIL"],
        "redirected": True,
        "original_department": original_dept
    })
    ticket_data = db.collection('tickets').document(ticket_id).get().to_dict()

    return ticket_data

def add_manager(name, email, department):
    db.collection('manager').add({
        "NAME": name,
        "EMAIL": email,
        "DEPARTMENT": department
    })

def update_manager(doc_id, name, email, department):
    db.collection('manager').document(doc_id).update({
        "NAME": name,
        "EMAIL": email,
        "DEPARTMENT": department
    })

def delete_manager(doc_id):
    db.collection('manager').document(doc_id).delete()

def get_prompt():
    docs=db.collection('prompt').limit(1).stream()
    for doc in docs:
        return doc.to_dict()['PROMPT']
def get_examples():
    examples = []
    correct = [doc.to_dict() for doc in db.collection('examples').where('TYPE', '==', 'correct').limit(5).stream()]
    redirected = [doc.to_dict() for doc in db.collection('examples').where('TYPE', '==', 'redirected').limit(5).stream()]
    examples = correct + redirected
    return examples