
json_data={
 
  "data": "{\n    \"evaluation\": [\n        {\n            \"type\": \"MCQ\",\n            \"question\": \"What is the capital of France?\",\n            \"user_answer\": \"Paris\",\n            \"correct_answer\": \"Paris\",\n            \"points_awarded\": 5,\n            \"points_possible\": 5,\n            \"feedback\": \"Correct! 'Paris' is the capital of France.\"\n        },\n        {\n            \"type\": \"Subjective\",\n            \"question\": \"Explain the water cycle.\",\n            \"user_answer\": \"Water cycle involves evaporation and precipitation...\",\n            \"correct_answer\": \"The water cycle is the continuous movement of water...\",\n            \"points_awarded\": 3,\n            \"points_possible\": 5,\n            \"feedback\": \"Your answer mentions key components like evaporation and precipitation, which are correct. However, to improve, include additional details about condensation, collection, and the overall cycle to provide a more complete explanation.\"\n        }\n    ],\n    \"evaluation_summary\": {\n        \"total_score\": 8,\n        \"total_possible\": 10,\n        \"percentage\": 80\n    },\n    \"overall_feedback\": \"The MCQ question was answered correctly. For the subjective question, while key aspects were mentioned, more detailed explanation is needed for full credit. To improve, try to include all parts of the concept in your answer.\"\n}"
}
import json
data = json.dumps(json_data)



print(data)