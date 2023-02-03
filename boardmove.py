from boardstate import Boardstate


class Boardmove:
    def __init__(self, piece_idx, dx, dy):
        self.piece_idx = piece_idx
        self.dx = dx
        self.dy = dy


def detect_move(bs0: Boardstate, bs1: Boardstate):
    cleared = [idx for idx in range(20) if bs0.cells[idx] != 0 and bs1.cells[idx] == 0]
    occupied = [idx for idx in range(20) if bs0.cells[idx] == 0 and bs1.cells[idx] != 0]
    assert 1 <= len(cleared) <= 2
    assert len(cleared) == len(occupied)
    x_occ = occupied[0] % 4
    y_occ = occupied[0] // 4
    x_cl = cleared[0] % 4
    y_cl = cleared[0] // 4
    dx = x_occ-x_cl
    dy = y_occ-y_cl
    if dx != 0 and bs0.cells[cleared[0]] == 3:
        dx = len(cleared) if dx > 0 else -len(cleared)
    if dy != 0 and bs0.cells[cleared[0]] == 2:
        dy = len(cleared) if dy > 0 else -len(cleared)
    if dx != 0 and bs0.cells[cleared[0]] == 4:
        dx = 1 if dx > 0 else -1
    if dy != 0 and bs0.cells[cleared[0]] == 4:
        dy = 1 if dy > 0 else -1
    return Boardmove(cleared[0], dx, dy)

