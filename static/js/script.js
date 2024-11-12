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
            document.getElementById('submit_response').disabled = true;  // Disable the submit button
        }
    }, 1000);

    // Initialize score as 100%
    let scorePercentage = 100;
    const scorebar = document.getElementById('scorebar');
    const scoreText = document.getElementById('score-text');

    // Function to update the scorebar and the score text
    function updateScorebar(scorePercentage) {
        // Ensure the score doesn't exceed 100% or go below 0%
        scorePercentage = Math.max(0, Math.min(100, scorePercentage));  // Cap score between 0 and 100

        // Update the width of the scorebar
        scorebar.style.width = `${scorePercentage}%`;

        // Change the color based on the score percentage
        if (scorePercentage >= 70) {
            scorebar.style.backgroundColor = '#28a745';  // Green
        } else if (scorePercentage >= 40) {
            scorebar.style.backgroundColor = '#ffc107';  // Yellow
        } else if (scorePercentage > 0) {
            scorebar.style.backgroundColor = '#dc3545';  // Red
        } else {
            scorebar.style.backgroundColor = '#dc3545';  // Fully red
            conversationEnded = true;  // End the conversation if score reaches 0%
            clearInterval(timer);  // Stop the timer
            document.getElementById('submit_response').disabled = true;  // Disable the submit button

            console.log('Score reached 0%. Redirecting to scenario-over.html.');
            window.location.href = '/scenario-over';  // Redirect to the new page
        }

        // Update the score text
        scoreText.textContent = `Score: ${Math.round(scorePercentage)}%`;
    }

    // Handle the submit button click event
    document.getElementById('submit_response').addEventListener('click', function () {
        const userInput = document.getElementById('user_input').value.trim();

        if (!userInput) {
            alert("Please enter a response!");
            return;
        }

        // Send data to Flask backend
        const data = { user_input: userInput, scenario_id: scenarioId };

        fetch(`/scenario/${scenarioId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to process your response');
            }
            return response.json();
        })
        .then(data => {
            if (data.bot_response && data.john_statement) {
                // Display AI evaluation
                document.getElementById('response_text').textContent = data.bot_response;
                document.getElementById('bot_response').style.display = 'block';

                // Update the current statement (John’s response) based on user input
                document.getElementById('current_statement').textContent = data.john_statement;

                // AI Evaluation logic to update the scorebar
                if (data.bot_response.includes('below average')) {
                    scorePercentage -= 10;  // Subtract 10% if AI evaluation is below average
                }
                if (data.bot_response.includes('average')) {
                    scorePercentage -= 5;  // Subtract 5% for average responses
                }
                if (data.bot_response.includes('good')) {
                    scorePercentage += 5;  // Increase 5% for good responses
                }

                // Update the scorebar based on the evaluation
                updateScorebar(scorePercentage);

                // Show the Next button for continuing the conversation (optional)
                document.getElementById('next_button').style.display = 'inline-block';
            } else {
                console.error('Error: Missing bot response or John’s statement');
            }
        })
        .catch(error => {
            console.error('Error in fetch request:', error);
        });
    });

    // Next button logic (if you have a Next button for multiple rounds)
    document.getElementById('next_button').addEventListener('click', function () {
        if (conversationEnded) {
            alert("The conversation has ended.");
            return;
        }

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
                document.getElementById('current_statement').textContent = data.john_statement;
            }
        })
        .catch(error => {
            console.error('Error in fetch request:', error);
        });
    });
});
