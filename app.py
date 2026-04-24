from flask import Flask,request
from ollama_client import Route_email
from router import  Route_decision
from notifier import handler
from config import MANAGERS

app = Flask(__name__)

@app.route('/ticket', methods=['POST'])
def handlet_icket():
    print("Request received")
    data = request.get_json()
    email =data['email']
    DECISION=Route_email(email)
    HANDLER=Route_decision(DECISION)
    llm_response =handler(HANDLER,DECISION)

    
    return  "Ticket routed successfully"


if __name__ == "__main__":
   app.run(debug=True, use_reloader=False)
   app.run()