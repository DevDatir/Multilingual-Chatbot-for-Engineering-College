import re
import json
from fuzzywuzzy import process, fuzz
from typing import Dict, List
import cohere
from argostranslate import package, translate
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()
# Cohere API setup
cohere_api_key = os.getenv('COHERE_API_KEY')  # Get the API key from the environment variable
co = cohere.Client(cohere_api_key)


app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests



# Load dataset
def load_data(file_path='dataset1.json'):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None

# Detect language (English vs Hinglish)
def detect_language(sentence):
    hinglish_keywords = {"kya", "ka", "hai", "kyunki", "aur", "kaise", "ki", "ke"}
    words = set(sentence.lower().split())
    if words & hinglish_keywords:  # Intersection of sets
        return "hinglish"
    return "english"

# Fuzzy matching for college name
def match_college_name(college_name, dataset):
    if not college_name:
        return None

    # Attempt exact match first
    college_data = next((college for college in dataset if college['name'].lower() == college_name.lower()), None)
    if college_data:
        return college_data

    # Use fuzzy matching as a fallback
    college_names = [college['name'] for college in dataset]
    best_match, score = process.extractOne(college_name, college_names, scorer=fuzz.token_set_ratio)
    if score > 75:  # Match threshold
        return next((college for college in dataset if college['name'] == best_match), None)

    return None

# Setup translation languages for Argos Translate
def setup_translation():
    package.update_package_index()
    available_packages = package.get_available_packages()
    for pkg in available_packages:
        if pkg.from_code == 'en' and pkg.to_code == 'hi':
            package.install_from_path(pkg.download())

def translate_text(from_lang, to_lang, text):
    installed_languages = translate.get_installed_languages()
    from_language = next((lang for lang in installed_languages if lang.code == from_lang), None)
    to_language = next((lang for lang in installed_languages if lang.code == to_lang), None)

    if from_language and to_language:
        translation = from_language.get_translation(to_language)
        return translation.translate(text)
    else:
        return "Translation service is not available."

# Cohere-based intent and entity extraction for eligibility and best college queries
def cohere_understand_query_eligibility(user_query):
    prompt = (
        f"Extract the following details from the user's query: '{user_query}'\n"
        "Classify the query intent into one of the following categories: [cutoff/fees/highest_package/average_package/info/eligibility/best_college].\n"
        "Identify the rank and category if the query is about rank-based college eligibility.\n"
        "If the query asks about the best college from eligible options, classify it as 'best_college'.\n"
        "Provide the response in the following JSON format:\n"
        "{"
        "\"intent\": \"[intent]\"," 
        "\"college_name\": \"[college_name or 'None']\"," 
        "\"branch\": \"[branch or 'None']\"," 
        "\"year\": \"[year or 'None']\"," 
        "\"rank\": \"[rank or 'None']\"," 
        "\"category\": \"[category or 'None']\""
        "}\n"
    )
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=100,
        temperature=0.5
    )
    return response.generations[0].text.strip()

# Cohere-based intent and entity extraction for other queries
def cohere_understand_query(user_query):
    prompt = (
        f"Extract the following details from the user's query: '{user_query}'\n"
        "Provide the response in the following format:\n"
        "Intent: [cutoff/fees/highest_package/average_package/info]\n"
        "College: [the college name, if mentioned, otherwise 'None']\n"
        "Branch: [the branch name if mentioned, otherwise 'None']\n"
        "Year: [the year if provided, otherwise 'None']"
    )
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=50,
        temperature=0.5
    )
    return response.generations[0].text.strip()

# Parse Cohere response for eligibility and best college queries
def parse_cohere_response_eligibility(ai_response):
    try:
        entities = json.loads(ai_response)  # Attempt to parse JSON directly
    except json.JSONDecodeError:
        # If parsing fails, fallback to manual extraction
        entities = {'intent': None, 'college_name': None, 'branch': None, 'year': None, 'rank': None, 'category': None}
        lines = ai_response.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                if key in entities and value.lower() != 'none':
                    entities[key] = value
    return entities

# Parse Cohere response for other queries
def parse_cohere_response(ai_response):
    entities = {'intent': None, 'college_name': None, 'branch': None, 'year': None}
    lines = ai_response.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            if 'intent' in key and value.lower() != 'none':
                entities['intent'] = value
            elif 'college' in key and value.lower() != 'none':
                entities['college_name'] = value
            elif 'branch' in key and value.lower() != 'none':
                entities['branch'] = value
            elif 'year' in key and value.lower() != 'none':
                entities['year'] = value
    return entities

