.. raw:: html

    <p align="center">
    <img alt="Proglog Logo" title="Proglog Logo" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Proglog/master/logo.png" width="500">
    <br /><br />
    </p>

.. image:: https://github.com/Edinburgh-Genome-Foundry/Proglog/actions/workflows/build.yml/badge.svg
    :target: https://github.com/Edinburgh-Genome-Foundry/Proglog/actions/workflows/build.yml
    :alt: GitHub CI build status

.. image:: https://coveralls.io/repos/github/Edinburgh-Genome-Foundry/Proglog/badge.svg?branch=master
    :target: https://coveralls.io/github/Edinburgh-Genome-Foundry/Proglog?branch=master

Proglog is a progress logging system for Python. It allows to build complex
libraries while giving your  users control over logs, callbacks and progress bars.

**What problems does it solve ?**

Libraries like `tqdm <https://github.com/noamraph/tqdm>`_ or `progress <https://github.com/verigak/progress/>`_ are great for quickly adding progress bars to your scripts, but become difficult to manage when building larger projects.

For instance, you will need to write different code depending on whether you are displaying the progress in a console, a Jupyter notebook, or a webpage.

Sometimes a single program may have to handle many logs and progress bars coming from different subprograms and libraries, at which case you may want to let the final user decide which progress bars they want to display or to mute, even when these progress bars are handled deep down in your program.

For instance if your program 1 calls a program 2 and program 3 (possibly from other libraries), you may want to be able to silence the progress bars of routine 2, or to only show the progress bars of routine 1. As long as all routines use Proglog, this will be easy to do.

.. raw:: html

    <p align="center">
    <img src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Proglog/master/docs/run_and_get_progress.png"    width="650">
    </p>


You may also want to log more than just progress bars, have specific callback fonctions, print the logs in human-readable format... Proglog provides all these features.


Usage
-----

Assume that you are writing a library called ``my_library`` in which you define a routine as follows:

.. code:: python

    import time  # for simulating computing time
    from proglog import default_bar_logger

    def my_routine(iterations=10, logger='bar'):
        """Run several loops to showcase Proglog."""
        logger = default_bar_logger(logger)  # shorthand to generate a bar logger
        for i in logger.iter_bar(iteration=range(iterations)):
            for j in logger.iter_bar(animal=['dog', 'cat', 'rat', 'duck']):
                time.sleep(0.1)  # simulate some computing time

Now when the library users run a program in the console, they will get a console progress bar:

.. code:: python

    from my_library import my_routine
    my_routine()

.. raw:: html

    <p align="center">
    <img src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Proglog/master/docs/console_bar.png"    width="450">
    </p>

If the users run the routine inside a Jupyter/IPython notebook, they only need to write ``proglog.notebook()`` at the beginning of the notebook to obtain HTML progress bars:

.. code:: python

    import proglog
    proglog.notebook()

    from my_library import my_routine
    my_routine()

.. raw:: html

    <p align="center">
    <img src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Proglog/master/docs/notebook_bar.png"    width="450">
    </p>


If the user wishes to turn off all progress bars:

.. code:: python

    from my_library import my_routine
    my_routine(logger=None)

If the user is running the routine on a web server and would want to attach the
data to an asynchronous Python-RQ job, all they need is yet a different logger:

.. code:: python

    from proglog import RqWorkerBarLogger
    from my_library import my_routine

    logger = RqWorkerBarLogger(job=some_python_rq_job)
    my_routine(logger=logger)

This allows to then display progress bars on the website such as these (see the `EGF CUBA <https://github.com/Edinburgh-Genome-Foundry/CUBA>`_ project for an example of website using Proglog):

.. raw:: html

    <p align="center">
    <img src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Proglog/master/docs/website_bar.png"    width="450">
    </p>


The user may also want a custom progress logger which selectively ignores the ``animals`` progress bar, and only updates its bars every second (to save computing time):

.. code:: python

    from proglog import TqdmProgressBarLogger
    from my_library import my_routine

    logger = TqdmProgressBarLogger(ignored_bars=('animal',),
                                   min_time_interval=1.0)
    my_routine(logger=logger)

Proglog loggers can be used for much more than just progress bars. They can in fact store any kind of data with a simple API:

.. code:: python

    logger(message='Now running the main program, be patient...')
    logger(current_animal='cat')
    logger(last_number_tried=1235)

For more complex customization, such as adding callback functions which will be executed every time the logger's state is updated, simply create a new logger class:

.. code:: python

    from proglog import ProgressBarLogger
    from my_library import my_routine

    class MyBarLogger(ProgressBarLogger):

        def callback(self, **changes):
            # Every time the logger is updated, this function is called with
            # the `changes` dictionnary of the form `parameter: new value`.

            for (parameter, new_value) in changes.items():
                print ('Parameter %s is now %s' % (parameter, value))

    logger = MyBarLogger()
    my_routine(logger=logger)

When writing libraries which all log progress and may depend on each other, simply pass the Proglog logger from one program to its dependencies, to obtain one logger keeping track of all progress across libraries at once:

.. raw:: html

    <p align="center">
    <img src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Proglog/master/docs/loggers_schema.png"    width="650">
    </p>

Note that this implies that not two libraries use the same variables or loop names, which can be avoided by attributing prefixes to these names:

.. code:: python

    for i in logger.iter_bar(iteration=range(iterations), bar_prefix='libraryname_'):
        ...


Installation
------------

You can install Proglog through PIP:

.. code:: shell

    pip install proglog

Alternatively, you can unzip the sources in a folder and type:

.. code:: shell

    python setup.py install

To use the ``tqdm`` notebook-style progress bars you need to install iwidgets:

.. code:: shell

    pip install ipywidgets

This `should automatically enable it <https://ipywidgets.readthedocs.io/en/latest/user_install.html>`_; for older versions try:

.. code:: shell

    jupyter nbextension enable --py --sys-prefix widgetsnbextension


License = MIT
-------------

Proglog is an open-source software originally written at the `Edinburgh Genome Foundry
<https://www.ed.ac.uk/biology/research/facilities/edinburgh-genome-foundry>`_ by `Zulko <https://github.com/Zulko>`_
and `released on Github <https://github.com/Edinburgh-Genome-Foundry/DnaCauldron>`_ under
the MIT license (Copyright 2017 Edinburgh Genome Foundry).

Proglog was not written by loggology experts, it *just works* with our projects and we use it a lot.
Everyone is welcome to contribute if you find bugs or limitations !
