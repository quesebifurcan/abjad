from abc import ABCMeta
from abjad.tools.instrumenttools._ReedInstrument import _ReedInstrument


class _SingleReedInstrument(_ReedInstrument):
    '''.. versionadded:: 2.0

    Abjad model of single-reed instruments.
    '''
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        _ReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'single reed instrument'
        self._default_performer_names.append('single reed player')
