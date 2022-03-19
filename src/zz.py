from tic_tac_toe import *

b = init_board()
b[4] = 0
b[0] = 1
b[2] = 0
b[6] = 1
b[1] = 0
#b[5] = 1
#b[3] = 1
#b[1] = 0
#b[7] = 1

display_board(b)
print()
p = who_plays(b)
print("next player=", p)
print()

t = gametree(b)

for tt in t[1]:
    s = evaluate1(tt[0])
    display_board(tt[0])
    print("score=", s)
    print()
