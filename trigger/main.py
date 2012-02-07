#!/usr/bin/env python

import curses
import math
import threading
import time

def set_interval(interval):
    def outer_wrap(function):
        def wrap(*args, **kwargs):
            stop = threading.Event()
            def inner_wrap():
                while not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap

class Timer:

    def __init__(self):
        self.start_time = time.time()
        self.elapsed = 0
        self.on = False

    def is_on(self):
        return self.on

    def reset(self):
        self.start_time = time.time()
        self.elapsed = 0

    def start(self):
        if not self.on:
            self.start_time = time.time()
            self.on = True

    def stop(self):
        if self.on:
            self.elapsed += time.time() - self.start_time
            self.on = False

    def toggle(self):
        if self.on:
            self.stop()
        else:
            self.start()

    def get_elapsed(self):
        if self.on:
            elapsed = self.elapsed + (time.time() - self.start_time)
            return elapsed
        else:
            return self.elapsed

    def render(self, elapsed):
        hours = math.floor(elapsed / 3600)
        remainder = elapsed % 3600
        minutes = math.floor(remainder / 60)
        seconds = remainder % 60

        return "%.2d:%.2d:%.2d" % (hours, minutes, seconds)


class Window:

    def __init__(self):
        self.width = 25
        self.height = 6
        self.no_update = False

    def add_padding(self, string, min_length):
        string_length = len(string)
        final_length = max(string_length, min_length - 2) + 2

        if (final_length - string_length) % 2:
            final_length += 1

        padding_length = int((final_length - string_length) / 2)
        padding = ' ' * padding_length

        return padding + string + padding

    def print_string(self, string):
        self.window.addstr(4, 1, string)
        if not self.no_update:
            self.window.refresh()

    def redraw(self):
        self.window.touchwin()

    def set_title(self, title):
        title = self.add_padding(title, self.width - 3)
        self.window.addstr(1, 1, title)

        underline = '-' * (self.width - 2)
        self.window.addstr(2, 1, underline)

        self.window.refresh()

    def set_no_update(self, val):
        self.no_update = val

    def build(self, identifier):
        row = (self.height * identifier) + 1

        self.window = curses.newwin(self.height, self.width, row, 1)
        self.window.border(0)

        self.window.refresh()


def create_help(height, width):
    help_window = curses.newwin(height - 2, width - 2, 1, 1)
    help_window.addstr(0, 0, 'Help')
    help_window.addstr(1, 0, '----')
    help_window.addstr(3, 0, 'Commands')

    description = 'On the main screen, type ":" to bring up the command window.'
    help_window.addstr(4, 0, description)

    commands = [
        'n [title]   - Creates and starts a new timer.',
        'e[n][title] - Edits the title of the nth timer.',
        'p[n]        - Pauses/starts the nth timer.',
        'r[n]        - Resets the nth timer.',
        'q           - Quits the program.',
        'h           - Shows this help screen.'
    ]
    for index, command in enumerate(commands):
        help_window.addstr(index + 6, 0, command)

    help_window.addstr(13, 0, 'To return to the main screen, type "q".')

    return help_window

@set_interval(1)
def update_window(window, timer):
    string = timer.render(timer.get_elapsed())
    if timer.is_on():
        suffix = '         '
    else:
        suffix = ' [Paused]'
    window.print_string(string + suffix)


def main():
    """Primary entry point."""
    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)

    screen.border(0)
    height, width = screen.getmaxyx()
    screen.refresh()

    timers = []
    windows = []

    command = None
    command_window = curses.newwin(1, width - 3, height - 2, 1)

    in_help_mode = False

    while command != 'q':
        char = screen.getch()
        if in_help_mode:
            if char != ord('q'):
                continue
            else:
                help_window.clear()
                help_window.refresh()
                for window in windows:
                    window.set_no_update(False)
                    window.redraw()
                in_help_mode = False

        if char != ord(':'):
            continue

        curses.echo()

        command_window.clear()
        command_window.refresh()
        command_window.addstr(0, 0, ':')

        command = command_window.getstr(0, 1, 13).decode('utf-8')
        curses.noecho()
        command_window.clear()
        command_window.refresh()

        command, params = command[0:1], command[1:].strip()
        if command == 'n':
            timer = Timer()
            window = Window()
            list_size = len(windows)
            window.build(list_size)
            params = '[' + str(list_size + 1) + '] ' + params
            window.set_title(params)
            timer.start()
            update_window(window, timer)

            timers.append(timer)
            windows.append(window)

        elif command == 'e':
            try:
                params, title = params[0:1], params[1:]
                windows[int(params) - 1].set_title('[' + params + ']' + title)
            except:
                command_window.addstr('Edit: invalid argument.')
                command_window.refresh()

        elif command == 'h':
            for window in windows:
                window.set_no_update(True)
            help_window = create_help(height, width)
            help_window.refresh()
            in_help_mode = True

        elif command == 'p':
            try:
                timers[int(params) - 1].toggle()
            except:
                command_window.addstr('Pause: invalid argument.')
                command_window.refresh()

        elif command == 'r':
            try:
                timers[int(params) - 1].reset()
            except:
                command_window.addstr('Reset: invalid argument.')
                command_window.refresh()


    curses.endwin()

#    print("""Trigger v.0.1
#
#Usage is as follows:
#
#n [title]   - Creates and starts a new timer with the supplied title.
#p[n] - Pauses/starts the nth timer.
#r[n] - Resets the nth timer.
#
#    """)

# Run the script.
if __name__ == '__main__':
    main()
