from board import PlayableBoard

b=PlayableBoard(size=3)
print(b)
b.shuffle(depth=30)
print(b)
moves=b.solve_with_bfs()
print(f'Solve in {len(moves)} moves:', moves)
b.animated_solve(speed=5, moves=moves)