# Find eligible colleges based on rank and category
def find_eligible_colleges(rank, category, dataset):
    eligible_colleges = []
    for college in dataset:
        eligible_branches = []
        for course in college.get('courses', []):
            cutoffs = course.get('cutoffs', {}).get('2024', {})  # Fetch cutoffs for the year 2024
            cutoff_rank = cutoffs.get(category, None)  # Use the specified category
            if cutoff_rank and rank <= cutoff_rank:
                eligible_branches.append(course['name'])

        # Sort branches and take the top 2
        eligible_branches = sorted(eligible_branches)[:2]
        if eligible_branches:
            eligible_colleges.append({
                "college": college['name'],
                "branches": eligible_branches,
                "rating": college['rating']
            })

    # Limit to 7 unique colleges
    return sorted(eligible_colleges, key=lambda x: x['rating'], reverse=True)[:7]


# Find best college from eligible entries
def find_best_college_and_branch(eligible_entries):
    if not eligible_entries:
        return None
    # Select the college with the highest rating and its most competitive branch
    best_entry = eligible_entries[0]
    return {
        "college": best_entry["college"],
        "branch": best_entry["branches"][0],  # Top branch
        "rating": best_entry["rating"]
    }

# Generate best college response
import re
def generate_best_college_response(best_entry, language):
    if not best_entry:
        if language == 'hinglish':
            return "Maaf kijiye, mujhe aapke eligible colleges mein se best college nahi mila."
        else:
            return "Sorry, I couldn't determine the best college from your eligible entries."

    # Generate an explanation using Cohere
    prompt = (
        f"Why is {best_entry['college']} the best choice for the branch {best_entry['branch']}? "
        f"The college has a rating of {best_entry['rating']}/5. Use bold text for section headers like 'Academic Reputation:' "
        f"and highlight its academic reputation, facilities, and other notable features."
    )
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=300,
        temperature=0.4
    )
    explanation = response.generations[0].text.strip()

    # Handle both standard bold markdown (**text**) and section headers
    explanation = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', explanation)
    explanation = re.sub(r'##\s*(.*?):', r'<strong>\1:</strong>', explanation)
    
    # Ensure section headers like "Academic Reputation:" are bold
    explanation = re.sub(r'([A-Za-z\s]+):', r'<strong>\1:</strong>', explanation)

    if language == 'hinglish':
        translated_explanation = translate_text('en', 'hi', explanation)
        return f"{best_entry['college']} branch {best_entry['branch']} ke saath sabse acha college hai.\n\n{translated_explanation}"
    else:
        return f"The best college is {best_entry['college']} with branch {best_entry['branch']}.\n\n{explanation}"

# Generate eligibility response
def generate_eligibility_response(eligible_entries, language='english'):
    if not eligible_entries:
        if language == 'hinglish':
            return "Maaf kijiye, aapke rank ke liye koi college nahi mila."
        else:
            return "Sorry, no colleges were found for your rank."

    response = "Eligible colleges and top branches:\n\n" if language == 'english' else "Yogya college aur unke top branch:\n\n"
    
    for entry in eligible_entries:
        # Add college name
        response += f"{entry['college']}\n"
        # Add branches with indentation and separate them with newlines
        for branch in entry['branches']:
            response += f"- {branch}\n"
        # Add extra newline after each college's complete entry
        response += "\n"
    
    return response.rstrip()  # Remove trailing whitespace while preserving intended line breaks

# Get cutoff details
def get_cutoff_details(college_data, branch_name=None, year=None):
    year = year if year else '2024'  # Default to 2024
    branch_cutoffs = []

    for course in college_data['courses']:
        if branch_name and branch_name.lower() not in course['name'].lower():
            continue
        cutoff = course['cutoffs'].get(year, {})
        branch_cutoffs.append({
            'branch': course['name'],
            'cutoff': cutoff
        })

    return branch_cutoffs

