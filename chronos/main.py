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

    def __init__(self, config={}):
        self.elapsed = 0
        self.running = False
        self.display_enabled = True
        self.highlight = False

        if config != {}:
            self.build(config)

    def add_time(self, amount):
        self.elapsed += self.parse_time(amount)

    def build(self, config):
        self.window = curses.newwin(config['height'], config['width'], 0, 0)
        self.move(config['pos_y'], config['pos_x'])
        self.title, self.colors = config['title'], config['colors']

    def clear(self):
        self.window.clear()
        self.window.refresh()

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

    def get_coordinates(self):
        return self.window.getbegyx()

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

        if self.highlight:
            self.window.addstr(0, 0, time, self.colors['htime'])
            self.window.addstr(0, len(time), self.title, self.colors['htitle'])
        else:
            self.window.addstr(0, 0, time, self.colors['time'])
            self.window.addstr(0, len(time), self.title, self.colors['title'])

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


@set_interval(1)
def update_trigger(trigger):
    trigger.tick()
    trigger.render()

def capture_command(command_window, description):
    curses.echo()
    command_window.addstr(0, 0, description)
    height, width = command_window.getmaxyx()

    desc_length = len(description)
    command = command_window.getstr(0, desc_length, width - desc_length).decode('utf-8')
    curses.noecho()
    repaint(command_window)

    return command

def define_colors():
    if not curses.has_colors():
        colors = {
            'title': curses.A_NORMAL,
            'htitle': curses.A_REVERSE,
            'time': curses.A_NORMAL,
            'htime': curses.A_REVERSE,
            'status': curses.A_REVERSE
        }
    else:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLUE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        colors = {
            'title': curses.color_pair(1),
            'htitle': curses.color_pair(1) | curses.A_REVERSE,
            'time': curses.color_pair(2),
            'htime': curses.color_pair(2) | curses.A_REVERSE,
            'status': curses.color_pair(3) | curses.A_BOLD
        }
    return colors

def print_help(screen):

    height, width = screen.getmaxyx()
    height -= 3
    width -= 2

    lines = [
        'Help',
        '----',
        '',
        'Commands',
        '',
        'n - Creates and starts a new timer.',
        'j - Move cursor down.',
        'k - Move cursor up.',
        'd - Deletes the selected timer.',
        'e - Edits the title of the selected timer.',
        'p - Pauses/starts the selected timer.',
        'r - Resets the selected timer.',
        'a - Adds time to the selected timer.',
        's - Subtracts time from the selected timer.',
        'q - Quits the program.',
        'h - Shows this help screen.',
        '',
        '',
        'Adding and Subtracting Time',
        '',
        'When entering the amount of time to add or subtract, ',
        'you can use any combination of the following formats:',
        '',
        'xh - x number of hours',
        'ym - y number of minutes',
        'zs - z number of seconds',
        '',
        'So if you wanted to add/subtract 1 hour and 5 minutes, type:',
        '1h5m',
        '',
        'Or if you wanted to add/subtract 45 minutes and 30 seconds, type:',
        '45m30s',
        '',
        '',
        'To return to the main screen, type "q".'
    ]

    pad_y = max(len(lines), height)
    max_y = pad_y - height - 1

    help_window = curses.newpad(pad_y, width)
    for index, line in enumerate(lines):
        help_window.addstr(index, 0, line)

    char = None
    position = 0

    while char != ord('q'):
        help_window.refresh(position, 0, 0, 0, height, width)
        char = screen.getch()

        if char == curses.KEY_DOWN or char == ord('j'):
            position = min(position + 1, max_y)
        elif char == curses.KEY_UP or char == ord('k'):
            position = max(position - 1, 0)

    screen.touchwin()
    screen.refresh()

def repaint(window):
    window.clear()
    window.refresh()

def main():
    # xterm-color can't handle curs_set(0)
    if os.environ['TERM'] == 'xterm-color':
        os.environ['TERM'] = 'xterm'


    screen = curses.initscr()
    colors = define_colors()
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(1)

    height, width = screen.getmaxyx()

    triggers = []
    stoppers = []

    status = "chronos v0.2 - Type 'h' for help, or 'q' to quit."
    status_bar = '{s:<{l}}'.format(s=status, l=width)
    screen.addstr(height - 2, 0, status_bar, colors['status'])

    command_window = curses.newwin(1, width, height - 1, 0)

    keep_alive = True

    position = 0

    while keep_alive:
        char = screen.getch()

        if char == curses.KEY_DOWN or char == ord('j'):
            if position < len(triggers) - 1:
                position += 1
        elif char == curses.KEY_UP or char == ord('k'):
            if position > 0:
                position -= 1

        # New
        elif char == ord('n') and len(triggers) < height - 2:
            prompt = '[NEW] Enter the title: '
            title = capture_command(command_window, prompt)

            config = {
                'colors': colors,
                'height': 1,
                'width': width - 2,
                'title': title,
                'pos_x': 0,
                'pos_y': len(triggers)
            }

            trigger = Trigger(config)
            trigger.start()
            trigger.render()

            stoppers.append(update_trigger(trigger))
            triggers.append(trigger)

        # Delete
        elif char == ord('d') and len(triggers):
            prompt = '[DELETE] Are you sure? [y/N]: '
            command = capture_command(command_window, prompt)
            if command.lower() == 'y':
                stoppers[position].set()
                triggers[position].clear()

                current = position + 1
                while current < len(triggers):
                    y, x = triggers[current].get_coordinates()
                    triggers[current].move(y - 1, x)
                    current += 1

                del triggers[position]
                del stoppers[position]
                if position == len(triggers) and position:
                    position -= 1

                repaint(screen)
                screen.addstr(height - 2, 0, status_bar, colors['status'])

        # Edit
        elif char == ord('e') and len(triggers):
            prompt = '[EDIT] Enter the title: '
            title = capture_command(command_window, prompt)
            triggers[position].set_title(title)

        # Add
        elif char == ord('a') and len(triggers):
            prompt = '[ADD] Enter the amount of time: '
            time = capture_command(command_window, prompt)
            triggers[position].add_time(time)

        # Subtract
        elif char == ord('s') and len(triggers):
            prompt = '[SUBTRACT] Enter the amount of time: '
            time = capture_command(command_window, prompt)
            triggers[position].subtract_time(time)

        # Pause
        elif char == ord('p') and len(triggers):
            triggers[position].toggle()

        # Reset
        elif char == ord('r') and len(triggers):
            prompt = '[RESET] Are you sure? [y/N]: '
            command = capture_command(command_window, prompt)
            if command.lower() == 'y':
                triggers[position].reset()

        # Help
        elif char == ord('h'):
            for trigger in triggers:
                trigger.disable_display()
            print_help(screen)
            for trigger in triggers:
                trigger.enable_display()
                trigger.redraw()

        # Quit
        elif char == ord('q'):
            prompt = '[QUIT] Are you sure? [y/N]: '
            command = capture_command(command_window, prompt)
            keep_alive = ( command.lower() != 'y' )


        for index, trigger in enumerate(triggers):
            if index == position:
                triggers[index].set_highlight(True)
            else:
                triggers[index].set_highlight(False)
            triggers[index].render()


    curses.endwin()


if __name__ == '__main__':
    main()
