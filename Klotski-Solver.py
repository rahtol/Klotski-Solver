import collections
import boardstate
import re


def bs_from_str(s: str):
    m = re.match(r'[-*]{2}\d{3}[-*]{2} ([0-4]{4}) ([0-4]{4}) ([0-4]{4}) ([0-4]{4}) ([0-4]{4})', s)
    assert m
    cells = []
    for row in range(5):
        s_row = m.group(row + 1)
        for col in range(4):
            val = int(s_row[col])
            cells.append(val)
    bs = boardstate.Boardstate(cells)
    return bs


def path_to(bs):
    p = bs
    path = []
    while p is not None:
        path.append(p)
        p = p.pred
    return list(reversed(path))


def solve():
    count = 0
    solutions = []
    _list = collections.deque([boardstate.initial_boardstate])
    marked_boardstates = set([boardstate.initial_boardstate])
    while _list:
        current_boardstate = _list.popleft()
        if current_boardstate.is_final():
            solutions.append(path_to(current_boardstate))
        admissible_moves = current_boardstate.find_admissible_moves()
        for nx_cells in admissible_moves:
            nx_boardstate = boardstate.Boardstate(nx_cells)
            if not (nx_boardstate in marked_boardstates):
                marked_boardstates.add(nx_boardstate)
                nx_boardstate.pred = current_boardstate
                _list.append(nx_boardstate)
            else:
                count = count + 1
    print(f'#configurations={len(marked_boardstates)},  #solutions={len(solutions)}')
    return marked_boardstates, solutions


def test1(marked_states):
    #    bs = bs_from_str('--007-- 2442 2442 0233 1212 1012')
    bs = bs_from_str('**047** 1112 2442 2442 2002 2133')
    t = bs in marked_states
    print(t)
    for x in marked_states:
        if x == bs:
            p = path_to(x)
            for i, bs2 in enumerate(p):
                bs2.print(i)


ms, sol = solve()
test1(ms)
