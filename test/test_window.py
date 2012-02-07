from trigger.main import Window

def test_add_padding():
    window = Window()

    minimum_length = 7

    string = '1'
    padding = ' ' * 3
    padded = window.add_padding(string, minimum_length)
    check = padding + '1' + padding
    assert padded == check

    string = '2' * 2
    padding = ' ' * 3
    padded = window.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

    string = '3' * 3
    padding = ' ' * 2
    padded = window.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

    string = '4' * 4
    padding = ' ' * 2
    padded = window.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

    string = '5' * 5
    padding = ' '
    padded = window.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

    string = '6' * 6
    padding = ' '
    padded = window.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

    string = '7' * 7
    padding = ' '
    padded = window.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check

    string = '8' * 8
    padding = ' '
    padded = window.add_padding(string, minimum_length)
    check = padding + string + padding
    assert padded == check
