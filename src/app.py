# app.py
import gradio as gr

# uses your updated back-end that builds the LangGraph and logs memory
from chatbot.chatbot_backend import ChatBot
from chatbot.load_config import LoadProjectConfig
from utils.ui_settings import UISettings  # keep if you use like/dislike

CFG = LoadProjectConfig()  # ensures env + memory dir are prepared


def _respond(history, message):
    # ChatBot.respond returns ("", updated_history)
    return ChatBot.respond(history, message)


with gr.Blocks(title="AgentGraph") as demo:
    with gr.Tabs():
        with gr.TabItem("AgentGraph"):
            # --- Row 1: Chat window
            with gr.Row():
                chatbot = gr.Chatbot(
                    value=[],
                    elem_id="chatbot",
                    height=500,
                    bubble_full_width=False,
                    avatar_images=("images/AI_RT.png", "images/openai.png"),  # swap the right icon if you prefer
                )
                # optional thumbs up/down hook
                chatbot.like(UISettings.feedback, None, None)

            # --- Row 2: Input
            with gr.Row():
                input_txt = gr.Textbox(
                    lines=3,
                    scale=8,
                    autofocus=True,
                    placeholder="Ask anything. (Your chats are saved per thread_id to CSV)",
                    container=False,
                )

            # --- Row 3: Actions
            with gr.Row():
                send_btn = gr.Button("Send", variant="primary")
                clear_btn = gr.ClearButton([input_txt, chatbot])

            # --- Wiring
            input_txt.submit(
                fn=_respond,
                inputs=[chatbot, input_txt],
                outputs=[input_txt, chatbot],
                queue=False,
            ).then(lambda: gr.Textbox(interactive=True), None, [input_txt], queue=False)

            send_btn.click(
                fn=_respond,
                inputs=[chatbot, input_txt],
                outputs=[input_txt, chatbot],
                queue=False,
            ).then(lambda: gr.Textbox(interactive=True), None, [input_txt], queue=False)

if __name__ == "__main__":
    
    demo.launch()
