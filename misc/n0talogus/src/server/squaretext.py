from random import choice
from string import ascii_lowercase, ascii_uppercase

flag = "COMPFEST14{s33_7H3_l0g!!!!_459b516942}"


with open("res.txt", "w+") as target:
    for i in range(len(flag)):
        rand_string = "".join(choice(ascii_lowercase) for j in range(len(flag)))
        flag_piece = flag[i] + rand_string
        print(flag_piece, file=target)
        