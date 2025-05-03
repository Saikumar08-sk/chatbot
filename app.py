import os
import gradio as gr
from dotenv import load_dotenv
from gtts import gTTS
import tempfile
from wyn_agent_x.main import AgentX

# Load environment variables from .env or Hugging Face Secrets
load_dotenv()

# Initialize AgentX
agent = AgentX(
    api_key=os.getenv("OPENAI_API_KEY"),
    account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
    auth_token=os.getenv("TWILIO_AUTH_TOKEN"),
    protocol="You are a helpful assistant."
)

# Chat + TTS handler
def chat(user_input):
    try:
        print(f"[DEBUG] User input: {user_input}")
        response_text = agent.process_message(user_input)
        print(f"[DEBUG] Bot response: {response_text}")

        # Convert text to speech
        tts = gTTS(response_text)
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)

        return response_text, temp_audio.name  # Return text + audio path
    except Exception as e:
        print(f"[ERROR] {e}")
        return f"❌ Error: {str(e)}", None

# Gradio interface
gr.Interface(
    fn=chat,
    inputs=gr.Textbox(label="Ask AgentX something", placeholder="e.g., What's the weather?"),
    outputs=[
        gr.Textbox(label="AgentX Says"),
        gr.Audio(label="Voice Response", type="filepath")
    ],
    title="🧠 WYN-Agent-X Chatbot with Voice",
    description="Ask questions or trigger actions — and hear AgentX respond out loud!",
    theme="default"
).launch()
