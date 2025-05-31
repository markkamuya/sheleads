import openai
from flask import Flask, render_template, request, jsonify
import time
import os
import asyncio
import aiohttp 

# Set the OpenAI API key
openai.api_key = 'API-KEy'  # Replace 'your-api-key' with your actual API key

# List of example scenarios
scenarios = [
    {"description": "A colleague criticizes your work in front of others.", "first_statement": "John: I think you missed some key points in your last report. Why did you do that?"},
    {"description": "You are asked to lead a meeting, but you feel unprepared.", "first_statement": "John: Hey, I know you were thrown into this last minute. Don't worry, I'll help guide things along."},
    {"description": "A colleague makes a derogatory remark about your dressing.", "first_statement": "John: Whoa, your dress today is so loud!!!."},
    {"description": "Your team is consistently missing deadlines, and you're under pressure from upper management.", "first_statement": "John: We've got a serious issue with deadlines. We need to have a very frank discussion about what's going on."}
]

# Initialize Flask app
app = Flask(__name__)

# Set up session handling
sessions = {}

# Asynchronous function to get AI response from OpenAI
async def get_openai_response(messages, model="gpt-4"):
    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization': f'Bearer {openai.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': model,
            'messages': messages,
            'max_tokens': 300,
            'temperature': 0.7
        }
        async with session.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers) as response:
            return await response.json()

# Main route to render landing page
@app.route('/')
def index():
    return render_template('landing_page.html', scenarios=scenarios)

# Route to handle scenario page and interaction
@app.route('/scenario/<int:scenario_id>', methods=['GET', 'POST'])
async def scenario_page(scenario_id):
    scenario = scenarios[scenario_id]  # Get the scenario using the scenario_id

    session_id = str(scenario_id)  # For simplicity, let's use the scenario ID as the session ID

    if session_id not in sessions:
        sessions[session_id] = {
            'messages': [{"role": "system", "content": "You are a helpful assistant simulating real-time workplace scenarios with the user."},
                         {"role": "user", "content": f"Scenario: {scenario['description']}"}],
            'start_time': time.time()
        }

    if request.method == 'POST':
        try:
            data = request.get_json()
            user_input = data.get('user_input', '').strip()

            if not user_input:
                return jsonify({'error': 'User input cannot be empty.'}), 400

            sessions[session_id]['messages'].append({"role": "user", "content": user_input})

            elapsed_time = time.time() - sessions[session_id]['start_time']
            if elapsed_time > 180:  # 3 minutes = 180 seconds
                return jsonify({'error': 'Time limit reached, conversation ended.'}), 400

            # Send the conversation history to OpenAI for John's response and evaluation
            messages = [{"role": "system", "content": "Time for acting! You are John, a colleague in the workplace. You make the first statement in the scenario. After the user responds, mirror their emotional tone perfectly in your reply. If the user is aggressive, respond with matching intensity; if they are calm, respond with neutrality or support. Your role is to act out the conversation with realism, reflecting the user’s emotional state accurately and consistently throughout. Be a great actor—mirror the tone exactly, just as it would unfold in a real workplace interaction. John is not a helper, he is just a workmate!!! Don't ask any questions, this is a play. So just push the conversation. Better acting skills, this is like the plays by Henrik Ibsen. You control, the conversation. Always ensure there's something to talk about to continue the conversation. You are the controller of the conversation!!! More control, trigger conversations."}] + sessions[session_id]['messages']
            openai_response = await get_openai_response(messages)

            john_statement = openai_response['choices'][0]['message']['content'].strip()

            # For evaluation - we can include both John's response and the user's message in one request
            evaluation_messages = [{"role": "system", "content": "You are an AI evaluator tasked with assessing the user's professionalism and emotional intelligence (EQ). Based on the user’s response, analyze how well they handle the workplace scenario. Focus on their emotional awareness, the appropriateness of their tone, and their ability to manage the conversation constructively. Consider the context of the workplace interaction, the user’s approach to resolving conflicts, and their ability to remain calm or assertive as needed. Provide an evaluation of their communication style, suggesting areas for improvement if necessary. Remember to use the wprd below average, average or good in your evaluation. If there's not enough context, just use available word to evaluate."}]
            evaluation_response = await get_openai_response(evaluation_messages + [{"role": "user", "content": user_input}], model="gpt-4")

            ai_evaluation = evaluation_response['choices'][0]['message']['content'].strip()

            # Score change logic based on evaluation response
            score_change = 0
            if 'excellent' in ai_evaluation.lower():
                score_change = 10
            elif 'good' in ai_evaluation.lower():
                score_change = 5
            elif 'average' in ai_evaluation.lower():
                score_change = 0
            elif 'below average' in ai_evaluation.lower():
                score_change = -10
            elif 'poor' in ai_evaluation.lower():
                score_change = -20

            return jsonify({'bot_response': ai_evaluation, 'john_statement': john_statement, 'score_change': score_change})

        except Exception as e:
            return jsonify({'error': f"Server error: {str(e)}"}), 500

    return render_template('scenario.html', scenario=scenario, scenario_id=scenario_id)

# New route for the "Scenario Over" page
@app.route('/scenario-over')
def scenario_over():
    return render_template('scenario-over.html')  # Renders the scenario-over.html page

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
