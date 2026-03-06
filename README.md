AI Image → Prompt Generator (Groq + Llama-4)

Convert any image into a high-quality AI generation prompt using the Groq API and Meta Llama-4 Scout.
This tool analyzes an uploaded image and produces a structured prompt optimized for Stable Diffusion, Midjourney, and other generative models.
Built with Python, Gradio, and Groq's ultra-fast inference platform.

## 🎯 Features

- Upload Images: Support for JPG, PNG, GIF, and WebP formats
- AI-Powered Analysis: Uses Groq's vision-capable LLM (Llama-4-Scout) to analyze images
- Prompt Generation: Generates detailed, AI-ready prompts for image generation tools like Stable Diffusion, Midjourney, or DALL-E
- Chat Interface: Clean, interactive Gradio-based chat UI
- Auto-Generation: Automatically generates prompts when you upload an image
- Copy Functionality: Easy copy-to-clipboard for generated prompts

##  Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Your API Key

**Option A**: Edit the `.env` file and add your Groq API key:
```
GROQ_API_KEY="your_actual_groq_api_key_here"
```

**Option B**: Enter your API key directly in the UI when you run the application

> **Get a Groq API Key**: Visit [https://console.groq.com/](https://console.groq.com/) to sign up and get your free API key.

### 3. Run the Application

**Method 1** - Using the test script:
```bash
python run_test.py
```

**Method 2** - Run directly:
```bash
python imgcap.py
```

### 4. Use the Application

1. Open your browser to `http://127.0.0.1:7860`
2. Upload an image (or enter API key if not in .env)
3. The AI will automatically analyze the image and generate a detailed prompt
4. Copy the prompt to use in your favorite image generation tool!

##  How It Works

The application:
1. Accepts an uploaded image from the user
2. Encodes the image in base64 format
3. Sends it to Groq's vision-capable LLM (Llama-4-Scout-17B)
4. The LLM analyzes the image and generates:
   - A ready-to-use comma-separated prompt
   - Detailed breakdown (subject, style, lighting, color palette, composition, mood, etc.)

## Tech Stack

- **Python**: Main programming language
- **Gradio**: Interactive web UI framework
- **Groq**: Fast LLM inference platform
- **Llama-4-Scout-17B**: Vision-capable language model

##  Project Structure

```
.
├── imgcap.py          # Main application file with Gradio UI
├── run_test.py        # Test/launch script
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (API keys)
└── README.md         # This file
```

## 💡 Tips

- The model automatically generates prompts as soon as you upload an image
- Use the "Clear" button to reset the chat and upload a new image
- The generated prompts are optimized for AI image generators
- You can use the copy button on the chat interface to quickly copy prompts

## 🔧 Troubleshooting

**API Key Error**: Make sure your `GROQ_API_KEY` is set correctly in the `.env` file or entered in the UI.

**Import Error**: Run `pip install -r requirements.txt` to install all dependencies.

**Image Upload Error**: Ensure your image is in a supported format (JPG, PNG, GIF, WebP).

## 📄 License

Free to use and modify for personal and commercial projects.
