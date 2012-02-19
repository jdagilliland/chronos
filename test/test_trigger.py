import time

from chronos.main import Trigger

def test_add_padding():
    trigger = Trigger()

    minimum_length = 7

    string = '1'
    padding = ' ' * 3
    padded = trigger.add_padding(string, minimum_length)
    check = padding + '1' + padding
    assert padded == check

    string = '2' * 2
    padding = ' ' * 3
    padded = trigger.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

    string = '3' * 3
    padding = ' ' * 2
    padded = trigger.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

    string = '4' * 4
    padding = ' ' * 2
    padded = trigger.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

    string = '5' * 5
    padding = ' '
    padded = trigger.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

    string = '6' * 6
    padding = ' '
    padded = trigger.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

    string = '7' * 7
    padding = ' '
    padded = trigger.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

    string = '8' * 8
    padding = ' '
    padded = trigger.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

def test_render():
    trigger = Trigger()

    assert trigger.format_seconds(2) == '00:00:02'

    assert trigger.format_seconds(62) == '00:01:02'

    assert trigger.format_seconds(3662) == '01:01:02'

    assert trigger.format_seconds(40272) == '11:11:12'

def test_stop():
    trigger = Trigger()

    trigger.start()
    time.sleep(1)
    trigger.stop()

    elapsed = trigger.get_elapsed()
    assert elapsed > 0

    time.sleep(1)
    assert elapsed == trigger.get_elapsed()

def test_start_and_stop():
    trigger = Trigger()

    assert trigger.get_elapsed() == 0

    trigger.start()
    time.sleep(1)
    trigger.stop()

    elapsed_first_stop = trigger.get_elapsed()
    assert elapsed_first_stop > 0

    trigger.start()
    time.sleep(1)
    trigger.stop()

    elapsed_second_stop = trigger.get_elapsed()

    assert elapsed_second_stop > elapsed_first_stop

