#!/usr/bin/env python

import curses
import math
import os
import re
import threading

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

class Trigger:

    def __init__(self, colors=None, height=None, width=None):
        self.elapsed = 0
        self.running = False
        self.display_enabled = True
        self.highlight = False

        self.colors = colors

        if height is None:
            height = 1
        self.height = height

        if width is None:
            width = 78
        self.width = width

    def add_time(self, amount):
        self.elapsed += self.parse_time(amount)

    def build(self):
        self.window = curses.newwin(self.height, self.width, 0, 0)

    def disable_display(self):
        self.display_enabled = False

    def enable_display(self):
        self.display_enabled = True

    def format_seconds(self, elapsed):
        hours = math.floor(elapsed / 3600)
        remainder = elapsed % 3600
        minutes = math.floor(remainder / 60)
        seconds = remainder % 60

        return "%.2d:%.2d:%.2d" % (hours, minutes, seconds)

    def get_elapsed(self):
        return self.elapsed

    def move(self, y, x):
        self.window.mvwin(y, x)
        self.refresh()

    def parse_time(self, amount):
        total = 0
        terms = re.findall('[\d]+[h|m|s]+', amount)
        for term in terms:
            if term[-1] == 'h':
                total += int(term[:-1]) * 3600
            elif term[-1] == 'm':
                total += int(term[:-1]) * 60
            elif term[-1] == 's':
                total += int(term[:-1])

        return total

    def redraw(self):
        self.window.touchwin()

    def refresh(self):
        if self.display_enabled:
            self.window.refresh()

    def render(self):
        time = self.format_seconds(self.get_elapsed())
        if self.running:
            time += '           '
        else:
            time += ' [Paused]  '

        self.window.erase()

        if self.colors:
            if self.highlight:
                color_time = self.colors['hgreen']
                color_title = self.colors['hblue']
            else:
                color_time = self.colors['green']
                color_title = self.colors['blue']
            self.window.addstr(0, 0, time, color_time)
            self.window.addstr(0, len(time), self.title, color_title)
        else:
            self.window.addstr(0, 0, time)
            self.window.addstr(0, len(time), self.title)

        self.refresh()

    def reset(self):
        self.elapsed = 0

    def set_highlight(self, highlight):
        self.highlight = highlight

    def set_title(self, title):
        self.title = title

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def subtract_time(self, amount):
        self.elapsed -= self.parse_time(amount)
        if self.elapsed < 0:
            self.elapsed = 0

    def tick(self):
        if self.running:
            self.add_time('1s')

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()


def print_help(help_window):
    help_window.addstr(0, 0, 'Help')
    help_window.addstr(1, 0, '----')
    help_window.addstr(3, 0, 'Commands')

    description = 'On the main screen, type ":" to bring up the command window.'
    help_window.addstr(4, 0, description)

    commands = [
        'n [title]      - Creates and starts a new timer.',
        'e[n][title]    - Edits the title of the nth timer.',
        'p[n]           - Pauses/starts the nth timer.',
        'r[n]           - Resets the nth timer.',
        'a[n][xh|ym|zs] - Adds time to the nth timer.',
        's[n][xh|ym|zs] - Subtracts time from the nth timer.',
        'q              - Quits the program.',
        'h              - Shows this help screen.'
    ]
    for index, command in enumerate(commands):
        help_window.addstr(index + 6, 0, command)

    help_window.addstr(15, 0, 'To return to the main screen, type "q".')
    help_window.touchwin()
    help_window.refresh()

@set_interval(1)
def update_trigger(trigger):
    trigger.tick()
    trigger.render()


def capture_command(command_window, description):
    curses.echo()

    command_window.clear()
    command_window.refresh()
    command_window.addstr(0, 0, description)

    command = command_window.getstr(0, len(description), 28).decode('utf-8')
    curses.noecho()
    command_window.clear()
    command_window.refresh()

    return command

def main():
    # xterm-color can't handle curs_set(0)
    if os.environ['TERM'] == 'xterm-color':
        os.environ['TERM'] = 'xterm'


    screen = curses.initscr()
    # TODO: FIX HIGHLIGHTING FOR NO COLORS
    if not curses.has_colors():
        colors = None
    else:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLUE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        colors = {
            'blue': curses.color_pair(1),
            'hblue': curses.color_pair(1) | curses.A_REVERSE,
            'green': curses.color_pair(2),
            'hgreen': curses.color_pair(2) | curses.A_REVERSE
        }

    curses.noecho()
    screen.keypad(1)

    curses.curs_set(0)

    height, width = screen.getmaxyx()

    triggers = []

    command_window = curses.newwin(1, width - 3, height - 1, 0)
    help_window = curses.newwin(height - 2, width - 2, 1, 1)

    keep_alive = True
    in_help_mode = False

    position = 0

    while keep_alive:
        char = screen.getch()

        # TODO: Fix this
        #if in_help_mode:
        #    if char != ord('q'):
        #        continue
        #    else:
        #        help_window.clear()
        #        help_window.refresh()
        #        for trigger in triggers:
        #            trigger.enable_display()
        #            trigger.redraw()
        #        in_help_mode = False

        if char == curses.KEY_DOWN or char == ord('j'):
            if position < len(triggers) - 1:
                position += 1
        elif char == curses.KEY_UP or char == ord('k'):
            if position > 0:
                position -= 1

        # New
        elif char == ord('n'):
            title = capture_command(command_window, '[NEW] Enter the title: ')

            num_triggers = len(triggers)

            trigger = Trigger(colors, 1, width - 2)
            trigger.build()
            trigger.move(num_triggers, 0)

            trigger.set_title(title)
            trigger.start()
            trigger.render()
            update_trigger(trigger)

            triggers.append(trigger)

        # Edit
        elif char == ord('e') and len(triggers):
            title = capture_command(command_window, '[EDIT] Enter the title: ')
            triggers[position].set_title(title)

        # Add
        elif char == ord('a') and len(triggers):
            time = capture_command(command_window, '[ADD] Enter the amount of time: ')
            triggers[position].add_time(time)

        # Subtract
        elif char == ord('s') and len(triggers):
            time = capture_command(command_window, '[SUBTRACT] Enter the amount of time: ')
            triggers[position].subtract_time(time)

        # Pause
        elif char == ord('p') and len(triggers):
            triggers[position].toggle()

        # Reset
        elif char == ord('r') and len(triggers):
            command = capture_command(command_window, '[RESET] Are you sure? [y/N]: ')
            if command == 'y':
                triggers[position].reset()

        # Quit
        elif char == ord('q'):
            command = capture_command(command_window, '[QUIT] Are you sure? [y/N]: ')
            keep_alive = ( command != 'y' )


        for index, trigger in enumerate(triggers):
            if index == position:
                triggers[index].set_highlight(True)
            else:
                triggers[index].set_highlight(False)
            triggers[index].render()

        # TODO: Fix this
        #if command == 'h':
        #    for trigger in triggers:
        #        trigger.disable_display()
        #    print_help(help_window)
        #    in_help_mode = True

    curses.endwin()


if __name__ == '__main__':
    main()
