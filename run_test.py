"""
Simple test script to launch the Image Prompt Generator UI
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import and run the Gradio app
from imgcap import demo

if __name__ == "__main__":
    print("🚀 Launching Image Prompt Generator...")
    print("📍 Make sure you have set your GROQ_API_KEY in .env file or enter it in the UI")
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860)
