import openai
from flask import Flask, render_template, request, jsonify
import time
import os

# Set the OpenAI API key
openai.api_key = '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'

# List of example scenarios
scenarios = [
    {
        "description": "A colleague criticizes your work in front of others.",
        "first_statement": "John: I think you missed some key points in your last report. Can we talk about that?"
    },
    {
        "description": "You are asked to lead a meeting, but you feel unprepared.",
        "first_statement": "John: Hey, I know you were thrown into this last minute. Don't worry, I'll help guide things along."
    },
    {
        "description": "A colleague makes a derogatory remark about your gender.",
        "first_statement": "John: That comment was completely inappropriate, and I think we need to address it."
    },
    {
        "description": "Your team is consistently missing deadlines, and you're under pressure from upper management.",
        "first_statement": "John: We've got a serious issue with deadlines. We need to have a frank discussion about what's going on."
    }
]

# Initialize Flask app
app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))
@app.route('/')
def index():
    return render_template('landing_page.html', scenarios=scenarios)

# Store session data (conversation history)
sessions = {}

@app.route('/scenario/<int:scenario_id>', methods=['GET', 'POST'])
def scenario_page(scenario_id):
    scenario = scenarios[scenario_id]  # Get the scenario using the scenario_id

    # Check if session exists for this user, if not create one
    session_id = str(scenario_id)  # For simplicity, let's use the scenario ID as the session ID

    if session_id not in sessions:
        sessions[session_id] = {
            'messages': [
                {"role": "system", "content": "You are a helpful assistant simulating real-time workplace scenarios with the user."},
                {"role": "user", "content": f"Scenario: {scenario['description']}"}
            ],
            'start_time': time.time()
        }

    # Handle POST request (user input)
    if request.method == 'POST':
        try:
            # Get the incoming JSON data
            data = request.get_json()
            user_input = data.get('user_input', '').strip()

            # Debugging: Log the incoming data
            print(f"Received data: {data}")

            if not user_input:
                return jsonify({'error': 'User input cannot be empty.'}), 400

            # Add user input to the conversation history
            sessions[session_id]['messages'].append({"role": "user", "content": user_input})

            # Get conversation time and check if it exceeded 3 minutes
            elapsed_time = time.time() - sessions[session_id]['start_time']
            if elapsed_time > 180:  # 3 minutes = 180 seconds
                return jsonify({'error': 'Time limit reached, conversation ended.'}), 400

            # Send the conversation history to OpenAI for John’s response
            john_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Time for acting! You are John, a colleague in the workplace. You make the first statement in the scenario. After the user responds, mirror their emotional tone perfectly in your reply. If the user is aggressive, respond with matching intensity; if they are calm, respond with neutrality or support. Your role is to act out the conversation with realism, reflecting the user’s emotional state accurately and consistently throughout. Be a great actor—mirror the tone exactly, just as it would unfold in a real workplace interaction. John is not a helper, he is just a workmate!!! Don't ask any questions, this is a play. So just push the conversation. Better acting skills, this is like the plays by Henrik Ibsen. You control, the conversation. Always ensure there's something to talk about to continue the conversation. You are the controller of the conversation!!! More control, trigger conversations."}
                ] + sessions[session_id]['messages'],
                max_tokens=300,
                temperature=0.7
            )

            # Extract John's response (this is what John says next)
            john_statement = john_response['choices'][0]['message']['content'].strip()

            # Send the user's input to the AI for evaluation (independent of John’s response)
            evaluation_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[ 
                    {"role": "system", "content": "You are an AI evaluator tasked with assessing the user's professionalism and emotional intelligence (EQ). Based on the user’s response, analyze how well they handle the workplace scenario. Focus on their emotional awareness, the appropriateness of their tone, and their ability to manage the conversation constructively. Consider the context of the workplace interaction, the user’s approach to resolving conflicts, and their ability to remain calm or assertive as needed. Provide an evaluation of their communication style, suggesting areas for improvement if necessary. Remember to use the wprd below average, average or good in your evaluation. If there's not enough context, just use available word to evaluate."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=300,
                temperature=0.7
            )

            # Extract AI's evaluation of the user's input
            ai_evaluation = evaluation_response['choices'][0]['message']['content'].strip()
	    # Score adjustment logic based on AI's evaluation
            score_change = 0  # Default score change
            if 'excellent' in ai_evaluation.lower():
                score_change = 10  # Increase score for excellent responses
            elif 'good' in ai_evaluation.lower():
                score_change = 5  # Increase score for good responses
            elif 'average' in ai_evaluation.lower():
                score_change = 0  # No change for average responses
            elif 'below average' in ai_evaluation.lower():
                score_change = -10  # Decrease score for below average responses
            elif 'poor' in ai_evaluation.lower():
                score_change = -20  # Decrease score for poor responses
	    

            # Return the evaluation and John's statement
            return jsonify({'bot_response': ai_evaluation, 'john_statement': john_statement, 'score_change': score_change})

        except Exception as e:
            print(f"Error processing request: {e}")
            return jsonify({'error': f"Server error: {str(e)}"}), 500

    # Handle GET requests (Rendering the scenario page)
    return render_template('scenario.html', scenario=scenario, scenario_id=scenario_id)

# New route for the "Scenario Over" page
@app.route('/scenario-over')
def scenario_over():
    return render_template('scenario-over.html')  # Renders the scenario-over.html page

# Run the app
if __name__ == '__main__':
    # Bind to 0.0.0.0 and use the dynamic port provided by Render
    app.run(host='0.0.0.0', port=port, debug=True)
