import gradio as gr
import google.generativeai as genai
import os
#from dotenv import load_dotenv
import time
import typing_extensions as typing


def chatting(message, history):
    if len(message["files"]) == 0: # No files attached
        try:
            response = chat.send_message(
                message["text"], stream=True,
                generation_config = genai.types.GenerationConfig(temperature=0.0),

            )
            response.resolve()

        except: # Rewind and resend if exception
            chat.rewind()
            response = chat.send_message(
                message["text"], stream=True,
                generation_config = genai.types.GenerationConfig(temperature=0.0),

            )
            response.resolve()

        finally: # Output
            for i in range(len(response.text)):
                time.sleep(0.005)
                yield response.text[: i+1]

    else: # File attached to message
        filePath = message["files"][0].get("path")
        file = genai.upload_file(filePath)
        try:            
            response = chat.send_message(
                [message["text"], file], stream=True,
                generation_config = genai.types.GenerationConfig(temperature=0.0),

            )
            response.resolve()

        except: # Rewind and resend if exception
            chat.rewind()
            response = chat.send_message(
                [message["text"], file], stream=True,
                generation_config = genai.types.GenerationConfig(temperature=0.0),

            )
            response.resolve()

        finally:
            for i in range(len(response.text)):
                time.sleep(0.005)
                yield response.text[: i+1]



with gr.Blocks(fill_height=True) as demo:
    chatbot = gr.ChatInterface(
        fn=chatting,
        title="Your personal cooking assistant",
        multimodal = True
    )

if __name__ == "__main__":
    #load_dotenv()
    genai.configure(api_key=os.environ["API_KEY"])
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction="You are an expert chef, provide assistance with cooking related questions only, no small talk",

    )
    chat = model.start_chat(history=[])
    demo.launch()