from boardstate import Boardstate, down, up, right, left
from boardstate import xy_from_idx


class Boardmove:
    def __init__(self, piece_idx, dx, dy, cleared, occupied):
        self.piece_idx = piece_idx
        self.dx = dx
        self.dy = dy
        self.cleared = cleared
        self.occupied = occupied

    def map_idx(self,idx=-99):
        if idx == -99:
            idx = self.piece_idx
        idx_out = idx + self.dx + 4 * self.dy
        assert 0 <= idx_out <= 19
        return idx_out


def detect_move(bs0: Boardstate, bs1: Boardstate) -> Boardmove:
    cleared = [idx for idx in range(20) if bs0.cells[idx] != 0 and bs1.cells[idx] == 0]
    occupied = [idx for idx in range(20) if bs0.cells[idx] == 0 and bs1.cells[idx] != 0]
    assert 1 <= len(cleared) <= 2
    assert len(cleared) == len(occupied)
    x_occ, y_occ = xy_from_idx(occupied[0])
    x_cl, y_cl = xy_from_idx(cleared[0])
    dx = x_occ - x_cl
    dy = y_occ - y_cl
    if dx != 0 and bs0.cells[cleared[0]] == 3:
        dx = len(cleared) if dx > 0 else -len(cleared)
    if dy != 0 and bs0.cells[cleared[0]] == 2:
        dy = len(cleared) if dy > 0 else -len(cleared)
    if dx != 0 and bs0.cells[cleared[0]] == 4:
        dx = 1 if dx > 0 else -1
    if dy != 0 and bs0.cells[cleared[0]] == 4:
        dy = 1 if dy > 0 else -1
    piece_idx = bs0.get_piece_reference_idx(cleared[0])
    return Boardmove(piece_idx, dx, dy, cleared, occupied)


def apply_move(bs: Boardstate, move: Boardmove) -> Boardstate:
    if bs.cells[move.piece_idx] == 1:
        # movement of 1x1 piece either horizontally or vertically
        assert len(move.cleared) == 1
        ret = Boardstate([0 if i == move.piece_idx else
                          1 if i == move.map_idx() else
                          x for i, x in enumerate(bs.cells)])
    elif bs.cells[move.piece_idx] == 2 and move.dx != 0:
        # movement of 2x1 piece horizontally along short axis
        assert len(move.cleared) == 2
        ret = Boardstate([0 if i in [move.piece_idx, down(move.piece_idx)] else
                          2 if i in [move.map_idx(), down(move.map_idx())] else
                          x for i, x in enumerate(bs.cells)])
    elif bs.cells[move.piece_idx] == 2 and move.dy == -1:
        # movement of 2x1 piece vertically up along long axis
        ret = Boardstate([0 if i == down(move.piece_idx) else
                          2 if i == up(move.piece_idx) else
                          x for i, x in enumerate(bs.cells)])
    elif bs.cells[move.piece_idx] == 2 and move.dy == 1:
        # movement of 2x1 piece vertically down along long axis
        ret = Boardstate([0 if i == move.piece_idx else
                          2 if i == down(down(move.piece_idx)) else
                          x for i, x in enumerate(bs.cells)])
    elif bs.cells[move.piece_idx] == 3 and move.dy != 0:
        # movement of 1x2 piece vertically along short axis
        assert len(move.cleared) == 2
        ret = Boardstate([0 if i in [move.piece_idx, right(move.piece_idx)] else
                          3 if i in [move.map_idx(), right(move.map_idx())] else
                          x for i, x in enumerate(bs.cells)])
    elif bs.cells[move.piece_idx] == 3 and move.dx == -1:
        # movement of 1x2xpiece horizontally left along long axis
        ret = Boardstate([0 if i == right(move.piece_idx) else
                          3 if i == left(move.piece_idx) else
                          x for i, x in enumerate(bs.cells)])
    elif bs.cells[move.piece_idx] == 3 and move.dx == 1:
        # movement of 1x2 piece horizontally right along long axis
        ret = Boardstate([0 if i == move.piece_idx else
                          3 if i == right(right(move.piece_idx)) else
                          x for i, x in enumerate(bs.cells)])
    elif bs.cells[move.piece_idx] == 4:
        # movement of 2x2 piece either horizontally or vertically
        assert len(move.cleared) == 2
        ret = Boardstate([0 if i in move.cleared else
                          4 if i in move.occupied else
                          x for i, x in enumerate(bs.cells)])
    return ret
