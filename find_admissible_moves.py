# boardstate is represented by list of 20 integers where
#   idx = row * 4 * col, i.e. col = idx %4, row = idx // 4 with rages raw 0..3, col 0..4
#   bord[idx] = 0, 1, 2 4 with 0=empy cell, 1,2,4=cell occupied by piece of respectiv size

initial_boardstate = [2, 4, 4, 2,
                      2, 4, 4, 2,
                      2, 1, 1, 2,
                      2, 1, 1, 2,
                      1, 0, 0, 1]


def get_cell_occupation(boardstate, idx):
    if idx < 0 or idx > 19:
        return -1
    else:
        return boardstate[idx]


def find_admissible_down_move(boardstate, idx):
    assert (boardstate[idx] == 0)
    occ = get_cell_occupation(boardstate, idx - 4)
    if occ == -1 or occ == 0:
        return []
    elif occ == 1:
        nx = boardstate[:]
        nx[idx-4] = 0
        nx[idx] = 1
        return [nx]
    elif occ == 2:
        nx = boardstate[:]
        nx[idx-8] = 0
        nx[idx] = 2
        return [nx]
    elif occ == 4:
        if get_cell_occupation(boardstate, idx+1) == 0 and get_cell_occupation(boardstate, idx - 3) == 4:
            nx = boardstate[:]
            nx[idx - 8] = 0
            nx[idx - 7] = 0
            nx[idx] = 4
            nx[idx + 1] = 4
            return [nx]
        else:
            return []


def find_admissible_up_move(boardstate, idx):
    assert (boardstate[idx] == 0)
    occ = get_cell_occupation(boardstate, idx + 4)
    if occ == -1 or occ == 0:
        return []
    elif occ == 1:
        nx = boardstate[:]
        nx[idx + 4] = 0
        nx[idx] = 1
        return [nx]
    elif occ == 2:
        nx = boardstate[:]
        nx[idx + 8] = 0
        nx[idx] = 2
        return [nx]
    elif occ == 4:
        if get_cell_occupation(boardstate, idx + 1) == 0 and get_cell_occupation(boardstate, idx + 5) == 4:
            nx = boardstate[:]
            nx[idx + 8] = 0
            nx[idx + 9] = 0
            nx[idx] = 4
            nx[idx + 1] = 4
            return [nx]
        else:
            return []


def find_admissible_right_move(boardstate, idx):
    assert (boardstate[idx] == 0)
    nx = []
    occ = get_cell_occupation(boardstate, idx - 1)
    if occ == -1 or occ == 0:
        pass
    elif occ == 1:
        nx = [[0 if i == idx-1 else 1 if i == idx else x for i, x in enumerate(boardstate)]]
    elif occ == 2:
        # the cell [idx-1] that was proven to belong to a 2x1 pieced must be top cell of that piece
        # which is the case if either the cell [idx-5] is not part of a 2x1 piece
        #                      or the two cells above form a separate 2x1 pice
        above2 = get_cell_occupation(boardstate, idx - 5)
        aboveabove2 = get_cell_occupation(boardstate, idx - 9)
        if get_cell_occupation(boardstate, idx + 4) == 0 and (above2 != 2 or (above2 == 2 and aboveabove2 == 2)):
            nx = [[0 if i in [idx-1, idx+3] else 2 if i in [idx, idx+4] else x for i, x in enumerate(boardstate)]]
    elif occ == 4:
        if get_cell_occupation(boardstate, idx + 4) == 0 and get_cell_occupation(boardstate, idx + 3) == 4:
            nx = [[0 if i in [idx-2, idx+2] else 4 if i in [idx, idx+4] else x for i, x in enumerate(boardstate)]]
    return nx


def find_admissible_left_move(boardstate, idx):
    assert (boardstate[idx] == 0)
    occ = get_cell_occupation(boardstate, idx + 1)
    if occ == -1 or occ == 0:
        return []
    elif occ == 1:
        nx = boardstate[:]
        nx[idx + 1] = 0
        nx[idx] = 1
        return [nx]
    elif occ == 2:
        above2 = get_cell_occupation(boardstate, idx - 3)
        aboveabove2 = get_cell_occupation(boardstate, idx - 7)
        if get_cell_occupation(boardstate, idx + 4) == 0 and (above2 != 2 or (above2 == 2 and aboveabove2 == 2)):
            nx = boardstate[:]
            nx[idx + 1] = 0
            nx[idx + 5] = 0
            nx[idx] = 2
            nx[idx + 4] = 2
            return [nx]
        else:
            return []
    elif occ == 4:
        if get_cell_occupation(boardstate, idx + 4) == 0 and get_cell_occupation(boardstate, idx + 5) == 4:
            nx = boardstate[:]
            nx[idx + 2] = 0
            nx[idx + 6] = 0
            nx[idx] = 4
            nx[idx + 4] = 4
            return [nx]
        else:
            return []


def find_admissible_moves(boardstate):
    next_boardstates = []
    for idx in range(20):
        if boardstate[idx] == 0:
            # we examine the empty cells and try to pull in pieces from all four directions.
            # the directions down, up, left, right describe the direction piece movement
            # from the empty cell we have to look in the opposite driection to identify the
            # piece that is appropriate as candidate.
            next_boardstates.extend(find_admissible_down_move(boardstate, idx))
            next_boardstates.extend(find_admissible_up_move(boardstate, idx))
            next_boardstates.extend(find_admissible_left_move(boardstate, idx))
            next_boardstates.extend(find_admissible_right_move(boardstate, idx))
    return next_boardstates


def print_boardstate(boardstate):
    print(f'----')
    for row in range(5):
        print(f'{boardstate[row*4]:d}{boardstate[row*4+1]:d}{boardstate[row*4+2]:d}{boardstate[row*4+3]:d}')


if __name__ == '__main__':
    nx_states = find_admissible_moves(initial_boardstate)
    for m in nx_states:
        print_boardstate(m)


