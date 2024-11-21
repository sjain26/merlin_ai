
from fastapi import HTTPException 
import os
import re
import openai
from assesment_utlity.assement_generation_prompt import generate_qa_system_prompt
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())


os.getenv("OPENAI_API_KEY")

def question_answer(job_description,
    question_type,
    num_questions ,
    question_traits,
    question_level):
    print("-------------------------------------",job_description)
    print("-type--",type(job_description))
    try:
        client = openai.Client()
        
        
        system_prompt = generate_qa_system_prompt(job_description=job_description, 

    question_type=question_type,
    num_questions= num_questions  ,
    question_traits=question_traits,
    question_level=question_level)
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