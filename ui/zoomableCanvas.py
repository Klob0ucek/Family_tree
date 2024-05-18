import tkinter as tk
from PIL import Image, ImageTk


class ZoomableImageCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.image_name = None
        self.image = None
        self.image_ref = None
        self.zoom_factor = 1.0
        self.pan_start_x = 0
        self.pan_start_y = 0

        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Button-4>", self._on_mousewheel)  # Linux
        self.bind("<Button-5>", self._on_mousewheel)  # Linux
        self.bind("<ButtonPress-1>", self._start_pan)
        self.bind("<B1-Motion>", self._pan_image)

    def load_image(self):
        image_path = self.image_name
        image = Image.open(image_path)
        self.image_ref = ImageTk.PhotoImage(image)
        self.image = self.create_image(0, 0, anchor=tk.NW,
                                       image=self.image_ref)

    def _on_mousewheel(self, event):
        if event.delta > 0:
            self.zoom_in()
        elif event.delta < 0:
            self.zoom_out()

    def zoom_in(self):
        self.zoom_factor *= 1.1
        self._apply_zoom()

    def zoom_out(self):
        self.zoom_factor /= 1.1
        self._apply_zoom()

    def _apply_zoom(self):
        new_width = int(self.image_ref.width() * self.zoom_factor)
        new_height = int(self.image_ref.height() * self.zoom_factor)

        image = Image.open(self.image_name)
        image_resized = image.resize((new_width, new_height),
                                     Image.LANCZOS)
        self.image_ref = ImageTk.PhotoImage(image_resized)
        self.itemconfig(self.image, image=self.image_ref)

    def _start_pan(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def _pan_image(self, event):
        delta_x = event.x - self.pan_start_x
        delta_y = event.y - self.pan_start_y

        self.scan_mark(0, 0)  # Reset the scan mark
        self.scan_dragto(delta_x, delta_y, gain=1)

        self.pan_start_x = event.x
        self.pan_start_y = event.y

    def reset_image(self, filename):
        self.image_name = filename + ".png"
        self.zoom_factor = 1.0
        self.load_image()
