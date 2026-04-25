from dotenv import load_dotenv
import os
from flask import Flask,request,send_file,jsonify
from flask_cors import CORS
from ollama_client import Route_email
from router import Route_decision
from notifier import handler
from database import save_to_db, redirect_ticket_db
from config import MANAGERS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'pages')
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

app = Flask(__name__)

CORS(app)

@app.route('/ticket', methods=['POST'])
def handle_icket():
    data = request.get_json()
    email = data['email']
    DECISION = Route_email(email)
    HANDLER = Route_decision(DECISION)
    save_to_db(DECISION,HANDLER)
    handler(HANDLER,DECISION)
    return  "Ticket routed successfully"


@app.route('/form', methods=['GET'])
def front():
   return send_file(os.path.join(FRONTEND_DIR, 'form.html'))

@app.route('/dashboard',methods=['GET'])
def dashboard():
    return send_file(os.path.join(FRONTEND_DIR, 'dashboard.html'))

@app.route('/firebase-config', methods=['GET'])
def get_firebase_config():
    return jsonify({
        "apiKey": os.environ.get("FIREBASE_apiKey"),
        "authDomain": os.environ.get("FIREBASE_authDomain"),
        "projectId": os.environ.get("FIREBASE_projectId"),
        "storageBucket": os.environ.get("FIREBASE_storageBucket"),
        "messagingSenderId": os.environ.get("FIREBASE_messagingSenderId"),
        "appId": os.environ.get("FIREBASE_appId"),
        "measurementId": os.environ.get("FIREBASE_measurementId")
    })

@app.route('/redirect-ticket',methods=['POST'])
def redirect_ticket():
    data = request.get_json()
    ticket_id = data["ticket_id"]
    new_department = data["new_department"]
    new_manager = MANAGERS[new_department]
    ticket_data = redirect_ticket_db(ticket_id, new_manager, new_department)
    
    mapped_data = {
    "department": ticket_data["DEPARTMENT"],
    "reason": ticket_data["REASON"],
    "original_email_text": ticket_data["ACTUAL_TICKET"],
    "confidence_rating": ticket_data["CONFIDENCE"]
    }   
    handler(new_manager, mapped_data)
    
    return "success"
if __name__ == "__main__":
   app.run()