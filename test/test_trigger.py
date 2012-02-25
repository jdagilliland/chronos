from chronos.main import Trigger

def test_add_time():
    trigger = Trigger()

    trigger.add_time('1s')
    assert trigger.get_elapsed() == 1

    trigger.add_time('5m')
    assert trigger.get_elapsed() == 301

    trigger.add_time('1h')
    assert trigger.get_elapsed() == 3901

    trigger.add_time('20m10s')
    assert trigger.get_elapsed() == 5111

    trigger.add_time('2h10s')
    assert trigger.get_elapsed() == 12321

    trigger.add_time('3h11m10s')
    assert trigger.get_elapsed() == 23791

    trigger.add_time('32e9p')
    assert trigger.get_elapsed() == 23791

def test_format_seconds():
    trigger = Trigger()

    assert trigger.format_seconds(2) == '00:00:02'

    assert trigger.format_seconds(62) == '00:01:02'

    assert trigger.format_seconds(3662) == '01:01:02'

    assert trigger.format_seconds(40272) == '11:11:12'

def test_stop():
    trigger = Trigger()

    trigger.start()
    trigger.tick()
    trigger.stop()

    elapsed = trigger.get_elapsed()
    assert elapsed == 1

    trigger.tick()
    assert elapsed == trigger.get_elapsed()

def test_start_and_stop():
    trigger = Trigger()

    assert trigger.get_elapsed() == 0

    trigger.start()
    trigger.tick()
    trigger.stop()

    elapsed_first_stop = trigger.get_elapsed()
    assert elapsed_first_stop == 1

    trigger.start()
    trigger.tick()
    trigger.stop()

    elapsed_second_stop = trigger.get_elapsed()

    assert elapsed_second_stop > elapsed_first_stop

def test_subtract_time():
    trigger = Trigger()

    trigger.elapsed = 23791

    trigger.subtract_time('3h11m10s')
    assert trigger.get_elapsed() == 12321

    trigger.subtract_time('2h10s')
    assert trigger.get_elapsed() == 5111

    trigger.subtract_time('20m10s')
    assert trigger.get_elapsed() == 3901

    trigger.subtract_time('1h')
    assert trigger.get_elapsed() == 301

    trigger.subtract_time('5m')
    assert trigger.get_elapsed() == 1

    trigger.subtract_time('1s')
    assert trigger.get_elapsed() == 0

    trigger.subtract_time('4m')
    assert trigger.get_elapsed() == 0
