from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import json
from collections import Counter
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import random

app = Flask(__name__)

# Load GPT-Neo or GPT-J
model_name = "EleutherAI/gpt-neo-1.3B"  # or "EleutherAI/gpt-j-6B" for GPT-J
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Function to generate a response
def generate_response(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    # Set pad_token_id if it is None
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token  # Use end-of-sequence token as padding
        tokenizer.pad_token_id = tokenizer.eos_token_id  # Set the pad_token_id to eos_token_id

    # Create attention mask
    attention_mask = (input_ids != tokenizer.pad_token_id).long()  # This will create a tensor now

    with torch.no_grad():
        output = model.generate(input_ids, attention_mask=attention_mask, max_length=150)
        
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response


# Utility function to get candidate data
def get_candidate_data(candidate_key):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT strengths, proficiency_levels FROM candidates WHERE candidate_key = ?
    ''', (candidate_key,))
    data = cursor.fetchone()
    conn.close()
    return data

# Utility function to determine difficulty
def determine_difficulty(proficiency):
    if proficiency <= 5:
        return 'easy'
    elif 5 < proficiency <= 7:
        return 'medium'
    else:
        return 'advanced'
    
# Utility function to get questions
def get_questions(candidate_key):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()

    strengths, proficiency_levels = get_candidate_data(candidate_key)
    if not strengths:
        return []

    strengths = strengths.split(',')
    proficiency_levels = proficiency_levels.split(',')
    
    questions = {'normal': [], 'mcq': [], 'code': []}

    # Get required questions
    for strength, proficiency in zip(strengths, proficiency_levels):
        difficulty = determine_difficulty(int(proficiency.split('/')[0]))

        cursor.execute('''
            SELECT id, question FROM normal_questions WHERE strength = ? AND difficulty = ?
        ''', (strength, difficulty))
        questions['normal'].extend(cursor.fetchall())

        cursor.execute('''
            SELECT id, mcq_question, option1, option2, option3, option4, correct_option FROM mcq_questions WHERE strength = ? AND difficulty = ?
        ''', (strength, difficulty))
        questions['mcq'].extend(cursor.fetchall())

        cursor.execute('''
            SELECT id, code_question, code_placeholder FROM code_questions WHERE strength = ? AND difficulty = ?
        ''', (strength, difficulty))
        questions['code'].extend(cursor.fetchall())

    conn.close()
    
     # Shuffle the questions randomly
    random.shuffle(questions['normal'])
    random.shuffle(questions['mcq'])
    random.shuffle(questions['code'])

    # Select 5 normal questions, 3 MCQ questions, and 2 code questions
    selected_questions = {
        'normal': questions['normal'][:5],
        'mcq': questions['mcq'][:3],
        'code': questions['code'][:2]
    }

    return selected_questions

@app.route('/')
def index():
    return render_template('index.html')                                           

@app.route('/start', methods=['GET', 'POST']) 
def start():
    if request.method == 'POST':
        candidate_key = request.form['candidate_key']
        return redirect(url_for('questions', candidate_key=candidate_key))
    return render_template('start.html')

@app.route('/questions/<candidate_key>', methods=['GET', 'POST'])
def questions(candidate_key):
    if request.method == 'POST':
        answers = request.form.getlist('answers[]')
        question_ids = request.form.getlist('question_ids[]')
        question_types = request.form.getlist('question_types[]')

        print(f"Received answers: {answers}")

        # Generate semantic analysis using GPT-Neo or GPT-J
        for answer in answers:
            generated_response = generate_response(answer)
            print(f"Generated Response for {answer}: {generated_response}")

        # Check if all answers are provided
        if len(answers) < 7:
            return "Error: Not all questions answered.", 400

        # Calculate accuracy and save responses
        correct_answers = get_correct_answers(question_ids, question_types)
        accuracy = calculate_accuracy(answers, correct_answers)

        print(f"Correct answers retrieved: {correct_answers}")
        print(f"User answers: {answers}")
        print(f"Correct answers: {correct_answers}")

        # Save responses to the database
        conn = sqlite3.connect('chatbot.db')
        cursor = conn.cursor()

        # Check if the candidate_key already exists
        cursor.execute('''
            SELECT id FROM correct_answers WHERE candidate_key = ?
        ''', (candidate_key,))
        existing_entry = cursor.fetchone()  

        if existing_entry:
            # Update the existing entry
            cursor.execute('''
                UPDATE correct_answers SET answers = ?, accuracy = ? WHERE candidate_key = ?
            ''', (json.dumps(answers), accuracy, candidate_key))
        else:
            # Insert a new entry
            cursor.execute('''
                INSERT INTO correct_answers (candidate_key, answers, accuracy)
                VALUES (?, ?, ?)
            ''', (candidate_key, json.dumps(answers), accuracy))

        conn.commit()
        conn.close()
        
        print(f"Answers and accuracy saved. Redirecting to result page.")
        return redirect(url_for('result', candidate_key=candidate_key))

    questions = get_questions(candidate_key)
    return render_template('questions.html', questions=questions, candidate_key=candidate_key)

# Function to fetch correct answers for selected questions
def get_correct_answers(question_ids, question_types):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()                            
 
    normal_ids = [id for id, q_type in zip(question_ids, question_types) if q_type == 'normal']
    mcq_ids = [id for id, q_type in zip(question_ids, question_types) if q_type == 'mcq']
    code_ids = [id for id, q_type in zip(question_ids, question_types) if q_type == 'code']

    print(f"Normal IDs: {normal_ids}")
    print(f"MCQ IDs: {mcq_ids}")                               
    print(f"Code IDs: {code_ids}")

    correct_answers = {'normal': {}, 'mcq': {}, 'code': {}}

    # Fetch normal questions answers
    if normal_ids:
        cursor.execute(f'''
            SELECT id, answer FROM normal_questions WHERE id IN ({','.join(['?']*len(normal_ids))})
        ''', normal_ids)
        correct_answers['normal'] = dict(cursor.fetchall())
 
    # Fetch MCQ questions correct answers
    if mcq_ids:
        cursor.execute(f'''
            SELECT id, correct_option FROM mcq_questions WHERE id IN ({','.join(['?']*len(mcq_ids))})
        ''', mcq_ids)
        correct_answers['mcq'] = dict(cursor.fetchall())

    # Fetch code questions answers
    if code_ids:
        cursor.execute(f'''
            SELECT id, code_placeholder FROM code_questions WHERE id IN ({','.join(['?']*len(code_ids))})
        ''', code_ids)
        correct_answers['code'] = dict(cursor.fetchall())

    conn.close()

    print(f"Correct answers retrieved: {correct_answers}")

    return correct_answers

# Token-based accuracy calculation for normal and code questions
def token_based_match(user_answer, correct_answer):
    # Convert both answers to lowercase and split into words, ignoring extra spaces
    user_tokens = Counter(user_answer.lower().strip().split())
    correct_tokens = Counter(correct_answer.lower().strip().split())
    return user_tokens == correct_tokens

# Updated calculate_accuracy function to handle different answer formats
def calculate_accuracy(user_answers, correct_answers):
    correct_count = 0
    total_count = 0

    print(f"User answers: {user_answers}")
    print(f"Correct answers: {correct_answers}")

    # Normal questions
    normal_keys = list(correct_answers['normal'].keys())
    for i, answer in enumerate(user_answers[:5]):                                     
        if i >= len(normal_keys):
            print("Index out of range for normal questions")
            break
        question_id = normal_keys[i]
        correct_answer = correct_answers['normal'].get(question_id)
        print(f"Normal Question ID: {question_id}, User Answer: {answer}, Correct Answer: {correct_answer}")

        if correct_answer and token_based_match(answer, correct_answer):
            correct_count += 1
        total_count += 1

    # MCQ questions
    mcq_keys = list(correct_answers['mcq'].keys())
    for i, answer in enumerate(user_answers[5:8]):
        if i >= len(mcq_keys):
            print("Index out of range for MCQ questions")
            break
        question_id = mcq_keys[i]
        correct_answer = correct_answers['mcq'].get(question_id)
        print(f"MCQ Question ID: {question_id}, User Answer: {answer}, Correct Answer: {correct_answer}")

        if answer.strip().lower() == correct_answer.strip().lower():
            correct_count += 1
        total_count += 1

    # Code questions
    code_keys = list(correct_answers['code'].keys())
    for i, answer in enumerate(user_answers[8:]): 
        if i >= len(code_keys):
            print("Index out of range for code questions")
            break
        question_id = code_keys[i]
        correct_answer = correct_answers['code'].get(question_id)
        print(f"Code Question ID: {question_id}, User Answer: {answer}, Correct Answer: {correct_answer}")
                            
        if correct_answer and token_based_match(answer, correct_answer):
            correct_count += 1
        total_count += 1

    accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
    print(f"Accuracy calculated: {accuracy}%")
    return accuracy

@app.route('/result/<candidate_key>')
def result(candidate_key):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT answers, accuracy FROM correct_answers WHERE candidate_key = ?
    ''', (candidate_key,))
    data = cursor.fetchone()
    conn.close()

    if data:
        answers, accuracy = data
        answers = json.loads(answers)
        return render_template('result.html', answers=answers, accuracy=accuracy)
    
    return "No results found for this candidate.", 404

if __name__ == '__main__':
    app.run(debug=True)
