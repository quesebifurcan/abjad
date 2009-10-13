from abjad.spanners.beam.format import _BeamSpannerFormatInterface
from abjad.spanners.spanner.grobhandler import _GrobHandlerSpanner


class Beam(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Beam', music)
      self._format = _BeamSpannerFormatInterface(self)
