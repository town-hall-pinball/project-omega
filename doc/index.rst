Project Omega
=============

Town Hall Pinball Studios is working on a customized pinball machine. The overall plan is to:

* Use an existing pinball machine, "No Fear"
* Completely rebrand it with a new play-field, backglass, and cabinet artwork
* Design a new theme
* Design a new ruleset
* Design and/or use new animations, sound effects, and music

We are using the
`P-ROC <http://www.pinballcontrollers.com/index.php/products/p-roc>`_
to interface with the pinball machine and our own software to implement the game.

Since the name of the game has not yet been decided, this repository will be called "project-omega" for now. It will be renamed in the future.

Feel free to clone the repository and see development in action. This code can be run without an actual pinball machine. Anything and everything can be broken at anytime.

User Guide
----------

* :doc:`Getting Started <user/getting_started>`
* :doc:`Take a Tour <user/tour>`
* :doc:`Keyboard Bindings <user/keyboard>`

Developer's Guide
-----------------

* :doc:`Logging <developer/logging>`
* :doc:`Documentation and Testing <developer/paver>`
* :doc:`Adding Resources (Music, Sounds, Images, etc) <developer/resources>`

API Reference
-------------

Note: This is not up-to-date at the moment.

Contents:

.. toctree::
   :maxdepth: 2

   api/pin/engine
   api/pin/events
   api/pin/timers
   api/pin/virtual/dmd
