import time

from trigger.main import Timer

def test_render():
    timer = Timer()

    assert timer.render(2) == '00:00:02'

    assert timer.render(62) == '00:01:02'

    assert timer.render(3662) == '01:01:02'

    assert timer.render(40272) == '11:11:12'

def test_stop():
    timer = Timer()

    timer.start()
    time.sleep(1)
    timer.stop()

    elapsed = timer.get_elapsed()
    assert elapsed > 0

    time.sleep(1)
    assert elapsed == timer.get_elapsed()

def test_start_and_stop():
    timer = Timer()

    assert timer.get_elapsed() == 0

    timer.start()
    time.sleep(1)
    timer.stop()

    elapsed_first_stop = timer.get_elapsed()
    assert elapsed_first_stop > 0

    timer.start()
    time.sleep(1)
    timer.stop()

    elapsed_second_stop = timer.get_elapsed()

    assert elapsed_second_stop > elapsed_first_stop

