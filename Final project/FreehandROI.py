import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
import tifffile

class FreehandDrawer:
    def __init__(self, ax, canvas):
        self.ax = ax
        self.canvas = canvas
        self.poly = None
        self.coords = []

    def start_drawing(self):
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)

    def on_click(self, event):
        if event.button == 1:
            self.coords.append((event.xdata, event.ydata))

    def on_motion(self, event):
        if event.button == 1 and len(self.coords) > 0:
            if self.poly:
                self.poly.remove()
            self.coords.append((event.xdata, event.ydata))
            self.poly = Polygon(self.coords, closed=False, fill=None, edgecolor='red')
            self.ax.add_patch(self.poly)
            self.canvas.draw()

    def on_release(self, event):
        if event.button == 1:
            self.coords.append((event.xdata, event.ydata))
            if self.poly:
                if self.is_enclosed():
                    self.poly.set_closed(True)
                else:
                    self.poly.remove()
                self.poly = None

    def is_enclosed(self):
        if len(self.coords) < 3:
            return False
        x_coords, y_coords = zip(*self.coords)
        return min(x_coords) != max(x_coords) and min(y_coords) != max(y_coords)

    def get_polygon(self):
        return self.coords

def open_tiff_stack():
    file_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tif")])
    if file_path:
        # Read TIFF stack
        tiff_stack = tifffile.imread(file_path)

        num_frames, frame_height, frame_width = tiff_stack.shape

        print("Number of frames in TIFF stack:", num_frames)
        print("Frame width:", frame_width)
        print("Frame height:", frame_height)

        # Create GUI window
        root = tk.Tk()
        root.title("TIFF Stack Viewer")

        # Create Freehand Drawer
        fig, ax = plt.subplots()
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack()

        freehand_drawer = FreehandDrawer(ax, canvas)

        # Function to update the displayed image
        def update_image(index_str):
            index = int(index_str)  # Convert the string index to an integer
            print("Slider index:", index)
            frame = tiff_stack[index]
            ax.clear()
            ax.imshow(frame, cmap='gray')  # Assuming grayscale images
            ax.set_title("Frame {}".format(index))
            ax.axis('off')
            if freehand_drawer.get_polygon():
                poly = Polygon(freehand_drawer.get_polygon(), closed=True, fill=None, edgecolor='red')
                ax.add_patch(poly)
            canvas.draw()
            print("Displayed frame:", index)

        # Slider to navigate through the stack
        slider = tk.Scale(root, from_=0, to=num_frames-1, orient=tk.HORIZONTAL, command=update_image)
        slider.pack()

        # Function to activate freehand drawing
        def draw_freehand():
            freehand_drawer.start_drawing()

        # Button to draw freehand
        draw_freehand_button = tk.Button(root, text="Draw Freehand", command=draw_freehand)
        draw_freehand_button.pack()

        # Display the first frame initially
        update_image(0)

        root.mainloop()

root = tk.Tk()
root.title("Open TIFF Stack")

open_button = tk.Button(root, text="Open TIFF Stack", command=open_tiff_stack)
open_button.pack()

root.mainloop()
