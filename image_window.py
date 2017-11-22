import tkinter
__name__ = "image_window"

class ImageWindow:
    def __init__(self, root, title, image):
        self.root = root
        self.root.title(title)
        self.root.resizable(0, 0)
        self.label = tkinter.Label(self.root, image = image)
        self.label.image = image
        self.label.grid(row = 1, column = 1)

    def start(self):
        self.root.mainloop()

    def keybind(self, func):
        self.root.bind("<Key>", func)

    def update(self, image):
        new_label = tkinter.Label(self.root, image = image)
        new_label.image = image
        self.label.grid_forget()
        self.label.destroy()
        self.label = new_label
        self.label.grid(row = 1, column = 1)