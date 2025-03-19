# Women's Tech Platform - AI-Driven Workplace Challenge Practice

## Overview

The platform was designed to help women in tech practice workplace challenges using AI-driven scenarios. It provides a dynamic environment where users can interact with challenges, receive real-time feedback, and track their progress. The backend is powered by Flask, and the frontend leverages JavaScript to deliver an engaging user experience. 

This project focuses on providing personalized learning experiences with real-time feedback while ensuring scalability and performance.

## Features

- **AI-Driven Scenarios**: Users practice workplace challenges through AI-generated scenarios that simulate real-world problems and decision-making situations.
  
- **Flask Backend with RESTful APIs**: The backend is built using Flask, providing a lightweight and efficient framework for handling API requests and real-time feedback.
  
- **Session Management Without Database**: Progress tracking is implemented via Flask’s session management, eliminating the need for a database and ensuring efficient handling of user data.
  
- **Adaptive Scoring**: An interactive color bar provides real-time performance feedback, with adaptive scoring to visually represent progress and performance levels during each scenario.

- **Real-Time Feedback**: Instantaneous feedback is provided as users progress through the challenges, offering a personalized learning experience that adapts to user behavior.

- **Scalable Hosting on Render**: The app is deployed on Render, ensuring a scalable, reliable, and performant hosting environment that allows for seamless user access.

## Architecture

- **Frontend**: 
  - JavaScript for dynamic interaction and performance feedback.
  - Real-time updates of user progress using an adaptive color bar that provides immediate visual feedback.

- **Backend**: 
  - **Flask**: Lightweight backend framework that serves RESTful APIs to handle real-time user interaction.
  - **Session Management**: User progress is stored in session variables, enabling real-time tracking of their performance without a traditional database.

- **Deployment**: 
  - Deployed on **Render** to ensure seamless, scalable access for users across devices.

## Technical Stack

- **Frontend**: HTML, CSS, JavaScript (for real-time performance feedback).
- **Backend**: Flask (Python), RESTful API design.
- **Hosting**: Render (scalable cloud deployment).
- **Session Management**: Flask's built-in session handling for progress tracking.
  
## Installation and Setup

To set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/markkamuya/sheleads
   ```

2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask development server:
   ```bash
   flask run
   ```

4. Access the app at `http://127.0.0.1:5000`.

## Deployment

The application is deployed and hosted on **Render**, ensuring a production-ready environment with automatic scaling and minimal maintenance.

To deploy the app, follow the instructions for [Render Deployment](https://render.com/docs/deploy-flask).

## Contributions

This project was developed by a team of 4 engineers under the guidance of Google’s Women Techmakers program. Contributions include frontend development, backend integration, AI implementation, and deployment.
