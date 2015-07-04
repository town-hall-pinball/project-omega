Documentation and Testing
=========================

* Documentation: https://readthedocs.org/projects/project-omega
* CI: https://travis-ci.org/town-hall-pinball/project-omega
* Coverage: https://coveralls.io/r/town-hall-pinball/project-omega

Log in to the Vagrant virtual machine and change to the base directory::

    cd /vagrant

Documentation
-------------

Build documents with::

    paver doc

The output is placed in ``build/doc``

Tests
-----

Run the test suite with::

    paver test