# Generate cutoff response
def generate_cutoff_response(branch_cutoffs, college_name, language='english'):
    if not branch_cutoffs:
        if language == 'hinglish':
            return "Maaf kijiye, is branch ke liye cutoff details nahi mili."
        else:
            return "Sorry, cutoff details for this branch are not available."

    # Create response with HTML formatting
    response = f"""<div class='cutoff-container'>
    <h3 class='college-name'>Cutoff Details for {college_name}</h3>
    <div class='branches-container'>"""

    # Sort branches alphabetically
    sorted_branches = sorted(branch_cutoffs, key=lambda x: x['branch'])

    for branch in sorted_branches:
        response += f"""
        <div class='branch-item'>
            <h4 class='branch-name'>{branch['branch']}</h4>
            <div class='cutoff-details'>"""
        
        for category, rank in branch['cutoff'].items():
            formatted_rank = f"{rank:,}"
            response += f"""
                <div class='category-item'>
                    <span class='category'>{category}:</span>
                    <span class='rank'>{formatted_rank}</span>
                </div>"""
        
        response += """
            </div>
        </div>"""

    response += """
    </div>
</div>"""

    return response

# Generate dynamic response for college-specific queries
def generate_dynamic_response_college(intent, college_data, language='english', branch=None, year=None):
    if not college_data:
        if language == 'hinglish':
            return "Maaf kijiye, mujhe college ke baare mein jaankari nahi mili."
        else:
            return "Sorry, I couldn't find information about the college."

    if intent == 'cutoff':
        branch_cutoffs = get_cutoff_details(college_data, branch, year)
        return generate_cutoff_response(branch_cutoffs, college_data['name'], language)

    elif intent == 'fees':
        # Fetch the fee of the first course
        annual_fee = college_data['courses'][0]['annual_fee']
        if language == 'hinglish':
            return f"{college_data['name']} ki fees:\n₹{annual_fee:,}/saal"
        else:
            return f"The fees for {college_data['name']} are:\n₹{annual_fee:,}/year"

    elif intent == 'highest_package' or intent=='highest_salary':
        highest_package = college_data['placements']['highest_package']
        if language == 'hinglish':
            return f"{college_data['name']} ka highest package ₹{highest_package:,}/saal hai."
        else:
            return f"The highest package for {college_data['name']} is ₹{highest_package:,}/year."

    elif intent == 'average_package' or intent=='highest_salary':
        avg_package = college_data['placements']['average_package']
        if language == 'hinglish':
            return f"{college_data['name']} ka average package ₹{avg_package:,}/saal hai."
        else:
            return f"The average package for {college_data['name']} is ₹{avg_package:,}/year."

    elif intent == 'info':
        location = college_data['location']
        rating = college_data['rating']
        facilities = ", ".join(college_data['facilities'])
        if language == 'hinglish':
            return (f"{college_data['name']} ki location {location} hai aur rating {rating}/5 hai. Facilities mein shamil hain: {facilities}.")
        else:
            return (f"{college_data['name']} is located in {location}, has a rating of {rating}/5. Facilities include: {facilities}.")

    return "Sorry, I couldn't understand your query."

# Generate dynamic response for eligibility and best college queries
def generate_dynamic_response_eligibility(intent, language='english', rank=None, category=None, dataset=None, eligible_entries=None):
    if intent == 'eligibility':
        eligible_entries = find_eligible_colleges(rank, category, dataset)
        return generate_eligibility_response(eligible_entries, language)

    if intent == 'best_college':
        best_entry = find_best_college_and_branch(eligible_entries)
        return generate_best_college_response(best_entry, language)

    return "Sorry, I couldn't understand your query."

# Process user query for eligibility and best college
# def process_user_query_eligibility(user_query, dataset):
#     detected_language = detect_language(user_query)

#     # Step 1: Extract intent and entities using Cohere
#     ai_response = cohere_understand_query_eligibility(user_query)
#     parsed_data = parse_cohere_response_eligibility(ai_response)

#     intent = parsed_data.get('intent', None)
#     rank = int(parsed_data['rank']) if parsed_data['rank'] and parsed_data['rank'] != 'None' else None
#     category = parsed_data['category'].upper() if parsed_data['category'] and parsed_data['category'] != 'None' else 'GOPEN'

#     if intent == 'eligibility' and rank is not None:
#         eligible_entries = find_eligible_colleges(rank, category, dataset)
#         return generate_dynamic_response_eligibility(intent, language=detected_language, rank=rank, category=category, dataset=dataset, eligible_entries=eligible_entries)

#     if intent == 'best_college':
#         # Reuse eligible entries from eligibility query
#         eligible_entries = find_eligible_colleges(rank if rank else 0, category, dataset)
#         return generate_dynamic_response_eligibility(intent, language=detected_language, eligible_entries=eligible_entries)

