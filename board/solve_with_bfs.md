```ts
fn solve_with_bfs(start, target)
    frontier=[{ //Queue
        board: start,
        path: []// moves to get to board
    }]
    while frontier is not empty
        curr=frontier.dequeue()
        if curr.board==target
            return curr.path

        for every legal move from curr.board
            new_board=curr.board.clone()
            new_board.move_to(move)

            frontier.enqueue({
                board: new_board,
                path: curr.board.paths+[move]
            })
            frontier.enqueue()
```