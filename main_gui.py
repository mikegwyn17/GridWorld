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
        self.arrows = ["\U00002191", "\U00002193", "\U00002190", "\U00002192"]
        self.fonts = {
            'small': font.Font(family="Arial", size=6),
            'medium': font.Font(family="Arial", size=14),
            'large': font.Font(family="Arial", size=24)
        }
        self.setup_world()
        self.agent = Agent(self.rewards)

    def setup_world(self):
        self.cells = []
        self.rewards = []
        with open('world_map.txt', 'r') as f:
            self.rewards = [
                [-1 * int(x) for x in line.split(',')]
                for line in f.readlines()
            ]
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
                if self.rewards[row][col] == -1:
                    cell.config(bg="black")
                elif self.rewards[row][col] == 1:
                    cell.config(text="$", font=self.fonts['large'], bg="green", fg="white")
                else:
                    cell.config(bg="white", fg="black", font=self.fonts['small'])
                self.cells[row].append(cell)

    def update_grid(self):
        for i in range(1, 21):
            for j in range(1, 21):
                if (
                    (i, j) == (self.agent.row, self.agent.col) and
                    not self.rewards[i][j]
                ):
                    self.cells[i][j].config(text="\U00002620", bg="blue", fg="white", font=self.fonts['large'])
                elif not self.rewards[i][j]:
                    arrow = self.arrows[self.agent.best_action(i, j)]
                    best = self.agent.best_value(i, j)
                    if best < 0.25:
                        afont = self.fonts['small']
                    elif best < 0.75:
                        afont = self.fonts['medium']
                    else:
                        afont = self.fonts['large']
                    self.cells[i][j].config(text=arrow, bg="white", fg="black", font=afont)
        self.update()

    def episode(self):
        self.agent.spawn()
        self.update_grid()
        while not self.rewards[self.agent.row][self.agent.col]:
            self.agent.take_step()
            r = self.rewards[self.agent.row][self.agent.col]
            if r:
                last = 'GOAL' if r == 1 else 'WALL'
                print('Terminating on {}'.format(last))
            self.update_grid()
        self.agent.epsilon -= 0.001

    def run(self, episodes):
        for i in range(episodes):
            self.episode()

root = Tk()
root.title("Grid World")

main = GridWorldGUI(root)

menubar = Menu(root)
run_menu = Menu(menubar, tearoff=0)
run_menu.add_command(label="Once", command=(lambda: main.run(1)))
run_menu.add_command(label="x100", command=(lambda: main.run(100)))
run_menu.add_command(label="x250", command=(lambda: main.run(250)))
run_menu.add_command(label="x500", command=(lambda: main.run(500)))
run_menu.add_command(label="x1000", command=(lambda: main.run(1000)))
menubar.add_cascade(label="Run Episode", menu=run_menu)
menubar.add_command(label="Exit", command=root.quit)
root.config(menu=menubar)

root.mainloop()

