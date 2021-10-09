import pystray
from pystray import MenuItem as item
from PIL import Image
import ctypes
import os


class Systray():
    def __init__(self, handle):
        self.handle = handle
        self.closed = False


        # menu = (
        #            item('Show/Hide window', lambda:  self.on_clicked()),
        # )
        # self.icon = pystray.Icon('Valorant skin downgrader', self.load_image(), menu=menu)

    def load_image(self):
        with Image.open("assets/icon.ico") as img:
            return img

    def on_clicked(self):
        self.closed = not self.closed
        if self.closed:
            ctypes.windll.user32.ShowWindow(self.handle, 0)
        else:
            ctypes.windll.user32.ShowWindow(self.handle, 1)


    def loop(self):
        menu = pystray.Menu(
                   item('Show/Hide window', lambda:  self.on_clicked()),
                   item('Quit', lambda:  os._exit(1)())
        )


        self.icon = pystray.Icon('Valorant skin downgrader', self.load_image(), menu=menu)

        self.icon.run()