# Add these methods at the end of the combined.py file
# Main query processing function for general college queries
def process_user_query(user_query, dataset):


    detected_language = detect_language(user_query)

    # First, try to process as an eligibility/best college query
    ai_response_eligibility = cohere_understand_query_eligibility(user_query)
    parsed_data_eligibility = parse_cohere_response_eligibility(ai_response_eligibility)
    
    intent_eligibility = parsed_data_eligibility.get('intent', None)
    
    # If it's an eligibility or best_college query, process it accordingly
    if intent_eligibility in ['eligibility', 'best_college']:
        rank = int(parsed_data_eligibility['rank']) if parsed_data_eligibility['rank'] and parsed_data_eligibility['rank'] != 'None' else None
        category = parsed_data_eligibility['category'].upper() if parsed_data_eligibility['category'] and parsed_data_eligibility['category'] != 'None' else 'GOPEN'
        
        if intent_eligibility == 'eligibility' and rank is not None:
            eligible_entries = find_eligible_colleges(rank, category, dataset)
            return generate_dynamic_response_eligibility(
                intent_eligibility, 
                language=detected_language, 
                rank=rank, 
                category=category, 
                dataset=dataset, 
                eligible_entries=eligible_entries
            )
        
        if intent_eligibility == 'best_college':
            eligible_entries = find_eligible_colleges(rank if rank else 0, category, dataset)
            return generate_dynamic_response_eligibility(
                intent_eligibility, 
                language=detected_language, 
                eligible_entries=eligible_entries
            )
    
    casual_response = handle_casual_conversation(user_query)
    if casual_response:
        return casual_response
    
    # If not an eligibility query, process as a regular college query
    ai_response = cohere_understand_query(user_query)
    parsed_data = parse_cohere_response(ai_response)

    intent = parsed_data['intent']
    college_name = parsed_data['college_name']
    branch_name = parsed_data['branch']
    year = parsed_data['year']

    college_data = match_college_name(college_name, dataset)
    
    return generate_dynamic_response_college(
        intent, 
        college_data, 
        language=detected_language, 
        branch=branch_name, 
        year=year
    )


def handle_casual_conversation(user_query):
    """
    Handle casual conversational queries using Cohere's generative model
    """
    # Predefined conversational intents
    conversational_intents = [
        "greeting", "small_talk", "how_are_you", "introduction", 
        "farewell", "appreciation", "joke", "general_chat"
    ]

    # Prompt to classify the intent and generate an appropriate response
    prompt = (
        f"Classify the intent of this message: '{user_query}'\n"
        "Possible intents: " + ", ".join(conversational_intents) + "\n"
        "If the intent is casual/conversational, generate a friendly, natural response. "
        "If it doesn't fit a conversational intent, return 'NOT_CONVERSATIONAL'.\n"
        "Format your response as: 'Intent: [intent]\nResponse: [generated_response]'"
    )

    # Use Cohere to generate a response
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7
    )

    # Process the generated response
    generated_text = response.generations[0].text.strip()
    
    # Parse the response
    lines = generated_text.split('\n')
    intent = lines[0].split(': ')[1] if len(lines) > 0 and ':' in lines[0] else None
    
    if intent and intent != 'NOT_CONVERSATIONAL':
        response_text = lines[1].split(': ')[1] if len(lines) > 1 else generated_text
        return response_text

    return None


# Chatbot interaction loop
@app.route('/chat', methods=['POST'])
def chat():
    print("Chat endpoint hit!")  # Debug print
    
    # Log the incoming request details
    print("Request method:", request.method)
    print("Request content type:", request.content_type)
    print("Request data:", request.get_json())

    try:
        # Explicitly parse JSON data
        data = request.get_json()
        if not data:
            print("No JSON data received")
            return jsonify({"error": "No data provided"}), 400

        user_query = data.get('message', '')
        print(f"Received query: {user_query}")

        if not user_query:
            return jsonify({"error": "Please enter a valid query."}), 400

        # Load dataset
        dataset = load_data('dataset1.json')
        if dataset is None:
            return jsonify({"error": "Dataset not found."}), 500

        # Process query
        response = process_user_query(user_query, dataset)
        print(f"Generated response: {response}")

        return jsonify({"response": response})

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Ensure CORS is configured correctly
CORS(app, resources={r"/chat": {"origins": "*"}})

# Run the chatbot
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)



#Eligibilty is fixed