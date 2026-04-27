from dotenv import load_dotenv
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))
from firebase_admin import auth
import logging
from flask import Flask,request,send_file,jsonify
from flask_cors import CORS
from services.ticket_service import process_ticket
from services.redirect_service import  redirect_ticket_service
from database import get_managers, add_manager, update_manager, delete_manager,get_clients
from config import ADMINS

FRONTEND_DIR = os.path.join(BASE_DIR, 'pages')

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'pages', 'static'))

#locks down which origin can make requests to the backend
CORS(app, origins=["http://127.0.0.1:5000", "http://localhost:5000"])

@app.route('/ticket', methods=['POST'])
def handle_ticket():
    data = request.get_json()
    
    if not data:
     return jsonify({"error": "invalid request"}), 400
    token = data.get('token')
    email = data.get('email')

    if not token or not email:
        return jsonify({"error": "token and email are required"}), 400
    try:
        verified = auth.verify_id_token(token)
        client_email = verified['email']
    except:
        return jsonify({"error": "unauthorized"}), 401
    try:
       return process_ticket(email,client_email)
    except Exception as e:
        logging.error(e)
        return jsonify({"error": "something went wrong"}), 500


@app.route ('/client',methods=['GET'])
def client():
      return send_file(os.path.join(FRONTEND_DIR,'client', 'client.html'))
@app.route('/form', methods=['GET'])
def form():
   return send_file(os.path.join(FRONTEND_DIR,'form', 'form.html'))
@app.route('/dashboard',methods=['GET'])
def dashboard():
    return send_file(os.path.join(FRONTEND_DIR, 'dashboard', 'dashboard.html'))
@app.route('/ticket-detail', methods=['GET'])
def ticket_detail():
    return send_file(os.path.join(FRONTEND_DIR,'ticket-detail', 'ticket-detail.html'))

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
    try:
        data = request.get_json()
        if not data:
         return jsonify({"error": "invalid request"}), 400
        ticket_id = data["ticket_id"]
        new_department = data["new_department"]
    except KeyError as e:
     return jsonify({"error": "department not found"}), 404
    try:
       return  redirect_ticket_service(ticket_id,new_department)
    except Exception as e:
     logging.error(e)
     return jsonify({"error": "something went wrong"}), 500

    
@app.route ('/login',methods=['GET'])
def login():
  return send_file(os.path.join(FRONTEND_DIR,'login', 'login.html'))    

@app.route ('/role-check',methods=['POST'])
def role_check():
    try:
        data=request.get_json()
        token_id = data['token']
        verify_token = auth.verify_id_token(token_id)
        email = verify_token['email']
        manager_list=get_managers()
        if email in ADMINS:
         return jsonify({ "role": "admin" })
        
        elif any(email == m['EMAIL'] for m in manager_list):
         return jsonify({ "role": "manager" })
        
        elif any(email == c['EMAIL'] for c in get_clients()):
          return jsonify({ "role": "client" })
        else:
           return jsonify({ "role": "unknown" })
           
    except Exception as e:
       logging.error(f"Role check failed: {e}")
       return jsonify({ "role": "unknown" })
@app.route ("/admin",methods=['GET'])
def admin():
   return send_file(os.path.join(FRONTEND_DIR,'admin', 'admin.html'))    

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