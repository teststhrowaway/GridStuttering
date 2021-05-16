from functools import partial
from threading import Thread
from time import sleep
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image, CoreImage
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from io import BytesIO

def get_image():
    file = open('./no-cover.png', 'rb')
    bytes_io = BytesIO(file.read())
    return bytes_io, 'png'


class Page(Image):
    def set_image(self, image, ext):
        image.seek(0)
        core = CoreImage(image, ext=ext)
        self.texture = core.texture
        return core.texture.size


class MainApp(App):
    pages_grid = ObjectProperty()

    def on_start(self, *args):
        self.pages_grid = self.root.ids['pages_grid']
        self.scroller = self.root.ids['scroller']
        Clock.schedule_once(self.start_images, 2)

    def start_images(self, *args):
        page_widgets = []
        for i in range(25):
            page = Page()
            self.pages_grid.add_widget(page)
            page_widgets.append(page)
        Thread(target=partial(self.load_images, page_widgets), daemon=True).start()

    def load_images(self, widgets, *args):
        for widget in widgets:
            image, ext = get_image()
            Clock.schedule_once(partial(self.show_image, widget, image, ext), 0)
            sleep(0.5)
        print('all images loaded')
    
    def show_image(self, widget, image, ext, time_delta):
        widget.set_image(image, ext)


if __name__ == '__main__':
    MainApp().run()