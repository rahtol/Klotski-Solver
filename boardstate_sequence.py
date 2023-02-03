from boardstate import bs_from_str


def read_from_file(fn: str):
    boardstate_sequence = []
    with open(fn, 'r') as f:
        for line in f:
            bs = bs_from_str(line)
            if bs is not None:
                boardstate_sequence.append(bs)
    return boardstate_sequence


def normalize(sequence_in):
    pass
