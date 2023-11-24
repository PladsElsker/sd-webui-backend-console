import gradio
from fastapi import FastAPI
from gradio.context import Context as GradioContext

from modules import script_callbacks

from lib_backend_console.settings import create_settings_section, extension_enabled, should_display_console
from lib_backend_console.websocket_server import websocket_server
from lib_backend_console.ui import create_console_ui


class GradioContextSwitch:
    def __init__(self, block):
        self.block = block

    def __enter__(self):
        self.previous_block = GradioContext.block
        GradioContext.block = self.block
        return self

    def __exit__(self, *args, **kwargs):
        GradioContext.block = self.previous_block


def on_ui_settings():
    create_settings_section()


def on_after_component(component, **kwargs):
    elem_id = kwargs.get('elem_id', None)

    if elem_id is None:
        return

    if elem_id in ['txt2img_send_to_extras', 'img2img_send_to_extras']:
        if should_display_console('Under preview image'):
            with GradioContextSwitch(component.parent.parent):
                create_console_ui()

    if elem_id == 'footer':
        if should_display_console('Above footer'):
            with GradioContextSwitch(component.parent):
                footer = component.parent.children[-1]
                component.parent.children = component.parent.children[:-1]
                create_console_ui()
                component.parent.children.append(footer)



def on_app_started(_, app: FastAPI):
    websocket_server(app)


def append_callbacks():
    script_callbacks.on_ui_settings(on_ui_settings)
    if extension_enabled():
        script_callbacks.on_after_component(on_after_component)
        script_callbacks.on_app_started(on_app_started)
