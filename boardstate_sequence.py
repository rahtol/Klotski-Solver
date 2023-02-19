from boardstate import bs_from_str, Boardstate, left, right
from boardmove import detect_move, apply_move


def read_from_file(fn: str):
    boardstate_sequence = []
    with open(fn, 'r') as f:
        for line in f:
            bs = bs_from_str(line)
            if bs is not None:
                boardstate_sequence.append(bs)
    return boardstate_sequence


def write_to_file(boardstate_sequence: [Boardstate], fn: str):
    with open(fn, 'w') as f:
        i: int = 0
        for bs in boardstate_sequence:
            f.write(f'--{i:03d}-- {bs}\n')
            i = i + 1


def normalize(boardstate_sequence_in: [Boardstate]) -> [Boardstate]:
    boardstate_sequence_out: [Boardstate] = boardstate_sequence_in[:1]
    for i in range(1, len(boardstate_sequence_in)):
        move = detect_move(boardstate_sequence_in[i - 1], boardstate_sequence_in[i])
        if abs(move.dx) > 1: # two steps in left/right direction
            assert abs(move.dx) == 2
            assert move.dy == 0
            move.dx = 1 if move.dx == 2 else -1
            bs = apply_move(boardstate_sequence_in[i - 1], move)
            boardstate_sequence_out.append(bs)
            move2 = detect_move(bs, boardstate_sequence_in[i])
            bs2 = apply_move(bs, move2)
            assert bs2 == boardstate_sequence_in[i]
            boardstate_sequence_out.append(bs2)
        elif abs(move.dy) > 1:  # two steps in up/down direction
            assert abs(move.dy) == 2
            assert move.dx == 0
            move.dy = 1 if move.dy == 2 else -1
            bs = apply_move(boardstate_sequence_in[i - 1], move)
            boardstate_sequence_out.append(bs)
            move2 = detect_move(bs, boardstate_sequence_in[i])
            bs2 = apply_move(bs, move2)
            assert bs2 == boardstate_sequence_in[i]
            boardstate_sequence_out.append(bs2)
        elif abs(move.dx) > 0 and abs(move.dy) > 0:  # two steps, exactly one per axis
            assert abs(move.dx) == 1
            assert abs(move.dy) == 1
            assert boardstate_sequence_in[i - 1].cells[move.piece_idx] == 1
            # figure out which direction to do first
            dx_first = boardstate_sequence_in[i-1].get_cell_occupation(left(move.piece_idx)) == 0 or \
                       boardstate_sequence_in[i-1].get_cell_occupation(right(move.piece_idx)) == 0
            if dx_first:
                move.dy = 0  # delay the up/down movement to move2
            else:
                move.dx = 0  # delay the left/right movement to move2
            bs = apply_move(boardstate_sequence_in[i - 1], move)
            boardstate_sequence_out.append(bs)
            move2 = detect_move(bs, boardstate_sequence_in[i])
            bs2 = apply_move(bs, move2)
            assert bs2 == boardstate_sequence_in[i]
            boardstate_sequence_out.append(bs2)
        else:  # single step in one direction only, nothing to normalize here
            assert (abs(move.dx) == 1) != (abs(move.dy) == 1)
            bs = apply_move(boardstate_sequence_in[i - 1], move)
            boardstate_sequence_out.append(bs)
            assert bs == boardstate_sequence_in[i]
    return boardstate_sequence_out


if __name__ == '__main__':
    bs0 = read_from_file('youtube-solution.txt')
    bs1 = normalize(bs0)
    write_to_file(bs1, 'youtube-solution.normalized.txt')