import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tifffile

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

        # Function to update the displayed image
        def update_image(index_str):
            index = int(index_str)  # Convert the string index to an integer
            print("Slider index:", index)
            frame = tiff_stack[index]
            ax.clear()
            ax.imshow(frame, cmap='gray')  # Assuming grayscale images
            ax.set_title("Frame {}".format(index))
            ax.axis('off')
            canvas.draw()
            print("Displayed frame:", index)

        # Slider to navigate through the stack
        slider = tk.Scale(root, from_=0, to=num_frames-1, orient=tk.HORIZONTAL, command=update_image)
        slider.pack()

        # Display the first frame initially
        fig, ax = plt.subplots()
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack()
        update_image(0)

        root.mainloop()

root = tk.Tk()
root.title("Open TIFF Stack")

open_button = tk.Button(root, text="Open TIFF Stack", command=open_tiff_stack)
open_button.pack()

root.mainloop()
