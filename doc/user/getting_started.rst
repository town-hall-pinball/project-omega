Getting Started
===============

Requirements
------------

* `VirtualBox <https://www.virtualbox.org>`_
* `Vagrant <https://www.vagrantup.com>`_

Mac OS X Specific
~~~~~~~~~~~~~~~~~

* `X11, Xquartz <http://xquartz.macosforge.org/trac/wiki>`_

Windows Specific
~~~~~~~~~~~~~~~~

* `Cygwin <https://www.cygwin.com>`_
* `X11, Xming <https://sourceforge.net/projects/xming/files/latest/download>`_

Running
-------

Setup a development environment as follows:

Open a terminal (open Cygwin in Windows) and clone the repository::

    mkdir town-hall-pinball
    cd town-hall-pinball
    git clone https://github.com/town-hall-pinball/project-omega.git

Initialize the virtual machine with::

    cd project-omega
    vagrant up

Wait for the command to complete, and run the software as follows::

    vagrant ssh
    pingame -d -s

A dot-matrix display should appear.
