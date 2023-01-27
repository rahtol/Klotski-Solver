import tkinter as tk
import boardstate

cellsize = 100


class Piece(tk.Frame):
    dim = [[0, 0], [1, 1], [2, 1], [1, 2], [2, 2]]
    bgcolor = ['gray25', '#d6e398', '#d6e398', '#d6e398', '#B88']

    def __init__(self, master, typecode):
        self.typecode = typecode
        self.placed = False
        self.x = 0
        self.y = 0
        self.dx = Piece.dim[typecode][1] * cellsize
        self.dy = Piece.dim[typecode][0] * cellsize
        super().__init__(master, height=self.dy, width=self.dx)
        self.button = tk.Button(self, text='', padx=1, pady=1, borderwidth=2,
                                relief=tk.SOLID, bg=Piece.bgcolor[self.typecode])
        self.button.place(x=0, y=0, height=self.dy - 2, width=self.dx - 2)


def createPieces(master):
    pieces = []
    for i in range(4):
        pieces.append(Piece(master, 1))
        pieces.append(Piece(master, 2))
    pieces.append(Piece(master, 3))
    pieces.append(Piece(master, 4))
    return pieces


class KlotskiGui:

    def __init__(self, master):
        master.title("Klotski Gui")
        self.stepcounter = 0
        self.master = master
        self.main = tk.Frame(self.master)
        self.board = tk.Frame(self.main, height=5 * cellsize, width=4 * cellsize)
        self.pieces = createPieces(self.board)
        self.placePieces(boardstate.initial_boardstate)
        self.control = tk.Frame(self.main)
        self.next = tk.Button(self.control, text='Next', padx=10, command=self.next_step)
        self.prev = tk.Button(self.control, text='Prev', padx=10, command=self.prev_step)
        self.stepcounterlabel = tk.Label(self.control, text=f'#{self.stepcounter}', width=6)
        self.board.pack(side=tk.TOP)
        self.control.pack(side=tk.BOTTOM, pady=10)
        self.next.pack(side=tk.LEFT, padx=20)
        self.stepcounterlabel.pack(side=tk.LEFT)
        self.prev.pack(side=tk.RIGHT, padx=20)
        self.main.pack()

    def placePieces(self, bs):
        for idx in range(20):
            if bs.is_master_cell_of_piece(idx):
                # pick first available piece of appropriate typecode
                piece = [p for p in self.pieces if p.typecode == bs.cells[idx] and not p.placed][0]
                piece.placed = True  # make it unavailable
                piece.x = idx % 4
                piece.y = idx // 4
                piece.place(relx=piece.x / 4, rely=piece.y / 5)

    def next_step(self):
        if self.stepcounter < 1000:
            self.stepcounter = self.stepcounter + 1
            self.stepcounterlabel.configure(text=f'#{self.stepcounter}')
        pass

    def prev_step(self):
        if self.stepcounter > 0:
            self.stepcounter = self.stepcounter - 1
            self.stepcounterlabel.configure(text=f'#{self.stepcounter}')
        pass


root = tk.Tk()
gui = KlotskiGui(root)
root.mainloop()
