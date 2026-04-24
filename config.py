OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL_NAME= 'qwen2.5:3b'
STREAM=False
THINK=False

MANAGERS = {"STAFF_SUPPORT":{ 
                 "name" :"THENDO",
                "email" :"rakhivhanithendo@gmail.com"
          },
          "BCDR":{ "name":"THEMBU",
                  "email" :"2715635@students.wits.ac.za"
          },
          "MUSEUM":{
                  "name":"FHUMULANI",
                  "email" :"mmsdectest1@gmail.com"
         }
}

PROMPT =  '''You are a ticket routing system for Wits university...

Departments:
- BCDR: managed by THEMBU. Handles :things like system outages, emergencies, backup failures, disaster situations, continuity planning
- STAFF_SUPPORT managed by THENDO. Handles : new student/staff onboarding, orientation, welcome events, introductions
- MUSEUM: managed by FHUMULANI. Handles : museum visits, artifact queries, exhibitions, donations, bookings

here is the email:
 {email}

Return only a JSON object only!! with fields: department, manager,original_email_text, reason.'''

