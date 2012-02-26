chronos
=======

chronos is an ncurses stopwatch/timer.  It supports multiple simultaneous
timers, which makes it ideal for keeping track of time spent on various tasks.

Show me the goods
-----------------

.. image:: http://nsinopoli.github.com/chronos/chronos02.png

Okay, how do I use it?
----------------------

Installing
~~~~~~~~~~

From the command line::

    pip install chronos

If chronos is already installed, you can upgrade to the latest version with::

    pip install --upgrade chronos

Usage
~~~~~

To use chronos, run it from the command line::

    chronos

Commands
~~~~~~~~

The following commands are supported::

    n - Creates and starts a new timer.
    j - Move cursor down.
    k - Move cursor up.
    d - Deletes the selected timer.
    e - Edits the title of the selected timer.
    p - Pauses/starts the selected timer.
    r - Resets the selected timer.
    a - Adds time to the selected timer.
    s - Subtracts time from the selected timer.
    q - Quits the program.
    h - Shows the help screen.

Adding and Subtracting Time
+++++++++++++++++++++++++++

When entering the amount of time to add or subtract, you can use any
combination of the following formats::

    xh - x number of hours
    ym - y number of minutes
    zs - z number of seconds

So if you wanted to add/subtract 1 hour and 5 minutes, type::

    1h5m

Or if you wanted to add/subtract 45 minutes and 30 seconds, type::

    45m30s

Version Information
-------------------

Current stable release is v0.2, last updated on 26 February 2012.

Feedback
--------

Feel free to send any feedback you may have regarding this project to NSinopoli@gmail.com.
