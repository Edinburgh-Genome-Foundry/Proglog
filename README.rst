Proglog
=========

.. image:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Proglog/master/logo.png
    :align: center

Proglog is a simple logging system for Python. It allows to build complex
libraries while giving the user control on the management of logs and progress
bars.

What problem does it solve ?
----------------------------

The simplest way to get progress bars in python is with ``tqdm``

.. code:: python

    from tqdm import tqdm
    for i in tqdm(range(10000)):
      ...

.. code:: shell

    76%|████████████████████████████         | 7568/10000 [00:33<00:10, 229.00it/s]

While this is great for quick scripts, it works less well when you want to:

- Log more than just progress bars, for instance pictures, text, or any python object.
- Selectively mute some progress bars.
- Let your project's users customize the way the logs and progress bars are
  handled, for instance to send the progress over to some webclient instead of the console.

Proglog solves this by sending the logs to any backend, such as tqdm, or some web
database. You can change where the data is sent just by using a different logger
class, without modification of your core code.

It does so by having a single logger used everywhere in your project:

.. code:: python

    logger = TqdmProgressBarLogger()
    for i in logger.iter_bar(main=range(10)):
        for j in logger.iter_bar(sub=range(10)):
            ... do suff here
        if i == 3:
            logger(message="We just passed i=3")

.. code:: shell

    We just passed i=3
    main:  50%|████████████▌            | 5/10 [00:04<00:04,  1.20it/s]
    sub:  100%|████████████████████████| 10/10 [00:00<00:00, 10.26it/s]


Now the complete logging behaviour can be customized by modifying the logger
definition, for instance ``TqdmProgressBarLogger(ignored_bars=['sub'])`` to mute
the ``sub`` bar, or ``logger=RqWorkerBarLogger(job=some_rq_job)`` to update the
status of a ``python-rq`` asynchronous job.


Installation
-------------

You can install Proglog through PIP

.. code:: shell

    sudo pip install proglog

Alternatively, you can unzip the sources in a folder and type

.. code:: shell

    sudo python setup.py install

To use the ``tqdm`` notebook-style progress bars you need to install and enable
iwidgets:

.. code:: shell

    sudo pip install ipywidgets
    sudo jupyter nbextension enable --py --sys-prefix widgetsnbextension


Licence
--------

Proglog is an open-source software originally written at the `Edinburgh Genome Foundry
<http://www.genomefoundry.io>`_ by `Zulko <https://github.com/Zulko>`_
and `released on Github <https://github.com/Edinburgh-Genome-Foundry/DnaCauldron>`_ under
the MIT licence (copyright Edinburgh Genome Foundry).
Everyone is welcome to contribute !
