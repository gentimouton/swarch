# Python in Windows console: https://docs.python.org/2/faq/windows.html

import sys


# Windows- and POSIX-compatible getch (read 1 char from console without \n)
# from http://stackoverflow.com/a/21659588/856897
def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch

getch = _find_getch()

# arrow keys
char_map = {'\113':'L', '\110': 'U', '\120': 'D', '\115': 'R'}
while 1:
    char = getch()  # BEWARE: CTRL-C won't work anymore!
    if char == '\033':  # ESC key
        exit()
    if char in char_map:  # filter only the 5 chars
        cmd = char_map[char]
        print cmd  # Send to next filter. Equivalent to sys.stdout.write(X+'\n')
        sys.stdout.flush()  # don't buffer output
