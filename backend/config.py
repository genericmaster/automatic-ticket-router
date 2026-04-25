OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL_NAME= 'qwen2.5:3b'
STREAM=False
THINK=False

MANAGERS = {"STAFF_SUPPORT":{ 
                 "name" :"THENDONY",
                "email" :"example@gmail.com"
          },
          "BCDR":{ "name":"ZWIDAHO",
                  "email" :"EXAMPLE2@gmail.com"
          },
          "MUSEUM":{
                  "name":"FHUMULANInwana",
                  "email" :"example3@gmail.com"
         }
}

PROMPT =  '''You are a ticket routing system for Wits university...

Departments:
- BCDR: managed by THEMBU. Handles :things like system outages, emergencies, backup failures, disaster situations, continuity planning
- STAFF_SUPPORT managed by THENDO. Handles : new student/staff onboarding, orientation, welcome events, introductions
- MUSEUM: managed by FHUMULANI. Handles : museum visits, artifact queries, exhibitions, donations, bookings

here is the email:
 {email}

 read the subject and body of the email

Return only a JSON object with string values only!! with fields: department, manager,original_email_text, reason,confidence_rating(numerical string within a range of 0 to 100).'''

