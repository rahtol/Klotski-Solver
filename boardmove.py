from boardstate import Boardstate


class Boardmove:
    def __init__(self, piece_idx, dx, dy):
        self.piece_idx = piece_idx
        self.dx = dx
        self.dy = dy


def detect_move(bs0: Boardstate, bs1: Boardstate):
    # TODO
    return Boardmove(14, 0, 1)

