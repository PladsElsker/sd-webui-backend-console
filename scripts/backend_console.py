from modules import scripts
import gradio as gr

from lib_backend_console.webui_callbacks import append_callbacks
from lib_backend_console.ui import create_console_ui
from lib_backend_console.hijack_std_write import apply_hijack as apply_std_hijack
from lib_backend_console.settings import extension_enabled, get_backend_url, should_display_console


class BackendConsoleScript(scripts.Script):
    def title(self):
        return 'Backend Console'

    def ui(self, img2img):
        gr.HTML(value=f'<div id="backend_console_websocket_url" data-url="{get_backend_url()}" style="display: none;"></div>')

        if not should_display_console('In accordions'):
            return []
        if not extension_enabled():
            return []


        with gr.Accordion(label='Backend Console'):
            create_console_ui()

        return []

    def show(self, img2img):
        return scripts.AlwaysVisible


if extension_enabled():
    apply_std_hijack()


append_callbacks()
