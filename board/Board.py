from typing import List, Tuple
import numpy as np
import random
import joelclui as j
from joeldata import Queue

class BoardException(Exception):
    def __init__(self, message: str):
        self.message=f'BoardError: {message}'
        super().__init__(self.message)
    

class Board:
    def __init__(
        self,
        board_state=None, #user sets board_state manually (debug_mode must be True)
        size=3, #eg 3 -> 3x3, 2 -> 2x2
        safe_mode=True, #if enabled, it makes sure no errors when moving (more computation heavy)
        return_errors=False, #False: throws errors, interrupting program. True: only returns errors
        debug_mode=False #allows cheating devtools such as set_board_state
    ):
        self.SIZE=size
        self.SAFE_MODE=safe_mode 
        self.RETURN_ERRORS=return_errors
        self.DEBUG_MODE=debug_mode
        if board_state is None:
            self.board=self.goal_board().board
        else: #user defined board_state
            self.board=np.array(board_state)


    def is_goal(self) -> bool:
        return self==self.goal_board()

    def get_hole(self) -> Tuple[int, int]:
        loc=np.where(self.board==0)
        return loc[0][0], loc[1][0] #ret tuple

    def get_legal_moves(self, position='absolute'):
        is_abs=position=='absolute'
            
        v, h=self.get_hole() #vertical first, horiz second
        moves=[] #array of tuples of locs

        if v>0:
            moves.append((v-1, h) if is_abs else (0, -1))
        if v<self.SIZE-1:
            moves.append((v+1, h) if is_abs else (0, 1))
        if h>0:
            moves.append((v, h-1) if is_abs else (-1, 0))
        if h<self.SIZE-1:
            moves.append((v, h+1) if is_abs else (1, 0))

        return moves

    def move(self, move, position='absolute') -> None | str: #pos: 'absolute' | 'relative'
        is_abs=position=='absolute'
        hole=self.get_hole()
        diff=(move[0]-hole[0], move[1]-hole[1]) if is_abs else move #x_diff, y_diff

        if self.SAFE_MODE:
            if diff[0]!=0 and diff[1]!=0:
                return self._err(f'Cannot move both y and x axes at same time: moving from {hole} to {move} (difference of {diff})')
            if diff[0]==0 and diff[1]==0:
                return self._err('No move specified')
            #check if move is legal
            legal_moves=self.get_legal_moves()
            if is_abs and move not in legal_moves:
                return self._err(f'Cannot move to {move}')
            if not is_abs:
                going_to=hole[0]+diff[0], hole[1]+diff[1]
                if going_to not in self.get_legal_moves():
                    return self._err(f'Cannot move {move} (relative moving) to {going_to}')

        dest=(None, None)
        # Figure out where to swap
        if diff[0]!=0: #x_diff ∴ swap horizontally
            dest=(hole[0]+diff[0], hole[1]) #tuple of destination location to swap with
        elif diff[1]!=0: #y_diff ∴ swap vertically
            dest=(hole[0], hole[1]+diff[1])
        #Swap
        self.board[hole]=self.board[dest] #mv swap loc to HOLE
        self.board[dest]=0 #mv hole to swap loc

    def make_random_move(self) -> None:
        mv=random.choice(self.get_legal_moves())
        self.move(mv)

    def shuffle(self, depth=50) -> None:
        for _ in range(depth): # Do {depth} random moves
            self.make_random_move()
        while self.is_goal(): # Keep moving until not in goal state
            self.make_random_move()
    scramble=shuffle #alias

    def goal_board(self) -> 'Board':
        board=np.arange(1, self.SIZE**2+1, 1).reshape((self.SIZE, self.SIZE))
        # 0 represents the hole/empty mark
        board[-1, -1]=0
        return Board(board)

    def __str__(self):
        out=str(self.board)#.replace('0', ' ') #hole is blank space
        if self.is_goal(): # 🌈 if solved
            out=j.format('[rainbow]'+str(out))
        return '---Board---\n'+out

    def hash(self) -> str: #hashed boards stored in a visitedSet
        return str(self.board)


    def __eq__(self, other_board) -> bool:
        if type(other_board)==Board or type(other_board).__name__=='PlayableBoard':
            return np.array_equal(self.board, other_board.board)
        else:
            return np.array_equal(self.board, other_board)

    def solve_with_bfs(self, target=None) -> List[Tuple[int, int]]: # -> solution
        if target is None: #no args means goal_board
            target=self.goal_board()

        visitedSet=set() #set of visited boards

        frontier=Queue() #q of els with board and path
            # : { board: Board; path: string[] }
        frontier.enqueue({ #starting point in frontier
            "board": self.clone(),
            "path": []
        })

        while len(frontier)!=0: #not empty
            #list of move tuples
            curr=frontier.dequeue()
            visitedSet.add(curr['board'].hash())

            if curr['board']==target:
                return curr['path']

            # Add every legal move to frontier
            for mv in curr['board'].get_legal_moves():
                new_board=curr['board'].clone() #go from current situation
                new_board.move(mv)
                if new_board.hash() in visitedSet: #skip over already visited boards
                    continue
                new_state={
                    "board": new_board,
                    "path": curr['path']+[mv]
                }
                frontier.enqueue(new_state)
        
        self._err('Target not found')
        return []

    def solve_with_dfs(self):
        assert 'DFS has not been implemented yet :('


    # Debug mode
    def set_board_state(self, new_board):
        if not self.DEBUG_MODE:
            return self._err('Cannot set_board_state unless debug_mode is True')
        self.board=new_board

    def _err(self, msg):
        if self.RETURN_ERRORS:
            return msg
        else:
            raise BoardException(msg)

    def clone(self) -> 'Board': #makes a new board
        return Board(board_state=self.board, debug_mode=True)
