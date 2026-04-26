import requests
import json
from config import OLLAMA_URL,STREAM,MODEL_NAME,THINK
from database import get_prompt,get_examples


def Route_email(email):
  EXAMPLES = get_examples()
   
  correct_examples = [ex for ex in EXAMPLES if ex.get('TYPE') == 'correct']
  redirected_examples = [ex for ex in EXAMPLES if ex.get('TYPE') == 'redirected']

  examples_text = ""
  if correct_examples:
    examples_text += "Examples of CORRECTLY routed tickets (the routing was right):\n\n"
    for ex in correct_examples:
        examples_text += f"Ticket: {ex['TICKET']}\nDepartment: {ex['DEPARTMENT']}\nReason: {ex['REASON']}\n\n"

  if redirected_examples:
    examples_text += "Examples of INCORRECTLY routed tickets (the routing was wrong and was redirected):\n\n"
    for ex in redirected_examples:
        examples_text += f"Ticket: {ex['TICKET']}\nOriginally routed to: {ex.get('ORIGINAL_DEPARTMENT', 'UNKNOWN')}\nCorrect department: {ex['DEPARTMENT']}\nReason: {ex['REASON']}\n\n"
        
  PROMPT = get_prompt()
  PROMPT = PROMPT.replace("{email}", examples_text + "\nHere is the new ticket:\n{email}")
  prompt = PROMPT.format(email=email)
  

  requests_body = {"model": MODEL_NAME,
                   'prompt':prompt,
                    "stream":STREAM,"think":THINK
  }

  request=requests.post(url=OLLAMA_URL,json=requests_body)
  returned_object=request.json()
  RESPONSE = returned_object["response"]
  RESPONSE = RESPONSE.replace('```json', '').replace('```', '').strip()
  output=json.loads(s=RESPONSE)

  return output

