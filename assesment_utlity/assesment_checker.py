
from fastapi import HTTPException 
import os
import re
import openai
from assesment_utlity.assment__checker_prompt import create_assessment_prompt
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
os.getenv("OPENAI_API_KEY")

def mark_evalution(assessment_content):
   
    try:
        client = openai.Client()
        
        
        system_prompt = create_assessment_prompt(assessment_content)
        print("promt--------------------",system_prompt)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
               
                {"role": "user", "content": system_prompt}
            ],
         
        )
    
        res =extract_json(response.choices[0].message.content)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generation Question: {str(e)}")


def extract_json(text):
    match = re.search(r'(?s)\{.*\}', text)   # find the JSON string using regex
    if match:  # check if the JSON string is found
        json_str = match.group(0)
        return json_str  # prints the JSON string
    else:
        print("No JSON object could be decoded")
        return None