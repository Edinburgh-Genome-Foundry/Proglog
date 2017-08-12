"""Implements the generic progress logger class, and the ProgressBar class.

WORK IN PROGRESS DO NOT USE
"""

from tqdm import tqdm, tqdm_notebook
from collections import OrderedDict

SETTINGS = {
    'notebook': False
}

class ProgressLogger:
    """Generic class for progress loggers.

    A progress logger contains a "state" dictionnary
    """

    def __init__(self, init_state=None):

        self.state = {}
        if init_state is not None:
            self.state.update(init_state)

    def callback(self, **kw):
        pass

    def iter(self, **kw):
        for field, iterable in kw.items():
            for it in iterable:
                self(**{field: it})
                yield it


    def __call__(self, **kw):
        self.state.update(kw)
        self.callback(**kw)


class ProgressBarLogger(ProgressLogger):
    """Generic class for progress loggers.

    A progress logger contains a "state" dictionnary
    """

    def __init__(self, init_state=None, bars=None, ignored_bars=()):
        ProgressLogger.__init__(self, init_state)
        if bars is None:
            bars = OrderedDict()
        elif isinstance(bars, (list, tuple)):
            bars = OrderedDict([
                (b, dict(name=b, index=-1, total=None, message=None))
                for b in bars
            ])
        self.ignored_bars = set(ignored_bars)
        self.state['bars'] = bars

    @property
    def bars(self):
        """Return self.state['bars']."""
        return self.state['bars']

    def iter_bar(self, **kw):
        for bar, iterable in kw.items():
            if bar in self.ignored_bars:
                for it in iterable:
                    yield it
                break
            if hasattr(iterable, '__len__'):
                self(**{bar + '__total': len(iterable)})
            for i, it in enumerate(iterable):
                self(**{bar + '__index': i})
                yield it
            self(**{bar + '__index': i + 1})

    def bars_callback(self, bar, attr, value, old_value=None):
        """Execute a custom action after the progress bars are updated.

        Parameters
        ----------
        bar
          Name/ID of the bar to be modified.

        attr
          Attribute of the bar attribute to be modified

        value
          New value of the attribute

        old_value
          Previous value of this bar's attribute.
        """
        pass

    def callback(self, **kw):
        pass

    def __call__(self, **kw):

        for key, value in sorted(kw.items(),
                                 key=lambda kv: not kv[0].endswith('total')):
            if '__' in key:
                bar, attr = key.split('__')
                if bar in self.ignored_bars:
                    continue
                if bar == 'mutation':
                    raise ValueError()
                kw.pop(key)
                if (bar not in self.bars) and (bar not in self.ignored_bars):
                    self.bars[bar] = dict(name=bar, index=-1,
                                          total=None, message=None)
                old_value = self.bars[bar][attr]
                self.bars[bar][attr] = value
                self.bars_callback(bar, attr, value, old_value)
        self.state.update(kw)
        self.callback(**kw)

class TqdmProgressBarLogger(ProgressBarLogger):

    def __init__(self, init_state=None, bars=None, leave_bars=False,
                 ignored_bars=(), notebook='default', print_messages=True):
        ProgressBarLogger.__init__(self, init_state=init_state, bars=bars,
                                   ignored_bars=ignored_bars)
        self.leave_bars = leave_bars
        self.tqdm_bars = OrderedDict([
            (bar, None)
            for bar in self.bars
        ])
        if notebook == 'default':
            notebook = SETTINGS['notebook']
        self.notebook = notebook
        self.print_messages = print_messages
        self.tqdm = (tqdm_notebook if self.notebook else tqdm)

    def new_tqdm_bar(self, bar):
        if self.tqdm_bars[bar] is not None:
            self.close_tqdm_bar(bar)
        infos = self.bars[bar]
        self.tqdm_bars[bar] = self.tqdm(
           total=infos['total'],
           desc=infos['name'],
           postfix=infos['message'],
           leave=self.leave_bars
        )
    def close_tqdm_bar(self, bar):
        self.tqdm_bars[bar].close()
        self.tqdm_bars[bar] = None

    def bars_callback(self, bar, attr, value, old_value):
        if self.tqdm_bars[bar] is None:
            self.new_tqdm_bar(bar)
        if attr == 'index':
            if value >= old_value:
                self.tqdm_bars[bar].update(value - old_value)
                total = self.bars[bar]['total']
                if total and (value >= total):
                    self.close_tqdm_bar(bar)
            else:
                self.new_tqdm_bar(bar)
                self.tqdm_bars[bar].update(value + 1)
    def callback(self, **kw):
        if self.print_messages and ('message' in kw) and kw['message']:
            self.tqdm.write(kw['message'])

class RqWorkerProgressLogger:
    def __init__(self, job):
        self.job = job
        if 'progress_data' not in self.job.meta:
            self.job.meta['progress_data'] = {}
            self.job.save()

    def callback(self, **kw):
        self.job.meta['progress_data'] = self.state
        self.job.save()

class RqWorkerBarLogger(ProgressBarLogger, RqWorkerProgressLogger):

    def __init__(self, job, init_state=None, bars=None, ignored_bars=()):
        RqWorkerBarLogger.__init__(self, job)
        ProgressBarLogger.__init__( init_state=init_state, bars=bars,
                                   ignored_bars=ignored_bars)
