from abjad.spanners.spanner.grobhandler import _GrobHandlerSpanner
from abjad.spanners.tie.format import _TieSpannerFormatInterface


class Tie(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Tie', music)
      self._format = _TieSpannerFormatInterface(self)
