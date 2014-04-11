"""
input: stdin
output: 'U', 'L', 'D', 'R' when the direction changed, and ''/EOF when stopped

Run this in command line:
python inputs.py | python simulation.py | python displaypygame.py 

Push arrow keys to change direction, or ESC key to leave the game.
Only the console listens for keyboard inputs, not the Pygame window. 

To replace the Pygame display by the console:
python inputs.py | python simulation.py | python displayconsole.py

Need help running Python scripts in the Windows console? 
Check https://docs.python.org/2/faq/windows.html
"""
import sys


# Windows- and POSIX-compatible getch (read 1 char from console without \n)
# From http://stackoverflow.com/a/21659588/856897
# Check also http://home.wlu.edu/~levys/software/kbhit.py
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
    if char in char_map:  # only send the arrows
        cmd = char_map[char]
        print cmd  # Send to next filter. Equivalent to sys.stdout.write(X+'\n')
        sys.stdout.flush()  # don't buffer output
