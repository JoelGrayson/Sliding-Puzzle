# run as python3 -i code.py
from ..board import Board
import numpy as np

b=Board(debug_mode=True)
b.set_board_state(np.array([
    [1, 2, 0],
    [4, 5, 3],
    [7, 8, 6]
]))
print(b)
print(b.get_legal_moves())
