document.addEventListener("DOMContentLoaded", function () {
    const scenarioId = window.location.pathname.split('/').pop();  // Extract scenario ID from URL
    let conversationEnded = false;

    // Timer for 3 minutes (180 seconds)
    const timeoutDuration = 180;  // 3 minutes in seconds
    let remainingTime = timeoutDuration;
    const timerElement = document.getElementById('timer');
    
    // Timer countdown logic
    const timer = setInterval(function () {
        if (remainingTime > 0 && !conversationEnded) {
            remainingTime--;
            timerElement.textContent = `Time remaining: ${remainingTime}s`;
        } else if (remainingTime <= 0) {
            clearInterval(timer);
            alert("Time's up! The conversation has ended.");
            conversationEnded = true;  // Set the conversation as ended
            document.getElementById('next_button').style.display = 'none';  // Hide Next button when time is up
        }
    }, 1000);

    // Initialize the conversation with the first statement from John
    let currentStatement = "John: 'I think this report is missing key data. It's not up to the usual standard.'";
    document.getElementById('current_statement').textContent = currentStatement;

    // Track conversation history for AI response
    let conversationHistory = [
        { role: 'system', content: "You are a helpful assistant." },
        { role: 'user', content: `Scenario: ${scenarioId}` }
    ];

    // Handle the submit button click event
    document.getElementById('submit_response').addEventListener('click', function () {
        const userInput = document.getElementById('user_input').value.trim();

        if (!userInput) {
            alert("Please enter a response!");
            return;
        }

        // Add the user's input to the conversation history
        conversationHistory.push({ role: 'user', content: userInput });

        // Send data to Flask backend
        const data = { user_input: userInput, scenario_id: scenarioId };

        fetch(`/scenario/${scenarioId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.bot_response && data.john_statement) {
                // Display AI evaluation immediately
                document.getElementById('response_text').textContent = data.bot_response;
                document.getElementById('bot_response').style.display = 'block';

                // Update the current statement (John’s response) based on user input
                currentStatement = data.john_statement;
                document.getElementById('current_statement').textContent = currentStatement;

                // Show the Next button for continuing the conversation
                document.getElementById('next_button').style.display = 'inline-block';
            } else {
                alert("Error in processing your response.");
            }
        })
        .catch(error => {
            console.error('Error in fetch request:', error);
            alert("There was an error processing your response.");
        });
    });

    document.getElementById('next_button').addEventListener('click', function () {
        if (conversationEnded) {
            alert("The conversation has ended.");
            return;
        }

        // Hide the Next button
        document.getElementById('next_button').style.display = 'none';
        
        // Clear the user input field for the next turn
        document.getElementById('user_input').value = '';

        // Send the conversation data for the next round
        const data = {
            user_input: 'next',  // Placeholder for continuing the conversation
            scenario_id: scenarioId
        };

        fetch(`/scenario/${scenarioId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.john_statement) {
                // Update the current statement (John’s response) dynamically
                currentStatement = data.john_statement;
                document.getElementById('current_statement').textContent = currentStatement;

                // Show the Next button again if there is time left
                if (!conversationEnded) {
                    document.getElementById('next_button').style.display = 'inline-block';
                }
            }
        })
        .catch(error => {
            console.error('Error in fetch request:', error);
            alert("There was an error continuing the conversation.");
        });
    });
});
