from board import PlayableBoard

b=PlayableBoard()
b.play()
print('Solution of moves:', b.solve_with_bfs())
b.animated_solve(speed=2)
