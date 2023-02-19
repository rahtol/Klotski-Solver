import re


# cellstate is represented by list of 20 integers where
#   idx = row * 4 * col, i.e. col = idx %4, row = idx // 4 with rages raw 0..3, col 0..4
#   cells[idx] = 0, 1, 2, 3, 4 with
#       0=empy cell,
#       1= cell occupied by 1x1 piece
#       2= cell occupied by 2x1 piece, vertical piece of size 2
#       3= cell occupied by 1x2 piece, horizontal piece of size 2
#       4= cell occupied by 2x2 piece, the red one

def xy_from_idx(idx: int) -> (int, int):
    return idx % 4, idx // 4


def xy_to_idx(x: int, y: int) -> int:
    return y * 4 + x


def up(idx: int) -> int:
    if idx >= 4:
        return idx - 4
    else:
        return -1


def down(idx: int) -> int:
    if idx != -1 and idx < 16:
        return idx + 4
    else:
        return -1


def left(idx: int) -> int:
    if idx >= 1 and idx % 4 != 0:
        return idx - 1
    else:
        return -1


def right(idx: int) -> int:
    if idx != -1 and idx % 4 != 3:
        return idx + 1
    else:
        return -1


class Boardstate:

    def calc_hashval(self):
        h = 0
        for cell in self.cells:
            h = (h << 2) + cell
        return h

    def __init__(self, cells):
        self.cells = cells
        self.hashval = self.calc_hashval()
        self.pred = None

    def __hash__(self):
        return self.hashval

    def __eq__(self, other):
        return self.hashval == other.hashval

    def get_cell_occupation(self, idx):
        if idx < 0 or idx > 19:
            return -1
        else:
            return self.cells[idx]

    def is_final(self):
        return self.cells[13] == 4 and self.cells[18] == 4

    def get_piece_reference_idx(self, idx: int) -> int:
        assert 0 < self.cells[idx] <= 4
        if self.cells[idx] == 1:
            reference_idx = idx
        elif self.cells[idx] == 2:
            above = self.get_cell_occupation(up(idx))
            below = self.get_cell_occupation(down(idx))
            belowbelow = self.get_cell_occupation(down(down(idx)))
            reference_idx = idx if above != 2 or (below == 2 and belowbelow != 2) else up(idx)
        elif self.cells[idx] == 3:
            reference_idx = idx if self.get_cell_occupation(left(idx)) != 3 else left(idx)
        elif self.cells[idx] == 4:
            reference_idx = idx if self.get_cell_occupation(left(idx)) != 4 else left(idx)
            reference_idx = reference_idx if self.get_cell_occupation(up(reference_idx)) != 4 else up(reference_idx)
        assert 0 <= reference_idx <= 19
        assert self.cells[idx] == self.cells[reference_idx]
        return reference_idx

    def find_admissible_down_move(self, idx):
        assert (self.cells[idx] == 0)
        nx = []
        occ = self.get_cell_occupation(up(idx))
        if occ == 1:
            nx = [[0 if i == up(idx) else
                   1 if i == idx else
                   x for i, x in enumerate(self.cells)]]
        elif occ == 2:
            nx = [[0 if i == up(up(idx)) else
                   2 if i == idx else
                   x for i, x in enumerate(self.cells)]]
        elif occ == 3:
            if self.get_cell_occupation(right(idx)) == 0 and self.get_cell_occupation(up(right(idx))) == 3:
                nx = [[0 if i in [up(idx), right(up(idx))] else
                       3 if i in [idx, right(idx)] else
                       x for i, x in enumerate(self.cells)]]
        elif occ == 4:
            if self.get_cell_occupation(right(idx)) == 0 and self.get_cell_occupation(up(right(idx))) == 4:
                nx = [[0 if i in [up(up(idx)), up(up(right(idx)))] else
                       4 if i in [idx, right(idx)] else
                       x for i, x in enumerate(self.cells)]]
        return nx

    def find_admissible_up_move(self, idx):
        assert (self.cells[idx] == 0)
        nx = []
        occ = self.get_cell_occupation(down(idx))
        if occ == 1:
            nx = [[0 if i == down(idx) else
                   1 if i == idx else
                   x for i, x in enumerate(self.cells)]]
        elif occ == 2:
            nx = [[0 if i == down(down(idx)) else
                   2 if i == idx else
                   x for i, x in enumerate(self.cells)]]
        elif occ == 3:
            if self.get_cell_occupation(right(idx)) == 0 and self.get_cell_occupation(down(right(idx))) == 3:
                nx = [[0 if i in [down(idx), right(down(idx))] else
                       3 if i in [idx, right(idx)] else
                       x for i, x in enumerate(self.cells)]]
        elif occ == 4:
            if self.get_cell_occupation(right(idx)) == 0 and self.get_cell_occupation(down(right(idx))) == 4:
                nx = [[0 if i in [down(down(idx)), down(down(right(idx)))] else
                       4 if i in [idx, right(idx)] else
                       x for i, x in enumerate(self.cells)]]
        return nx

    def find_admissible_right_move(self, idx):
        assert (self.cells[idx] == 0)
        nx = []
        occ = self.get_cell_occupation(left(idx))
        if occ == 1:
            nx = [[0 if i == left(idx) else
                   1 if i == idx else
                   x for i, x in enumerate(self.cells)]]
        elif occ == 2:
            # the cell [left(idx)] that was proven to belong to a 2x1 piece must be top cell of that piece
            # which is the case if either the cell [idx-5] is not part of a 2x1 piece
            #                      or the two cells above form a separate 2x1 pice
            above2 = self.get_cell_occupation(up(left(idx)))
            aboveabove2 = self.get_cell_occupation(up(up(left(idx))))
            if self.get_cell_occupation(down(idx)) == 0 and \
                    self.get_cell_occupation(down(left(idx))) == 2 and \
                    (above2 != 2 or (above2 == 2 and aboveabove2 == 2)):
                nx = [[0 if i in [left(idx), left(down(idx))] else
                       2 if i in [idx, down(idx)] else
                       x for i, x in enumerate(self.cells)]]
        elif occ == 3:
            nx = [[0 if i == left(left(idx)) else
                   3 if i == idx else
                   x for i, x in enumerate(self.cells)]]
        elif occ == 4:
            if self.get_cell_occupation(down(idx)) == 0 and self.get_cell_occupation(down(left(idx))) == 4:
                nx = [[0 if i in [left(left(idx)), left(left(down(idx)))] else
                       4 if i in [idx, down(idx)] else
                       x for i, x in enumerate(self.cells)]]
        return nx

    def find_admissible_left_move(self, idx):
        assert (self.cells[idx] == 0)
        nx = []
        occ = self.get_cell_occupation(right(idx))
        if occ == 1:
            nx = [[0 if i == right(idx) else
                   1 if i == idx else
                   x for i, x in enumerate(self.cells)]]
        elif occ == 2:
            above2 = self.get_cell_occupation(up(right(idx)))
            aboveabove2 = self.get_cell_occupation(up(up(right(idx))))
            if self.get_cell_occupation(down(idx)) == 0 and \
                    self.get_cell_occupation((down(right(idx)))) == 2 and \
                    (above2 != 2 or (above2 == 2 and aboveabove2 == 2)):
                nx = [[0 if i in [right(idx), right(down(idx))] else
                       2 if i in [idx, down(idx)] else
                       x for i, x in enumerate(self.cells)]]
        elif occ == 3:
            nx = [[0 if i == right(right(idx)) else
                   3 if i == idx else
                   x for i, x in enumerate(self.cells)]]
        elif occ == 4:
            if self.get_cell_occupation(down(idx)) == 0 and self.get_cell_occupation(down(right(idx))) == 4:
                nx = [[0 if i in [right(right(idx)), right(right(down(idx)))] else
                       4 if i in [idx, down(idx)] else
                       x for i, x in enumerate(self.cells)]]
        return nx

    def find_admissible_moves(self):
        next_cellarrays = []
        for idx in range(20):
            if self.cells[idx] == 0:
                # we examine the empty cells and try to pull in pieces from all four directions.
                # the directions down, up, left, right describe the direction piece movement
                # from the empty cell we have to look in the opposite driection to identify the
                # piece that is appropriate as candidate.
                next_cellarrays.extend(self.find_admissible_down_move(idx))
                next_cellarrays.extend(self.find_admissible_up_move(idx))
                next_cellarrays.extend(self.find_admissible_left_move(idx))
                next_cellarrays.extend(self.find_admissible_right_move(idx))
        return next_cellarrays

    def print(self, no):
        print(f'--{no:03d}-- ', end='')
        for row in range(5):
            print(
                f'{self.cells[row * 4]:d}{self.cells[row * 4 + 1]:d}{self.cells[row * 4 + 2]:d}{self.cells[row * 4 + 3]:d}',
                end=' ')
        print('')

    def __str__(self):
        s = ''
        for row in range(5):
            for col in range(4):
                s = s + f'{self.cells[row * 4 + col ]}'
            s = s + ' '
        return s[:-1]

    # the left-top cell of a piece is defined to be the master cell of that piece
    def is_master_cell_of_piece(self, i: int) -> bool:
        rc = False
        if self.cells[i] == 1:
            rc = True
        elif self.cells[i] == 2:
            above2 = self.get_cell_occupation(up(i))
            aboveabove2 = self.get_cell_occupation(up(up(i)))
            return self.get_cell_occupation(down(i)) == 2 and (above2 != 2 or (above2 == 2 and aboveabove2 == 2))
        elif self.cells[i] == 3:
            return self.get_cell_occupation(right(i)) == 3
        elif self.cells[i] == 4:
            return self.get_cell_occupation(right(down(i))) == 4
        return rc


def bs_from_str(s: str):
    m = re.match(r'[-*]{2}\d{3}[-*]{2} ([0-4]{4}) ([0-4]{4}) ([0-4]{4}) ([0-4]{4}) ([0-4]{4})\n?', s)
    if not m:
        return None  # input string does not specify a boardstate
    cells = []
    for row in range(5):
        s_row = m.group(row + 1)
        for col in range(4):
            val = int(s_row[col])
            cells.append(val)
    bs = Boardstate(cells)
    return bs


initial_boardstate = Boardstate([2, 4, 4, 2,
                                 2, 4, 4, 2,
                                 2, 3, 3, 2,
                                 2, 1, 1, 2,
                                 1, 0, 0, 1])
