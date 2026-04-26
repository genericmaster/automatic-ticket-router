from dotenv import load_dotenv
from firebase_admin import auth
import os
import logging
from flask import Flask,request,send_file,jsonify
from flask_cors import CORS
from ollama_client import Route_email
from router import Route_decision
from notifier import handler
from database import save_to_db, redirect_ticket_db, get_managers, add_manager, update_manager, delete_manager
from config import CONFIDENCE_THRESHOLD,ADMINS

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
    if int(DECISION["confidence_rating"])>=CONFIDENCE_THRESHOLD and int(DECISION["confidence_rating"])<=100:
      subject = "new ticket routed to you"
      flagged = False
    else:
        subject = "⚠️ LOW CONFIDENCE — Please verify this routing"
        flagged = True
       
    save_to_db(DECISION,HANDLER,flagged)
    handler(HANDLER,DECISION,subject)
    return  "Ticket routed successfully"


@app.route('/form', methods=['GET'])
def front():
   return send_file(os.path.join(FRONTEND_DIR, 'form.html'))

@app.route('/dashboard',methods=['GET'])
def dashboard():
    return send_file(os.path.join(FRONTEND_DIR, 'dashboard.html'))
@app.route('/ticket-detail', methods=['GET'])
def ticket_detail():
    return send_file(os.path.join(FRONTEND_DIR, 'ticket-detail.html'))

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
    manager_list = get_managers()
    new_manager = next((m for m in manager_list if m['DEPARTMENT'] == new_department), None)
    ticket_data = redirect_ticket_db(ticket_id, new_manager, new_department)
    
    mapped_data = {
    "department": ticket_data["DEPARTMENT"],
    "reason": ticket_data["REASON"],
    "original_email_text": ticket_data["ACTUAL_TICKET"],
    "confidence_rating": ticket_data["CONFIDENCE"]
    }   
    handler(new_manager, mapped_data) 

    return "success"
    
@app.route ('/login',methods=['GET'])
def login():
  return send_file(os.path.join(FRONTEND_DIR, 'login.html'))    

@app.route ('/role-check',methods=['POST'])
def role_check():
    try:
        data=request.get_json()
        token_id = data['token']
        verify_token = auth.verify_id_token(token_id)
        email = verify_token['email']
        manager_list=get_managers()
        print(email)
        if any(email == m['EMAIL'] for m in manager_list):
         return jsonify({ "role": "manager" })
        elif email in ADMINS:
         return jsonify({ "role": "admin" })
        else:
           return jsonify({ "role": "unknown" })
           
    except:
      logging.error("user not found")
      return jsonify({ "role": "unknown" })
      
@app.route ("/admin",methods=['GET'])
def admin():
   return send_file(os.path.join(FRONTEND_DIR, 'admin.html'))    

@app.route('/add-manager', methods=['POST'])
def add_manager_route():
    try:
        data = request.get_json()
        token = data['token']
        verified = auth.verify_id_token(token)
        email = verified['email']
        if email not in ADMINS:
            return jsonify({"error": "unauthorized"}), 403
        add_manager(data['name'], data['email'], data['department'])
        return jsonify({"success": True})
    except Exception as e:
        logging.error(e)
        return jsonify({"error": "failed"}), 500

@app.route('/update-manager', methods=['POST'])
def update_manager_route():
    try:
        data = request.get_json()
        token = data['token']
        verified = auth.verify_id_token(token)
        email = verified['email']
        if email not in ADMINS:
            return jsonify({"error": "unauthorized"}), 403
        update_manager(data['doc_id'], data['name'], data['email'], data['department'])
        return jsonify({"success": True})
    except Exception as e:
        logging.error(e)
        return jsonify({"error": "failed"}), 500

@app.route('/delete-manager', methods=['POST'])
def delete_manager_route():
    try:
        data = request.get_json()
        token = data['token']
        verified = auth.verify_id_token(token)
        email = verified['email']
        if email not in ADMINS:
            return jsonify({"error": "unauthorized"}), 403
        delete_manager(data['doc_id'])
        return jsonify({"success": True})
    except Exception as e:
        logging.error(e)
        return jsonify({"error": "failed"}), 500 
    
if __name__ == "__main__":
   app.run()