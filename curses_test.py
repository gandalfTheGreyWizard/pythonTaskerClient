from curses import wrapper

def main(stdscr):
    stdscr.clear()
    for i in range(0, 11):
        v = i - 10
        stdscr.addstr(i, 0, '10 divided by {} '.format(v))
    stdscr.refresh()
    stdscr.getkey()
wrapper(main)
