from boardstate_sequence import read_from_file
from boardstate import Boardstate

youtube_sloution = read_from_file('youtube-solution.txt')

for i in range(len(youtube_sloution)-1):
    nx = youtube_sloution[i].find_admissible_moves()
    nx_boardstates = [Boardstate(cellstate) for cellstate in nx]
    if youtube_sloution[i+1] not in nx_boardstates:
        print( f'{i}')
print('finished')

