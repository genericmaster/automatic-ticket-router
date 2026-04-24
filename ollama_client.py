import requests
import json
from config import OLLAMA_URL,STREAM,MODEL_NAME,THINK,PROMPT


def Route_email(email):
  prompt = PROMPT.format(email=email)

  requests_body = {"model": MODEL_NAME,
                   'prompt':prompt,
                    "stream":STREAM,"think":THINK
  }

  request=requests.post(url=OLLAMA_URL,json=requests_body)
  returned_object=request.json()
  RESPONSE = returned_object["response"]
  print(RESPONSE)
  output=json.loads(s=RESPONSE)

  

  return output

