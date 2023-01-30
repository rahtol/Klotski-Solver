import tkinter as tk
from boardstate import Boardstate
from KlotskiSolver import bs_from_str
from boardmove import detect_move

cellsize = 100


class Piece(tk.Frame):
    dim = [[0, 0], [1, 1], [2, 1], [1, 2], [2, 2]]
    bg_color = ['gray25', '#d6e398', '#d6e398', '#d6e398', '#B88']

    def __init__(self, master, typecode):
        self.typecode = typecode
        self.placed = False
        self.x = 0
        self.y = 0
        self.dx = Piece.dim[typecode][1]
        self.dy = Piece.dim[typecode][0]
        super().__init__(master, height=self.dy * cellsize, width=self.dx * cellsize)
        self.button = tk.Button(self, text='', padx=1, pady=1, borderwidth=2,
                                relief=tk.SOLID, bg=Piece.bg_color[self.typecode])
        self.button.place(x=0, y=0, height=self.dy * cellsize - 2, width=self.dx * cellsize - 2)


def create_pieces(master):
    pieces = []
    for i in range(4):
        pieces.append(Piece(master, 1))
        pieces.append(Piece(master, 2))
    pieces.append(Piece(master, 3))
    pieces.append(Piece(master, 4))
    return pieces


def read_boardstate_sequence_from_file(fn: str):
    boardstate_sequence = []
    with open(fn, 'r') as f:
        for line in f:
            bs = bs_from_str(line)
            if bs is not None:
                boardstate_sequence.append(bs)
    return boardstate_sequence


class KlotskiGui:
    boardstate_sequence_fn = 'shortest-solution.txt'

    def __init__(self, master):
        master.title("Klotski Gui")
        self.boardstate_sequence = read_boardstate_sequence_from_file(self.boardstate_sequence_fn)
        self.stepcounter = 0
        self.master = master
        self.main = tk.Frame(self.master)
        self.board = tk.Frame(self.main, height=5 * cellsize, width=4 * cellsize)
        self.pieces = create_pieces(self.board)
        self.place_pieces(self.boardstate_sequence[0])
        self.control = tk.Frame(self.main)
        self.next = tk.Button(self.control, text='Next', padx=10, command=self.next_step)
        self.prev = tk.Button(self.control, text='Prev', padx=10, command=self.prev_step)
        self.stepcounter_label = tk.Label(self.control, text=f'#{self.stepcounter}', width=6)
        self.board.pack(side=tk.TOP)
        self.control.pack(side=tk.BOTTOM, pady=10)
        self.next.pack(side=tk.LEFT, padx=20)
        self.stepcounter_label.pack(side=tk.LEFT)
        self.prev.pack(side=tk.RIGHT, padx=20)
        self.main.pack()

    def find_piece(self, idx: int) -> Boardstate:
        x = idx % 4
        y = idx // 4
        cand = [p for p in self.pieces if p.x <= x < p.x + p.dx and p.y <= y < p.y + p.dy]
        assert len(cand) == 1
        return cand [0]

    def place_pieces(self, bs):
        for idx in range(20):
            if bs.is_master_cell_of_piece(idx):
                # pick first available piece of appropriate typecode
                piece = [p for p in self.pieces if p.typecode == bs.cells[idx] and not p.placed][0]
                piece.placed = True  # make it unavailable
                piece.x = idx % 4
                piece.y = idx // 4
                piece.place(relx=piece.x / 4, rely=piece.y / 5)

    def next_step(self):
        if self.stepcounter < len(self.boardstate_sequence)-1:
            self.stepcounter = self.stepcounter + 1
            self.stepcounter_label.configure(text=f'#{self.stepcounter}')
            move = detect_move(self.boardstate_sequence[self.stepcounter], self.boardstate_sequence[self.stepcounter+1])
            piece = self.find_piece(move.piece_idx)
            piece.x = piece.x + move.dx
            piece.y = piece.y + move.dy
            piece.place(relx=piece.x / 4, rely=piece.y / 5)

    def prev_step(self):
        if self.stepcounter > 0:
            self.stepcounter = self.stepcounter - 1
            self.stepcounter_label.configure(text=f'#{self.stepcounter}')
        pass


root = tk.Tk()
gui = KlotskiGui(root)
root.mainloop()
