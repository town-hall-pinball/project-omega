Logging
=======

Not much is logged by default. To enable additional logging, copy the
``debug_sample.py`` file in the top-most directory to ``debug.py``. Uncomment
the loggers to see the following information:

============== ================================================================
Logger         Description
============== ================================================================
pin.data       Loading and saving of persistant state
pin.dmd        Dot-matrix stack, queue, and overlay handling
pin.dmd_shift  Current and previous renderer tracking for transitions
pin.event      Global event queue
pin.gi         General illumination lights
pin.keyboard   Key down and up events
pin.handler    Lifecycle events of the game handlers that implement the modes
               of the game
pin.magic      Shows if switch events are accepted, rejected, or trigger by
               a given magic sequence
pin.mixer      Music and sounds being played
pin.resources  Loading of resource assets
pin.server     Lifecylce events for the web server
pin.shows      Lifecycle of scripted events to be shown to the user
pin.switch     Physical switches
============== ================================================================
