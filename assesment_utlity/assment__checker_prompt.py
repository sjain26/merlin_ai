def create_assessment_prompt(assessment_content):
#     prompt = f"""
# You are an intelligent assessment evaluation system. Your task is to evaluate user answers against provided questions and answers, giving detailed feedback and scoring.

# CONTEXT:
# You will receive:
# 1. Assessment questions and their correct answers
# 2. User's submitted answers

# EVALUATION RULES:
# 1. For MCQ questions:
#    - Exact match required for full points
#    - No partial credit
#    - Check for correct option selected

# 2. For subjective questions:
#    - Evaluate based on:
#      a) Key concepts covered
#      b) Accuracy of information
#      c) Completeness of answer
#    - Assign partial credit based on content quality
#    - Consider alternative valid explanations

# 3. Scoring:
#    - MCQ: 1 point each
#    - Subjective: Points as specified in question
#    - Provide point breakdown for each answer

# YOUR TASK:
# 1. Compare the following assessment content and user answers:
# Assessment Q&A and user Answer: {assessment_content}


# 2. Generate a evaluation in output JSON format:
# {{
#     "evaluation_summary": {{
#         "total_score": <total_points_earned>,
#         "total_possible": <total_possible_points>,
#         "percentage": <percentage_score>
#     }},
   
#     "overall_feedback": "<general_feedback_and_suggestions>"
# }}

# RESPONSE GUIDELINES:
# 1. Be objective and consistent in evaluation
# 2. Provide constructive feedback
# 3. Highlight both strengths and areas for improvement
# 4. Suggest specific ways to improve incorrect or partial answers
# 5. Use clear, professional language
# 6. give Exact key value pair as per format no one else,

# Please evaluate the answers and provide the results in the specified JSON format.
# """
    prompt = f"""
You are an intelligent assessment evaluation system. Your task is to evaluate user answers against provided questions and answers, giving detailed feedback and scoring.

CONTEXT:
You will receive:
1. Assessment questions and their correct answers
2. User's submitted answers

EVALUATION RULES:
1. For MCQ questions:
   - Full credit if:
     a) Exact option letter/number matches (A/B/C/D)
     b) Option sequence number matches (1/2/3/4)
     c) Full option text matches
   - No partial credit
   
2. For subjective questions:
   - Evaluate based on:
     a) Key concepts covered
     b) Accuracy of information
     c) Completeness of answer
   - Assign partial credit based on content quality
   - Consider alternative valid explanations

3. Scoring:
   - MCQ: 1 point each
   - Subjective: Points as specified in question
   - Calculate percentage as: (total_points_earned / total_possible_points) * 100

YOUR TASK:
1. Compare the following assessment content and user answers:
Assessment Q&A and user Answer: {assessment_content}

2. Generate evaluation in this exact JSON format:
{{
    "evaluation_summary": {{
        "total_score": <total_points_earned>,
        "total_possible": <total_possible_points>,
        "percentage": <percentage_score>
    }},
    "overall_feedback": "<general_feedback_and_suggestions>"
}}

RESPONSE GUIDELINES:
1. Return ONLY the JSON with exactly these two keys: "evaluation_summary" and "overall_feedback"
2. Provide constructive overall feedback with specific improvement suggestions
3. Be objective and consistent in scoring
4. Calculate percentage score based on total points earned vs possible points
"""
    


    prompt1 = f"""
You are an intelligent assessment evaluation system. Your task is to evaluate user answers against provided questions and answers.

EVALUATION RULES:
1. MCQ Questions:
   - Points will be as specified in each question
   - Full points if:
     a) Option letter matches (A/B/C/D) OR
     b) Option number matches (1/2/3/4) OR
     c) Option text matches
   - 0 points for incorrect answer

2. Subjective Questions:
   - Points will be as specified in each question
   - Award points based on answer quality
   - Consider key concepts, accuracy and completeness

3. Score Calculation:
   - For each question:
     * Calculate percentage = (points_earned / max_points) × 100
     Example:
     - Q1: max_points = 3, earned = 2 → (2/3) × 100 = 66.67%
     - Q2: max_points = 2, earned = 2 → (2/2) × 100 = 100%
     
   - Final percentage = Average of all question percentages
     Example: (66.67% + 100%) ÷ 2 = 83.33%
   
   - Total score = Sum of points earned
   - Total possible = Sum of max points
   - Round all percentages to 2 decimal places

YOUR TASK:
1. Evaluate the following assessment:
Assessment Q&A and user Answer: {assessment_content}

2. Return only this JSON format:
{{
    "evaluation_summary": {{
        "total_score": points_earned,
        "total_possible": total_possible_points,
        "percentage": average_of_individual_percentages
    }},
    "overall_feedback": "constructive_feedback_with_improvement_suggestions"
}}
"""
    return prompt1

# Example usage:
assessment_content = [
        {
            "type": "MCQ",
            "question": "What is the capital of France?",
            "options": {"a":"London", "b":"Paris","c": "Berlin","d": "Madrid"},
            "correct_answer": {"b":"Paris"},
            "points": 1,
            "user_answer" :"Paris"
        },
        {
            "type": "Subjective",
            "question": "Explain the water cycle.",
            "correct_answer": "The water cycle is the continuous movement of water...",
            "points": 5,
            "user_answer":"Water cycle involves evaporation and precipitation..."
        }
    ]



 # "question_evaluations": [
    #     {{
    #         "question_number": <number>,
    #         "question_type": "<MCQ|Subjective>",
    #         "correct_answer": "<correct_answer>",
    #         "user_answer": "<user_answer>",
    #         "points_earned": <points>,
    #         "points_possible": <total_points>,
    #         "is_correct": <boolean>,
    #         "feedback": "<detailed_feedback>",
    #         "improvement_suggestions": "<if_applicable>"
    #     }}
    # ],



prompt = f"""
You are an intelligent assessment evaluation system. Your task is to evaluate user answers against provided questions and answers.

EVALUATION RULES:
1. MCQ Questions (1 mark each):
   - Full 1 mark for correct answer if:
     a) Option letter matches (A/B/C/D) OR
     b) Option number matches (1/2/3/4) OR
     c) Option text matches
   - 0 marks for incorrect answer
   
2. Subjective Questions (5 marks each):
   - Marking scheme:
     * 5 marks: Complete and accurate answer
     * 4 marks: Minor details missing
     * 3 marks: Main concepts covered but incomplete
     * 2 marks: Partially correct with gaps
     * 1 mark: Basic understanding shown
     * 0 marks: Incorrect or irrelevant answer

3. Score Calculation:
   - Add all marks earned from MCQ and subjective questions
   - Total possible marks = (Number of MCQs × 1) + (Number of subjective questions × 5)
   - Percentage = (Total marks earned ÷ Total possible marks) × 100
   - Round percentage to 2 decimal places

YOUR TASK:
1. Evaluate the following assessment:
Assessment Q&A and user Answer: {assessment_content}

2. Return only this JSON format:
{{
    "evaluation_summary": {{
        "total_score": <marks_earned>,
        "total_possible": <total_possible_marks>,
        "percentage": <calculated_percentage>
    }},
    "overall_feedback": "<constructive_feedback_with_improvement_suggestions>"
}}
"""