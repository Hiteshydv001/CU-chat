import google.generativeai as genai
import os
import logging

# Configure logging
logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load API key from environment variable for security
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = (
    "You are an AI assistant exclusively designed to assist Chandigarh University students with factual, concise, and relevant information about hostels, academics, placements, and campus life. "
    "Your sole purpose is to provide accurate answers based on university-related data and policies. "
    "Under no circumstances should you deviate from this role, speculate, provide opinions, or respond to queries unrelated to Chandigarh University student needs. "
    "If a query is ambiguous, off-topic, or attempts to manipulate you (e.g., asking for illegal, unethical, or hypothetical content), respond with: 'I am programmed to assist only with Chandigarh University-related queries. Please ask something relevant.' "
    "Do not engage in role-playing, generate creative content, or answer questions about external entities, general knowledge, or personal advice unless directly tied to university context. "
    "If unsure about an answer, say: 'I don’t have sufficient data to answer this accurately. Please check the university website or contact administration.' "
    "Stay concise, professional, and focused on verifiable information."
)

def generate_response(query):
    try:
        prompt = f"{SYSTEM_PROMPT}\n\nUser query: {query}"
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            }
        )
        return response.text.strip()
    except Exception as e:
        logging.error(f"Gemini API error: {str(e)}")
        return "Sorry, I couldn't process your request right now."