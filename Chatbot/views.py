from django.http import JsonResponse
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from .preload import FAISSLoader
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


# Store the current context and topic
current_topic = None
latest_context_summary = ""
diseases = [
    "citrus greening",
    "canker",
    "black spot",
    "huanglongbing",
    "sooty mold",
    "leaf miner",
    "hlb",
    "hi",
]


def detect_topic(prompt):
    """
    Detect the disease topic in the user's prompt.
    Returns the detected topic or None if no match is found.
    """
    for disease in diseases:
        if disease.lower() in prompt.lower():
            return disease
    return None

def index(request):
    db = FAISSLoader.get_faiss_db()
    print("FAISS database accessed successfully!")

@api_view(['POST'])
def chatbot_response(request):
    global current_topic, latest_context_summary
    prompt = request.data.get('prompt')

    if prompt:
        # Detect the disease in the user's prompt
        detected_topic = detect_topic(prompt)

        # Check if the topic has changed
        if detected_topic and detected_topic != current_topic:
            current_topic = detected_topic
            latest_context_summary = ""  # Reset the context summary for the new topic

        db = FAISSLoader.get_faiss_db()
        GROQ_LLM = ChatGroq(
            api_key = os.getenv("GROQ_API_KEY"),
            model="llama-3.2-11b-vision-preview"
        )

        # Combine the latest context with the user's prompt
        combined_context = f"{latest_context_summary}\n{prompt}"

        # Run the query through the chain
        chain = RetrievalQA.from_chain_type(
            llm=GROQ_LLM,
            chain_type="stuff",
            retriever=db.as_retriever()
        )

        response = chain.invoke(combined_context)

        # Update the context summary
        latest_context_summary = summarize_conversation(prompt, response)

        return Response({"response": response})

    return Response({"error": "No prompt provided"}, status=400)

def summarize_conversation(user_input, assistant_response):
    """
    Summarizes the current exchange into a concise context summary.
    """
    if not isinstance(assistant_response, str):
        assistant_response = str(assistant_response)
    return f"User asked about '{user_input}', and assistant responded with '{assistant_response[:50]}...'"