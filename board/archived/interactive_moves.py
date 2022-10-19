from ..board import Board, BoardException
import re
import joelclui as j

def interactive_board():
    b=Board()
    print('Type a move as vertical, horizontal')
    while True:
        print(b)
        u_input=input('> ')
        try:
            buff=re.match(r'(\d*),\ ?(\d*)', u_input).groups()
        except:
            j.print('[red][ERR][/] Please type the right move format: vertical (int), horizontal (int) e.g. [blue]3, 3[/]')
            continue
        u_move=(int(buff[0]), int(buff[1]))
        try:
            b.move(u_move)
        except BoardException as e:
            j.print(f'[red]Invalid move: {e}[/]')


if __name__=='__main__':
    interactive_board()
