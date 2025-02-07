===================================================
Example CytoContainer Docker App
===================================================

Contains a code to build a Docker container that has several sample
Cytoscape Service Apps that are meant to be incorporated into a running
`CytoscapeContainer REST Service <https://github.com/cytoscape/cytocontainer-rest-server>`__

Dependencies
------------

* `Docker <https://www.docker.com/>`_
* `make <https://www.gnu.org/software/make/>`_ (to build)
* Python (to build)

Direct invocation
------------------

.. code-block::

   docker run --rm -v `pwd`:`pwd` coleslawndex/testcywebserviceapp:0.9.0 -h

Building
--------

.. code-block::

   git clone https://github.com/idekerlab/test_cyweb_service_app
   cd test_cyweb_service_app
   make dockerbuild

Run **make** command with no arguments to see other build/deploy options including creation of Docker image

.. code-block::

   make

Output:

.. code-block::

   clean                remove all build, test, coverage and Python artifacts
   clean-build          remove build artifacts
   clean-pyc            remove Python file artifacts
   clean-test           remove test and coverage artifacts
   lint                 check style with flake8
   test                 run tests quickly with the default Python
   test-all             run tests on every Python version with tox
   coverage             check code coverage quickly with the default Python
   docs                 generate Sphinx HTML documentation, including API docs
   servedocs            compile the docs watching for changes
   testrelease          package and upload a TEST release
   release              package and upload a release
   dist                 builds source and wheel package
   install              install the package to the active Python's site-packages
   dockerbuild          build docker image and store in local repository
   dockerpush           push image to dockerhub


Usage
-----

.. code-block::

   docker run -v coleslawndex/testcywebserviceapp:0.9.0 -h


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
