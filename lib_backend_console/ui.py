import gradio as gr


def create_console_ui():
    return gr.Code(label='', elem_classes=['backend-console-textbox'], interactive=True)
