from tkinter import *
from backprop import *

# size of the grid
width = 15
height = 15


class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Backpropagation")
        self.root.geometry("250x250")
        self.dragging = False

        # create a grid
        self.grid = Canvas(self.root, width=width * 10 + 1, height=height * 10 + 1, highlightthickness=0)
        for i in range(height):
            for j in range(width):
                x1 = (j * 10)
                x2 = (x1 + 10)
                y1 = (i * 10)
                y2 = (y1 + 10)
                self.grid.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")

        # bind mouse actions to the grid
        # left button - draw
        self.grid.bind("<ButtonPress-1>", self.on_button_press)
        self.grid.bind("<B1-Motion>", self.on_move_press)
        self.grid.bind("<ButtonRelease-1>", self.on_button_release)
        # right button - erase
        self.grid.bind("<ButtonPress-3>", self.right_on_button_press)
        self.grid.bind("<B3-Motion>", self.right_on_move_press)
        self.grid.bind("<ButtonRelease-3>", self.on_button_release)
        self.grid.pack()

        # label for an answer
        self.label = Label(root, text="")
        self.label.pack()

        self.guess_button = Button(self.root, text="Guess!", command=self.guess)
        self.guess_button.pack()

        self.clear_button = Button(self.root, text="Clear", command=self.clear)
        self.clear_button.pack()

    def guess(self):
        num = []
        items = self.grid.find_all()

        # read values from the grid
        for item in items:
            if self.grid.itemcget(item, "fill") == "black":
                num.append(1)
            else:
                num.append(0)

        # send the values to the input of the network
        t = findNum(num)
        if t is None:
            self.label.config(text="Recognition failed. Try once more.")
        else:
            self.label.config(text="The number/letter is " + t)

    def clear(self):
        items = self.grid.find_all()
        for item in items:
            self.grid.itemconfigure(item, fill="white")
        self.label.config(text="")

    def on_button_press(self, event):
        self.dragging = True
        self.on_move_press(event)

    def on_move_press(self, event):
        if self.dragging:
            items = self.grid.find_closest(event.x, event.y)
            if items:
                self.grid.itemconfigure(items[0], fill="black")

    def on_button_release(self, event):
        self.dragging = False

    def right_on_button_press(self, event):
        self.dragging = True
        self.right_on_move_press(event)

    def right_on_move_press(self, event):
        if self.dragging:
            items = self.grid.find_closest(event.x, event.y)
            if items:
                self.grid.itemconfigure(items[0], fill="white")


def main():
    # initialize and train the network
    init()
    train()

    # start GUI
    root = Tk()
    Gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
