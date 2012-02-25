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

    def __init__(self, height=None, width=None):
        self.elapsed = 0
        self.running = False
        self.display_enabled = True

        if height is None:
            height = 6
        self.height = height

        if width is None:
            width = 35
        self.width = width

    def add_padding(self, string, min_length):
        string_length = len(string)
        final_length = max(string_length, min_length - 2) + 2

        if (final_length - string_length) % 2:
            final_length += 1

        padding_length = int((final_length - string_length) / 2)
        padding = ' ' * padding_length

        return padding + string + padding

    def add_time(self, amount):
        self.elapsed += self.parse_time(amount)

    def build(self):
        self.window = curses.newwin(self.height, self.width, 1, 1)
        self.window.border(0)

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

    def render_time(self):
        display = self.format_seconds(self.get_elapsed())
        if self.running:
            display += '         '
        else:
            display += ' [Paused]'

        self.window.addstr(4, 1, display)
        self.refresh()

    def reset(self):
        self.elapsed = 0

    def set_title(self, title):
        title = self.add_padding(title, self.width - 3)
        self.window.addstr(1, 1, title)

        underline = '-' * (self.width - 2)
        self.window.addstr(2, 1, underline)

        self.refresh()

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
    trigger.render_time()

def run(screen):
    curses.curs_set(0)

    screen.border(0)
    height, width = screen.getmaxyx()
    screen.refresh()

    triggers = []

    command_window = curses.newwin(1, width - 3, height - 2, 1)
    help_window = curses.newwin(height - 2, width - 2, 1, 1)

    command = None
    in_help_mode = False

    while command != 'q':
        char = screen.getch()

        if in_help_mode:
            if char != ord('q'):
                continue
            else:
                help_window.clear()
                help_window.refresh()
                for trigger in triggers:
                    trigger.enable_display()
                    trigger.redraw()
                in_help_mode = False

        if char != ord(':'):
            continue

        curses.echo()

        command_window.clear()
        command_window.refresh()
        command_window.addstr(0, 0, ':')

        command = command_window.getstr(0, 1, 28).decode('utf-8')
        curses.noecho()
        command_window.clear()
        command_window.refresh()

        command, params = command[0:1], command[1:].strip()
        if command == 'n':
            num_triggers = len(triggers)

            trigger = Trigger()
            trigger.build()
            y = (trigger.height * num_triggers) + 1
            trigger.move(y, 1)

            title = '[' + str(num_triggers + 1) + '] ' + params
            trigger.set_title(title)
            trigger.start()
            update_trigger(trigger)

            triggers.append(trigger)

        elif command == 'e':
            try:
                params, title = params[0:1], params[1:]
                triggers[int(params) - 1].set_title('[' + params + ']' + title)
            except:
                command_window.addstr('Edit: invalid argument.')
                command_window.refresh()

        elif command == 'a':
            try:
                params, time = params[0:1], params[1:].strip()
                triggers[int(params) - 1].add_time(time)
            except:
                command_window.addstr('Add: invalid argument.')
                command_window.refresh()

        elif command == 's':
            try:
                params, time = params[0:1], params[1:].strip()
                triggers[int(params) - 1].subtract_time(time)
            except:
                command_window.addstr('Subtract: invalid argument.')
                command_window.refresh()

        elif command == 'h':
            for trigger in triggers:
                trigger.disable_display()
            print_help(help_window)
            in_help_mode = True

        elif command == 'p':
            try:
                triggers[int(params) - 1].toggle()
            except:
                command_window.addstr('Pause: invalid argument.')
                command_window.refresh()

        elif command == 'r':
            try:
                triggers[int(params) - 1].reset()
            except:
                command_window.addstr('Reset: invalid argument.')
                command_window.refresh()

        else:
            command_window.addstr('Unrecognized command.')
            command_window.refresh()

def main():
    # xterm-color can't handle curs_set(0)
    if os.environ['TERM'] == 'xterm-color':
        os.environ['TERM'] = 'xterm'
    curses.wrapper(run)


if __name__ == '__main__':
    main()
