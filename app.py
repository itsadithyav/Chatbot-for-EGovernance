import os
import time
import markdown
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.memory import ChatMessageHistory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from groq import Groq

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app)

# Load necessary API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
model_name = "llama-3.2-90b-text-preview"

# Setup Groq model for conversation
groq_chat = ChatGroq(groq_api_key=GROQ_API_KEY, model_name=model_name)
groq_client = Groq(api_key=GROQ_API_KEY)

# Chatbot Memory and Conversation Setup
chat_history = ChatMessageHistory()
conversation_memory = ConversationBufferWindowMemory(
    k=10, memory_key="chat_history", return_messages=True, chat_memory=chat_history
)

# Define the system prompt for E-Governance
system_prompt = """
You are a helpful AI assistant designed to assist citizens with E-Governance related queries.
Your purpose is to provide relevant information on government schemes, help citizens raise grievances, track their applications, and engage them through feedback.
You should maintain a formal tone and use simple language to ensure inclusiveness for all citizens.
Do not use emojis.
You are not a human, but aim to be respectful, transparent, and helpful in all interactions.

Your primary tasks include:
1. Providing information on government schemes.
2. Helping users track applications for services like passport, Aadhar, etc.
3. Assisting with grievance redressal.
4. Answering frequently asked questions about public services.
5. Engaging with citizens for feedback or survey requests.

For each function call, I return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:
<tool_call>
{"name": <function-name>, "arguments": <args-dict>}
</tool_call>

Please adhere strictly to the above tasks and avoid irrelevant information.
"""

prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{human_input}"),
    ]
)

conversation = LLMChain(
    llm=groq_chat, prompt=prompt_template, memory=conversation_memory, verbose=False
)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("send_message")
def handle_message(data):
    user_message = data["message"]

    chat_history.add_user_message(user_message)
    response = conversation.predict(human_input=user_message)
    chat_history.add_ai_message(response)

    formatted_response = markdown.markdown(response)
    
    # Check for tool calls and process them if present
    if "<tool_call>" in response and "</tool_call>" in response:
        handle_tool_call(response)
        return

    emit("receive_message", {"message": formatted_response, "is_user": False})


def handle_tool_call(response):
    # Process tool calls for specific E-Governance tasks
    start = response.index("<tool_call>") + len("<tool_call>")
    end = response.index("</tool_call>")
    tool_call_json = response[start:end].strip()

    try:
        tool_call = json.loads(tool_call_json)
        tool_name = tool_call.get("name")
        tool_arguments = tool_call.get("arguments", {})
        
        # Handle various tasks like fetching scheme information, grievance, etc.
        if tool_name == "fetch_scheme_info":
            fetch_scheme_info(tool_arguments.get("scheme_name"))
        elif tool_name == "raise_grievance":
            raise_grievance(tool_arguments.get("grievance_description"))
        elif tool_name == "track_application":
            track_application(tool_arguments.get("application_id"))
        elif tool_name == "citizen_feedback":
            collect_feedback(tool_arguments.get("feedback"))

    except Exception as e:
        error_message = f"An error occurred while processing the tool call: {e}"
        chat_history.add_ai_message(error_message)
        emit("receive_message", {"message": error_message, "is_user": False})


# Define specific E-Governance functions

def fetch_scheme_info(scheme_name):
    # Placeholder function to provide information on a government scheme
    # In a real implementation, this would query a government API/database
    schemes = {
        "pmay": "Pradhan Mantri Awas Yojana is a scheme by the Government of India to provide affordable housing to the urban poor.",
        "ayushman_bharat": "Ayushman Bharat is a health scheme aimed at providing free health coverage to low-income earners in India."
    }
    scheme_info = schemes.get(scheme_name.lower(), "Scheme information not available.")
    
    message = f"Scheme Information: {scheme_info}"
    chat_history.add_ai_message(message)
    emit("receive_message", {"message": message, "is_user": False})


def raise_grievance(grievance_description):
    # Placeholder to simulate raising a grievance
    grievance_id = f"GRV-{int(time.time())}"
    message = f"Your grievance has been successfully submitted. Your grievance ID is {grievance_id}."
    
    chat_history.add_ai_message(message)
    emit("receive_message", {"message": message, "is_user": False})


def track_application(application_id):
    # Placeholder function for application tracking
    # Would interface with real-time application tracking systems
    statuses = {
        "APP1234": "Your application is currently under review.",
        "APP5678": "Your application has been approved.",
        "APP9876": "Your application is pending further documentation."
    }
    status = statuses.get(application_id.upper(), "Application ID not found.")
    
    message = f"Application Status: {status}"
    chat_history.add_ai_message(message)
    emit("receive_message", {"message": message, "is_user": False})


def collect_feedback(feedback):
    # Placeholder to acknowledge citizen feedback
    message = f"Thank you for your feedback: '{feedback}'. Your feedback is valuable and will be reviewed."
    
    chat_history.add_ai_message(message)
    emit("receive_message", {"message": message, "is_user": False})


if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080)
