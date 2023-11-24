import gradio as gr

from modules.shared import opts, OptionInfo
from modules import ui_components


display_locations_choices = ['Under preview image', 'Above footer', 'In accordions']
display_locations_default = [display_locations_choices[0]]
backend_url_default = 'localhost:7860'


def create_settings_section():
    section = ('backend_console', 'Backend Console')

    opts.add_option('backend_console_enabled', OptionInfo(True, 'Enable backend-console extension', section=section).needs_restart())
    opts.add_option('backend_console_url', OptionInfo(backend_url_default, 'Backend URL', gr.Textbox, {'placeholder': 'url:port'}, section=section).needs_restart())
    opts.add_option('backend_console_display_locations', OptionInfo(display_locations_default, 'Display the console at these locations', ui_components.DropdownMulti, {'choices': display_locations_choices}, section=section).needs_reload_ui())


def extension_enabled():
    return opts.data.get('backend_console_enabled', True)


def get_backend_url():
    return opts.data.get('backend_console_url', backend_url_default)


def should_display_console(str_location):
    return str_location in opts.data.get('backend_console_display_locations', display_locations_default)
