"""
Image Prompt Generator — powered by Groq + Gradio
Requires:
    pip install gradio groq python-dotenv
Set env var:
    GROQ_API_KEY=your_key_here
"""

import base64
import os
from pathlib import Path
from dotenv import load_dotenv

import gradio as gr
from groq import Groq

# Load environment variables
load_dotenv()




def encode_image(image_path: str) -> tuple[str, str]:
    """Return (base64_data, media_type) for an image file."""
    ext = Path(image_path).suffix.lower()
    mime = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return data, mime


def normalize_chat_history(chat_history: list) -> list:
    """Convert legacy tuple/list entries into dicts with 'role' and 'content'.

    - If item is a dict with 'role'/'content' it is left as-is.
    - If item is a 2-tuple/list (a, b):
        - If a is None -> assistant with content b
        - If a and b are strings -> treat as (user_message, assistant_message)
          and expand into two dicts.
        - Otherwise, stringify the item into an assistant message.
    - All other items are stringified as assistant messages.
    """
    normalized: list[dict] = []
    if not chat_history:
        return normalized

    for item in chat_history:
        if isinstance(item, dict) and "role" in item and "content" in item:
            normalized.append(item)
            continue

        if isinstance(item, (list, tuple)) and len(item) == 2:
            a, b = item
            if a is None:
                normalized.append({"role": "assistant", "content": str(b)})
                continue
            if isinstance(a, str) and isinstance(b, str):
                normalized.append({"role": "user", "content": a})
                normalized.append({"role": "assistant", "content": b})
                continue

       
        normalized.append({"role": "assistant", "content": str(item)})

    return normalized


SYSTEM_PROMPT = """You are an expert AI image prompt engineer.
Your ONLY job is to analyze an uploaded image and produce a high-quality,
detailed generation prompt that another AI (e.g. Stable Diffusion, Midjourney,
DALL-E) could use to recreate it as faithfully as possible.

Structure your output exactly like this:

**Prompt:**
<single, comma-separated prompt ready to paste into an image generation >

 **Breakdown:**
- **Subject:** ...
- **Style / Medium:** ...
- **Lighting:** ...
- **Color Palette:** ...
- **Composition:** ...
- **Mood / Atmosphere:** ...
- **Extra Details:** ...

Do NOT add commentary outside this structure."""


#logic

def generate_prompt(image_path: str, chat_history: list) -> tuple[list, str]:
    """Analyse the image and append the result to chat_history."""
    
    if not isinstance(chat_history, list):
        chat_history = []
    chat_history = normalize_chat_history(chat_history)

    if not image_path:
        chat_history.append({"role": "assistant", "content": " Please upload an image first."})
        return chat_history, ""

    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        chat_history.append({
            "role": "assistant",
            "content": "No API key found. Set the `GROQ_API_KEY` environment variable.",
        })
        return chat_history, ""

    try:
        b64, mime = encode_image(image_path)
        client = Groq(api_key=key)

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",   # vision capable model on Groq
            max_tokens=1024,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime};base64,{b64}"},
                        },
                        {
                            "type": "text",
                            "text": "Generate a detailed image prompt for this image.",
                        },
                    ],
                },
            ],
        )

        answer = response.choices[0].message.content
        chat_history.extend([
            {"role": "user", "content": "[Image uploaded] "},
            {"role": "assistant", "content": answer},
        ])

    except Exception as e:
        chat_history.extend([
            {"role": "user", "content": "[Image uploaded]"},
            {"role": "assistant", "content": f" Error: {e}"},
        ])

    # ensure output is always normalized dictionaries
    chat_history = normalize_chat_history(chat_history)
    return chat_history


def clear_all() -> tuple[list, None]:
    return [], None


#gradio ui

CSS = """
#title { text-align: center; }
#gen-btn { width: 100%; }
"""

with gr.Blocks(title="IMGCAP") as demo:

    gr.Markdown(
        "#  Image Prompt Generator\n",
        elem_id="title",
    )

    with gr.Row():
        # left side
        with gr.Column(scale=1, min_width=280):
            image_input = gr.Image(
                type="filepath",
                label=" Upload Image",
                height=280,
            )
            generate_btn = gr.Button(
                " Generate Prompt",
                variant="primary",
                size="lg",
                elem_id="gen-btn",
            )
            clear_btn = gr.Button(" Clear", variant="secondary", elem_id="gen-btn")

        # right side
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                label=" Generated Prompt",
                height=480,
                placeholder=" Generated prompt will appear here…",
            )

    gr.Markdown(
        "Supported formats: JPG, PNG, GIF, WebP",
        elem_id="title",
    )

    # buttons
    generate_btn.click(
        fn=generate_prompt,
        inputs=[image_input, chatbot],
        outputs=[chatbot],
    )

    image_input.upload(          # auto-generate as soon as image lands
        fn=generate_prompt,
        inputs=[image_input, chatbot],
        outputs=[chatbot],
    )

    clear_btn.click(
        fn=clear_all,
        outputs=[chatbot, image_input],
    )


if __name__ == "__main__":
    demo.launch(share=False)