from time import sleep
from pynput.keyboard import Key, Listener
from .Board import Board
import joelclui as j

class PlayableBoard(Board): #extends board with .play() method
    def __init__(
        self,
        board_state=None,
        size=3, #eg 3 -> 3x3, 2 -> 2x2
        safe_mode=True, #if enabled, it makes sure no errors when moving (more computation heavy)
        return_errors=True, #True: only returns errors, False: throws errors, interrupting program
        debug_mode=False #allows cheating devtools such as set_board_state
    ):
        super().__init__(board_state=board_state, size=size, safe_mode=safe_mode, return_errors=return_errors, debug_mode=debug_mode)

    def play(self):
        print('Press arrow keys to move or escape key to exit program')
        print(self) #intial board
        def on_press(key):
            mv={
                Key.up: (-1, 0),
                Key.down: (1, 0),
                Key.left: (0, -1),
                Key.right: (0, 1),
            }.get(key, None)
            if mv:
                self.move(
                    mv,
                    position='relative'
                )
                j.move_up(self.SIZE+1) #+1 because prints ---Board---
                print(self)
            if key==Key.esc:
                return False

        with Listener(on_press=on_press, suppress=True) as listener:  # type: ignore
            listener.join()

    def animated_solve(self, moves=None, speed=1):
        if moves is None:
            moves=self.solve_with_bfs()

        for move in moves:
            print(self)
            j.print('[blue]Solving...')
            sleep(1/speed)
            j.move_up(self.SIZE+2)
            self.move(move)
        print(self)
        j.print('[green]Solved!      ')

