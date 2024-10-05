# E-Governance Chatbot

This project is a chatbot application built with Flask and Socket.IO, designed to assist citizens with E-Governance-related queries. The chatbot handles government-related tasks such as tracking applications, providing scheme information, raising grievances, and collecting feedback. It uses natural language processing through the Groq model for seamless conversation and memory management.

## Features

- **E-Governance Assistance**: The chatbot helps users with common government services such as:
  - Providing information on government schemes.
  - Tracking service applications (e.g., passports, Aadhaar).
  - Assisting with grievance redressal.
  - Collecting citizen feedback.
- **Memory Management**: Chat history is stored using a memory buffer, allowing the chatbot to remember the last 10 interactions.
- **Real-time Messaging**: Users can interact with the chatbot in real-time through WebSockets using Flask-SocketIO.
- **Tool Calls**: The bot can detect when certain tasks (like fetching scheme details or tracking applications) need to be performed via specialized function calls.
- **Markdown Formatted Responses**: The chatbot uses Markdown to format its responses, ensuring clarity in its output.

## Technologies Used

- **Flask**: A micro web framework used for handling the backend and routing.
- **Flask-SocketIO**: Enables real-time communication between the chatbot and the user.
- **Langchain**: Manages conversational chains and memory for AI interactions.
- **Groq API**: Powers the language model for generating responses.
- **Markdown**: Used for formatting the chatbot’s responses.
- **dotenv**: Loads environment variables (API keys, etc.) from a `.env` file.
  
## Setup and Installation

### Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)

### Steps to Set Up

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/e-governance-chatbot.git
   cd e-governance-chatbot
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root of the project and add the Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```

6. **Access the Application**:
   Open a browser and navigate to `http://localhost:8080`.

## Project Structure

```bash
├── app.py                   # Main Flask application
├── templates
│   └── index.html           # HTML template for chatbot UI
├── .env                     # Environment variables for API keys
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Key Components

- **Groq Language Model**: Utilizes the Groq model (`llama-3.2-90b-text-preview`) for generating responses.
- **Chat Memory**: The chatbot uses `ConversationBufferWindowMemory` from Langchain to remember the last 10 messages, ensuring a smooth conversation flow.
- **Tool Calls**: The chatbot processes specific tasks like fetching scheme information, raising grievances, and tracking applications through JSON-based tool calls embedded in the conversation.

## Key Functions

- **fetch_scheme_info(scheme_name)**: Provides information about government schemes like "Pradhan Mantri Awas Yojana" and "Ayushman Bharat."
  
- **raise_grievance(grievance_description)**: Simulates raising a grievance and returns a unique grievance ID.
  
- **track_application(application_id)**: Tracks the status of a user's application based on a predefined list of application IDs.
  
- **collect_feedback(feedback)**: Acknowledges and stores citizen feedback.

## Usage

- **Send Message**: Users can send messages through the UI. The chatbot will process these using the Groq model, and if required, will call specific functions to fetch information or track applications.
  
- **Real-time Response**: The chatbot responds in real-time with a formatted message, visible in the chat interface.

## License

This project is open source and available under the [MIT License](./LICENSE).
