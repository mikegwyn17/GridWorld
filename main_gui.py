from tkinter import *


class GridWorldGUI(Frame):

    def __init__(self, root):
        super().__init__(root)
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.setup_world()

    def setup_world(self):
        self.cells = []
        for row in range(22):
            self.cells.append([])
            row_container = Frame(self)
            row_container.pack(side=TOP)
            for col in range(22):
                cell_container = Frame(row_container, height=40, width=40)
                cell_container.pack_propagate(False)
                cell_container.pack(side=LEFT)
                cell = Button(cell_container)
                cell.pack(fill=BOTH, expand=1)
                self.cells[row].append(cell)

root = Tk()
root.title("Grid World")

main = GridWorldGUI(root)
#main.cells[4][4].config(text="^", compound=CENTER)

root.mainloop()

