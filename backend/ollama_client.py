import requests
import json
import logging
from config import OLLAMA_URL,STREAM,MODEL_NAME,THINK
from database import get_prompt,get_examples



def build_examples_text(correct_examples, redirected_examples):
    
    examples_text = ""
    if correct_examples:
      examples_text += "Examples of CORRECTLY routed tickets (the routing was right):\n\n"
      for ex in correct_examples:
        examples_text += f"Ticket: {ex['TICKET']}\nDepartment: {ex['DEPARTMENT']}\nReason: {ex['REASON']}\n\n"

    if redirected_examples:
      examples_text += "Examples of INCORRECTLY routed tickets (the routing was wrong and was redirected):\n\n"
      for ex in redirected_examples:
        examples_text += f"Ticket: {ex['TICKET']}\nOriginally routed to: {ex.get('ORIGINAL_DEPARTMENT', 'UNKNOWN')}\nCorrect department: {ex['DEPARTMENT']}\nReason: {ex['REASON']}\n\n"

    return examples_text

def build_prompt(email, examples_text):
    PROMPT = get_prompt()
    PROMPT = PROMPT.replace("{email}", examples_text + "\nHere is the new ticket:\n{email}")
    return PROMPT.format(email=email)



def validate_model_output(output):
  
    required_keys = ['department', 'manager', 'original_email_text', 'reason', 'confidence_rating']
    missing = [key for key in required_keys if key not in output]
    if missing:
        raise RuntimeError(f"Model response missing fields: {missing}")

def Route_email(email):
  EXAMPLES = get_examples()
  correct_examples = [ex for ex in EXAMPLES if ex.get('TYPE') == 'correct']
  redirected_examples = [ex for ex in EXAMPLES if ex.get('TYPE') == 'redirected']
  example_text= build_examples_text(correct_examples,redirected_examples)
  prompt = build_prompt(email,example_text)
  
  requests_body = {"model": MODEL_NAME,
                   'prompt':prompt,
                    "stream":STREAM,"think":THINK
  }
 # Try block 1 — HTTP request
  try:
    request = requests.post(url=OLLAMA_URL, json=requests_body)
    request.raise_for_status()
  except requests.RequestException as e:
    raise RuntimeError(f"Ollama is unavailable: {e}")

# Try block 2 — parsing
  try:
    returned_object = request.json()
    RESPONSE = returned_object["response"]
    RESPONSE = RESPONSE.replace('```json', '').replace('```', '').strip()
    output = json.loads(s=RESPONSE)
  except (KeyError, json.JSONDecodeError) as e:
    logging.error(f"Failed to parse model response: {e}")
    raise RuntimeError("Model returned an unexpected response")

# Validation — outside both try blocks
  validate_model_output(output)
  return output