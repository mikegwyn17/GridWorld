from tkinter import *
import tkinter.font as font
from sarsa_lambda import Agent
from time import sleep


class GridWorldGUI(Frame):

    def __init__(self, root):
        super().__init__(root)
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.agent = Agent()
        self.setup_world()
        self.arrows = ["\U00002191", "\U00002193", "\U00002190", "\U00002192"]

    def setup_world(self):
        self.cells = []
        self.label_font = font.Font(family="Arial", size=24, weight="bold")
        for row in range(22):
            self.cells.append([])
            row_container = Frame(self)
            row_container.pack(side=TOP)
            for col in range(22):
                cell_container = Frame(row_container, height=40, width=40)
                cell_container.pack_propagate(False)
                cell_container.pack(side=LEFT)
                cell = Button(cell_container, state=DISABLED)
                cell.pack(fill=BOTH, expand=1)
                if row in [0, 21] or col in [0, 21]:
                    cell.reward = -1
                    cell.config(bg="black")
                elif row == 2 and col == 18:
                    cell.reward = 1
                    cell.config(text="$", font=self.label_font, bg="green", fg="white")
                else:
                    cell.reward = 0
                    cell.config(font=self.label_font, bg="white")
                self.cells[row].append(cell)

    def update_grid(self):
        for i in range(1, 21):
            for j in range(1, 21):
                if (i, j) == (self.agent.row, self.agent.col):
                    self.cells[i][j].config(text="\U00002620", bg="blue", fg="white")
                elif i == 2 and j == 18:
                    continue
                else:
                    arrow = self.arrows[self.agent.best_action(i, j)]
                    self.cells[i][j].config(text=arrow, bg="white", fg="black")
        self.update()

    def episode(self):
        self.agent.spawn()
        self.update_grid()
        while not self.cells[self.agent.row][self.agent.col].reward:
            self.agent.take_step(
                self.cells[self.agent.row][self.agent.col].reward
            )
            self.update_grid()

root = Tk()
root.title("Grid World")

main = GridWorldGUI(root)

menubar = Menu(root)
menubar.add_command(label="Start", command=main.episode)
menubar.add_command(label="Exit", command=root.quit)
root.config(menu=menubar)

root.mainloop()

