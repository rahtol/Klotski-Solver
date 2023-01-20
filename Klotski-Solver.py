import collections

import boardstate


def solve():
    count = 0
    l = collections.deque([boardstate.initial_boardstate])
    marked_boardstates = set()
    while l:
        current_boardstate = l.popleft()
        if current_boardstate.is_final():
            len_solution = 0
            p = current_boardstate
            while p is not None:
                len_solution = len_solution + 1
                p.print(len_solution)
                p = p.pred
            print(f'Solution of length {len_solution} found.')
            return
        admissible_moves = current_boardstate.find_admissible_moves()
        for nx_cells in admissible_moves:
            nx_boardstate = boardstate.Boardstate(nx_cells)
            if not (nx_boardstate in marked_boardstates):
                marked_boardstates.add(nx_boardstate)
                nx_boardstate.pred = current_boardstate
                l.append(nx_boardstate)
            else:
                count = count + 1
    print(f'#configurations={len(marked_boardstates)},  count={count}')


solve()
