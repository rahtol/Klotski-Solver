import tkinter as tk
from boardstate import Boardstate
from boardstate import xy_from_idx
from boardmove import detect_move
import boardstate_sequence

CELLSIZE = 100


class Piece(tk.Frame):
    DIM = [[0, 0], [1, 1], [2, 1], [1, 2], [2, 2]]
    BG_COLOR = ['gray25', '#d6e398', '#d6e398', '#d6e398', '#B88']

    def __init__(self, master, typecode):
        self.typecode = typecode
        self.placed = False
        self.x = 0
        self.y = 0
        self.dx = Piece.DIM[typecode][1]
        self.dy = Piece.DIM[typecode][0]
        super().__init__(master, height=self.dy * CELLSIZE, width=self.dx * CELLSIZE)
        self.button = tk.Button(self, text='', padx=1, pady=1, borderwidth=2,
                                relief=tk.SOLID, bg=Piece.BG_COLOR[self.typecode])
        self.button.place(x=0, y=0, height=self.dy * CELLSIZE - 2, width=self.dx * CELLSIZE - 2)


def create_pieces(master):
    pieces = []
    for i in range(4):
        pieces.append(Piece(master, 1))
        pieces.append(Piece(master, 2))
    pieces.append(Piece(master, 3))
    pieces.append(Piece(master, 4))
    return pieces


class KlotskiGui:
#    boardstate_sequence_fn = 'youtube-solution.txt'
    boardstate_sequence_fn = 'solution-117-1.txt'

    def __init__(self, master):
        master.title("Klotski Gui")
        self.boardstate_sequence = boardstate_sequence.read_from_file(self.boardstate_sequence_fn)
        self.stepcounter = 0
        self.master = master
        self.main = tk.Frame(self.master)
        self.board = tk.Frame(self.main, height=5 * CELLSIZE, width=4 * CELLSIZE)
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

    def find_piece(self, idx: int) -> Piece:
        x, y = xy_from_idx(idx)
        candidates = [p for p in self.pieces if p.x <= x < p.x + p.dx and p.y <= y < p.y + p.dy]
        assert len(candidates) == 1
        return candidates[0]

    def place_pieces(self, bs: Boardstate):
        for idx in range(20):
            if bs.is_master_cell_of_piece(idx):
                # pick first available piece of appropriate typecode
                piece = [p for p in self.pieces if p.typecode == bs.cells[idx] and not p.placed][0]
                piece.placed = True  # make it unavailable
                piece.x, piece.y = xy_from_idx(idx)
                piece.place(relx=piece.x / 4, rely=piece.y / 5)

    def next_step(self):
        if self.stepcounter < len(self.boardstate_sequence) - 1:
            move = detect_move(self.boardstate_sequence[self.stepcounter],
                               self.boardstate_sequence[self.stepcounter + 1])
            piece = self.find_piece(move.piece_idx)
            piece.x = piece.x + move.dx
            piece.y = piece.y + move.dy
            piece.place(relx=piece.x / 4, rely=piece.y / 5)
            self.stepcounter = self.stepcounter + 1
            self.stepcounter_label.configure(text=f'#{self.stepcounter}')

    def prev_step(self):
        if self.stepcounter > 0:
            move = detect_move(self.boardstate_sequence[self.stepcounter],
                               self.boardstate_sequence[self.stepcounter - 1])
            piece = self.find_piece(move.piece_idx)
            piece.x = piece.x + move.dx
            piece.y = piece.y + move.dy
            piece.place(relx=piece.x / 4, rely=piece.y / 5)
            self.stepcounter = self.stepcounter - 1
            self.stepcounter_label.configure(text=f'#{self.stepcounter}')


root = tk.Tk()
gui = KlotskiGui(root)
root.mainloop()
