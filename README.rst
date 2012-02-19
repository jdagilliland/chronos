chronos
=======

chronos is an ncurses stopwatch/timer.  It supports multiple simultaneous timers, which makes it ideal for keeping track of time spent on various tasks.

Show me the goods
-----------------

.. image:: http://nsinopoli.github.com/chronos/chronos.png

Okay, how do I use it?
----------------------

Installing
~~~~~~~~~~

From the command line::

    pip install chronos

Usage
~~~~~

To use chronos, run it from the command line::

    chronos

You should see a blank screen with a border.

Commands
~~~~~~~~

Type ":" to bring up a command window at the bottom of the screen (yes, a la Vim).  The following commands are supported::

    n [title]   - Creates and starts a new timer.
    e[n][title] - Edits the title of the nth timer.
    p[n]        - Pauses/starts the nth timer.
    r[n]        - Resets the nth timer.
    q           - Quits the program.
    h           - Shows the help screen.

So, to create a timer titled, 'Test', simply type::

    :n Test

Then, to pause it::

    :p1

To reset it::

    :r1

Version Information
-------------------

Current stable release is v0.1, last updated on 12 February 2012.

Feedback
--------

Feel free to send any feedback you may have regarding this project to NSinopoli@gmail.com.
