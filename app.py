"""
python 3.7.9

Pendulum entry point
"""
from ui.ui_builder import UiBuilder
from pyautogui import size
from configparser import ConfigParser

def parser() -> ConfigParser:
    config = ConfigParser()
    config.read('config.ini')

    return config

def main() -> None:
    app_name = parser()['app']['name']
    font_size = float(parser()['app']['font_size'])
    wireframe = UiBuilder(height=size().height, 
    width=size().width, theme='Dark')
    wireframe.make_gui(app_name=app_name, font_size=font_size, width=size().width, height=size().height)
    wireframe.run_gui()

if __name__ == "__main__":
    main()